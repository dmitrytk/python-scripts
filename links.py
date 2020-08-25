#!/usr/bin/env python
"""
find links to literature for all <.docx> files in folder
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

pattern = re.compile("\[[^\]]+")


def sorted_set(arr):
    res_arr = []
    for i in arr:
        if i not in res_arr:
            res_arr.append(i)
    return res_arr


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


os.system("cls")


def main():
    print("Processing, please wait.")
    doc_files = [i for i in os.listdir() if ".docx" in i and "$" not in i]
    result_txt = ""
    links = []

    for file in doc_files:

        txt = get_docx_text(file)

        if "[" in txt:
            result_txt += file.replace(".docx", "").capitalize() + "\n"
            arr = pattern.findall(txt)
            arr = [i + "]" for i in arr]
            for i in arr:
                links.append(i)
                result_txt += " " + i + "\n"
            result_txt += "\n"

    res_links = []
    for i in links:
        i = re.sub("\[|\]", "", i)
        if "," in i:
            arr = i.split(",")
            for j in arr:
                res_links.append(j.strip())
        else:
            res_links.append(i.strip())

    set_links = sorted_set(res_links)
    st = "Количество ссылок: " + str(len(set_links))
    result_txt += "\n" + 30 * "-" + "\n"
    result_txt += st + '\n'
    result_txt += 30 * "-" + "\n"

    result_txt += "\nСтарые\tНовые\n"
    for link in res_links:
        result_txt += "[" + link + "]" + "\t" + "[" + str(
            set_links.index(link) + 1) + "]" + "\n"

    with open("Ссылки.txt", "w") as f:
        f.write(result_txt)
    os.system("start ссылки.txt")


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
