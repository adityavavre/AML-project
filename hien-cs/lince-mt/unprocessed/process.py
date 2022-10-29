import sys

for line in sys.stdin:
    print(line.strip().split('\t')[1])