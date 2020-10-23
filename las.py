#!/usr/bin/env python
"""
Delete unnecessary LAS file part for RMS import
!!! Replace original files !!!
"""

import os
import time
import re
from runner import run


def main():
    files = [i for i in os.listdir() if '.las' in i]

    for file in files:
        with open(file, 'r') as f:
            content = f.read()
        content = re.sub('~Parameter Information(.|\n)+~ASCII Log Data',
                         '\n~ASCII Log Data', content, re.MULTILINE)
        with open(file, 'w') as f:
            f.write(content)


# -------------------MAIN----------------------#
if __name__ == '__main__':
    run(main)
