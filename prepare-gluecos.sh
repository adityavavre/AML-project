# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Usage: ./prepare-gluecos.sh
#

set -e

# data paths
MAIN_PATH=$PWD
OUTPATH=$PWD/gluecos-data/
TOOLS_PATH=$PWD/tools
PROCESSED_PATH=$PWD/gluecos-data/processed/XLMR-17
CODES_PATH=$MAIN_PATH/other-data/XLMR-17-codes
VOCAB_PATH=$MAIN_PATH/other-data/XLMR-17-vocab
FASTBPE=$TOOLS_PATH/fastBPE/fast


# # Get BPE codes and vocab (MODIFY if needed)
# wget -c https://dl.fbaipublicfiles.com/XLM/codes_en -P $MAIN_PATH
# wget -c https://dl.fbaipublicfiles.com/XLM/vocab_en -P $MAIN_PATH

# apply BPE codes and binarize the GLUE corpora
glue_tasks="SST-2 QNLI" # TODO: missing MRPC

for task in $glue_tasks
do
  if [ ! -d $PROCESSED_PATH/eval/$task ]; then
    mkdir -p $PROCESSED_PATH/eval/$task
  else
    rm -r $PROCESSED_PATH/eval/$task/*
  fi
  for splt in train dev test
  do
    FPATH=$OUTPATH/${task}/${splt}.tsv

    cut -f1 $FPATH > ${FPATH}.f1
    $FASTBPE applybpe $PROCESSED_PATH/eval/$task/${splt}.s1 ${FPATH}.f1 $CODES_PATH
    python preprocess.py $VOCAB_PATH $PROCESSED_PATH/eval/$task/${splt}.s1
    rm ${FPATH}.f1

    if [ "$task" != "CoLA" ] && [ "$task" != "SST-2" ]
    then
      cut -f2 $FPATH > ${FPATH}.f2
      $FASTBPE applybpe $PROCESSED_PATH/eval/$task/${splt}.s2 ${FPATH}.f2 $CODES_PATH
      python preprocess.py $VOCAB_PATH $PROCESSED_PATH/eval/$task/${splt}.s2
      rm ${FPATH}.f2
      
      cut -f3 $FPATH > $PROCESSED_PATH/eval/$task/${splt}.label
    else
      cut -f2 $FPATH > $PROCESSED_PATH/eval/$task/${splt}.label
    fi
  done
done
