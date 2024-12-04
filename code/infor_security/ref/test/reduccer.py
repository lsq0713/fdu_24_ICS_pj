#!/usr/bin/env python

import sys

def reducer():
    current_key = None
    current_count = 0
    key = None

    for line in sys.stdin:
        line = line.strip()
        key, word, count = line.split('\t', 2)
        count = int(count)

        if current_key == (key, word):
            current_count += count
        else:
            if current_key:
                print(f"{current_key[0]}\t{current_key[1]}\t{current_count}")
            current_key = (key, word)
            current_count = count

    if current_key == (key, word):
        print(f"{current_key[0]}\t{current_key[1]}\t{current_count}")

if __name__ == "__main__":
    reducer()