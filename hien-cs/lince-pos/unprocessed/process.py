import sys

sentence=[]
for line in sys.stdin:
    # train
    split_line = line.strip().split('\t')
    if len(split_line) < 2:
        if not sentence:
            continue
        else:
            print(' '.join(sentence))
            sentence.clear()
    else:
        sentence.append(split_line[0])