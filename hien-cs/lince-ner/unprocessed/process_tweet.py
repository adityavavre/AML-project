import sys
import csv
import preprocessor

for line in sys.stdin:
    print(preprocessor.clean(line.strip()))