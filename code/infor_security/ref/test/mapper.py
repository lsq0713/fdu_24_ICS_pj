#!/usr/bin/env python

import sys
import csv

def mapper():
    reader = csv.DictReader(sys.stdin)
    for row in reader:
        for key, value in row.items():
            words = value.split()
            for word in words:
                print(f"{key}\t{word}\t1")

if __name__ == "__main__":
    mapper()