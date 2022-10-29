import pandas as pd
import os
from shutil import copyfile

for split in ['train.tsv', 'dev.tsv', 'test.tsv']:
    print(split)
    backupn = 1
    while os.path.exists(split + ".backup" + str(backupn)):
        backupn += 1
    copyfile(split, split + ".backup" + str(backupn))
    data = pd.read_csv(split, delimiter="\t")
    data.replace(r"\s+", " ", inplace=True, regex=True)
    data['question'] = data['question'].str.lower()
    data['sentence'] = data['sentence'].str.lower()
    del data['index']
    data.to_csv(split, sep="\t", header=False, index=False, mode='w')
