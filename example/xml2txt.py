# xml2txt.py
# transform xml file to txt(.src / .tgt)

import os
# import xml.etree.ElementTree as ET
from lxml import etree
# from xml.dom import minidom
from tqdm import tqdm
# from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split


def write_mtriples(folder_path, dataset_name, mtriples, adds="_mtriples.txt"):
    with open(os.path.join(folder_path, dataset_name+adds), "w") as f:
        write_data = ""
        for mtri in mtriples:
            write_data += f"'{mtri}'\n"
        f.write(write_data[:-1])

def write_sentences(folder_path, dataset_name, sentences, adds="_sentences.txt"):
    with open(os.path.join(folder_path, dataset_name+adds), "w") as f:
        write_data = ""
        for sen in sentences:
            write_data += str(sen[0])+"\n"
        f.write(write_data[:-1])

def write_txt(folder_path, dataset_name, mtriples, sentences, split=False):
    folder = os.path.exists(folder_path)
    if not folder: 
        os.makedirs(folder_path) 

    if not split:
        write_mtriples(folder_path, dataset_name, mtriples)
        write_sentences(folder_path, dataset_name, sentences)
        
    else:
        X_trainval, X_test, y_trainval, y_test = train_test_split(mtriples, sentences, test_size=0.1, random_state=42)
        write_mtriples(folder_path, dataset_name="test", mtriples=X_test, adds=".src")
        write_sentences(folder_path, dataset_name="test", sentences=y_test, adds=".tgt")
        X_train, X_val, y_train, y_val = train_test_split(X_trainval, y_trainval, test_size=0.12, random_state=42)
        write_mtriples(folder_path, dataset_name="train", mtriples=X_train, adds=".src")
        write_sentences(folder_path, dataset_name="train", sentences=y_train, adds=".tgt")
        write_mtriples(folder_path, dataset_name="valid", mtriples=X_val, adds=".src")
        write_sentences(folder_path, dataset_name="valid", sentences=y_val, adds=".tgt")
        


def list2str(str_list):
    str_list = [xx for xx in str_list if xx[0] != '.']
    separator = ' [SEP] '
    output = separator.join(str_list)
    return output


def formatting(ori_folder_path, xml_file, dst_folder_path):

    tree = etree.parse(os.path.join(ori_folder_path, xml_file))
    root = tree.getroot()

    N_entry = len(root.xpath('//entry'))

    mtriple_list, sentence_list = [], []
    for i in tqdm(range(1, N_entry+1)):
        mtriples = list2str(root.xpath(f'//entry[{i}][contains(@category, "MISC")]/modifiedtripleset/mtriple/text()'))
        mtriple_list.append(mtriples)
        sen = root.xpath(f'//entry[{i}]/lex/text()')[0]
        if ' ' == sen[0]:
            sentence_list.append([sen[1:]])
        else:
            sentence_list.append([sen])
    
    # print(sentence_list)
    # write_txt(folder_path=dst_folder_path, dataset_name="STR", mtriples=mtriple_list, sentences=sentence_list)

    # if train-val-test split
    write_txt(folder_path=dst_folder_path, dataset_name="STR", mtriples=mtriple_list, sentences=sentence_list, split=True)
    # else:
    # write_txt(folder_path=dst_folder_path, dataset_name="STR", mtriples=mtriple_list, sentences=sentence_list, split=False)




def main():
    xml_file = 'STR_data.xml'  # datasets/xmls/STR_data.xml
    ori_folder_path = '../../datasets/xmls/'
    dst_folder_path = '../../datasets/str_data/'
    formatting(ori_folder_path, xml_file, dst_folder_path)


if __name__ == '__main__':
    main()

