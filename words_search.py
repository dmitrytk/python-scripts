#!/usr/bin/env python
"""
Search for words in <in.txt> in all docx files in current folder.
Write search result in <out.txt>
Search in lower register.
<in.txt> file format:
    южно-киняминское
    уватская
    шапшинское
"""

import os
import re
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile
import time

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'


def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [
            node.text for node in paragraph.getiterator(TEXT) if node.text
        ]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n\n'.join(paragraphs)


def main():
    print("Processing\n\n\n")
    files = os.listdir()
    files = [i for i in files if ".docx" in i and '~$' not in i]

    try:
        with open('in.txt', 'r') as file:
            words = file.read()
            words = words.split('\n')
            words = [i.lower() for i in words if i != '']
        with open('out.txt', 'w') as file:
            file.write('')
    except Exception as e:
        print(e)
        input("File in.txt not found. Create it and try again.")
        exit()
    counter = 0

    for file_name in files:
        with open('out.txt', 'a') as file:
            file.write(file_name + '\n')
            print(file_name + '\n')
        txt = get_docx_text(file_name).lower()
        for word in words:
            if word in txt:
                counter += 1
                with open('out.txt', 'a') as file:
                    file.write('\t ' + word + '\n')
                    print('\t ' + word + '\n')

    print(f'Done in {time.perf_counter()} sec')
    input(f'\n\n{counter} matches found.\n')


# -------------------MAIN----------------------#
if __name__ == "__main__":
    try:
        print("processing")
        main()
        print("Done!")
        time.sleep(3)
    except Exception as e:
        print(e)
        input()
