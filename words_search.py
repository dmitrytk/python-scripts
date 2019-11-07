"""
Поиск слов из файла in.txt во всех файлах docx в текущей папке.
Результаты записываются в файл out.txt
Поиск ведется в нижнем регистре.
Формат файла in.txt:
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
    os.system('cls')
    print("Обрабатывается\n\n\n")
    files = os.listdir()
    files = [file_name for file_name in files if ".docx" in file_name and '~$' not in file_name]

    try:
        with open('in.txt', 'r') as file:
            words = file.read()
            words = words.split('\n')
            words = [i.lower() for i in words if i != '']
        with open('out.txt', 'w') as file:
            file.write('')
    except Exception as e:
        print(e)
        input("Файл in.txt не найден. Создайте его и попробуйте снова.\nНажмите Enter для выхода")
        exit()
    counter=0

    for file_name in files:
        with open('out.txt', 'a') as file:
            file.write(file_name + '\n')
            print(file_name + '\n')
        txt = get_docx_text(file_name).lower()
        for word in words:
            if word in txt:
                counter+=1
                with open('out.txt', 'a') as file:
                    file.write('\t ' + word + '\n')
                    print('\t ' + word + '\n')

    print(f'Завершено за {time.perf_counter()} сек')
    input(f'\n\n{counter} совпадений найдено.\n\nНажмите Enter для выхода')

if __name__=='__main__':
    try:
        main()
    except Exception as e:
        print(e)
        input("Нажмите Enter для выхода")