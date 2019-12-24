'''
Delete unnecessary LAS file part for RMS import
!!! Replace original files
'''

import os
import time
import re


def main():
    print("Executing")
    files = [i for i in os.listdir() if ".las" in i]

    for file in files:
        with open(file, "r") as f:
            content = f.read()
        content = re.sub("~Parameter Information(.|\n)+~ASCII Log Data",
                         "\n~ASCII Log Data", content, re.MULTILINE)
        with open(file, "w") as f:
            f.write(content)


if __name__ == "__main__":
    try:
        main()
        print(f"done in {time.perf_counter()} sec.")
        time.sleep(3)

    except Exception as e:
        print(e)
        input()
