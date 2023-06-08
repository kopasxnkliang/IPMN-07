# labelling.py 
# preprocess raw text data and generate our dataset by labelling entity relations within each sentence

import os
import string
from dataclasses import dataclass
from textblob import TextBlob
import nltk
# nltk.download('brown')
# nltk.download('punkt')
from tqdm import tqdm
import opennre

import xml.etree.ElementTree as ET



def create_xml(filename, dataset, comment="STR"):
    root = ET.Element('benchmark')
    entries = ET.SubElement(root, 'entries')
    print("Generating XML file ...")
    for each in tqdm(dataset):
        if len(each.relations) == 0:
            continue
        entry = ET.SubElement(entries, 'entry', category="MISC", eid=str(each.idx), size=str(len(each.relations)))
        modifiedtripleset = ET.SubElement(entry, 'modifiedtripleset')
        for tripleset in each.relations:
            mtriple = ET.SubElement(modifiedtripleset, 'mtriple')
            mtriple.text = f"{tripleset[0]} | {tripleset[1]} | {tripleset[2]}"
        lex = ET.SubElement(entry, 'lex', comment="STR", lid=str(each.idx), size='1')
        lex.text = each.sentence
    pretty_xml(root, '\t', '\n')
    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

    return


def pretty_xml(element, indent, newline, level=0):
    if element:
        if (element.text is None) or element.text.isspace(): 
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    temp = list(element)
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):
            subelement.tail = newline + indent * (level + 1)
        else:
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)


@dataclass
class TextData:
    idx: int
    sentence: str
    entityIdx: list
    relations: list


def split_sentences(input_str: str) -> str:
    output_str = input_str.replace("?", ".")
    output_str = output_str.strip("`")
    output_str = output_str.strip("'")
    output_str = output_str.strip('"')
    output_str = output_str.replace("+", " ")
    output_str = output_str.replace("!", ".")
    output_str = output_str.replace(";", ",")
    output_str = output_str.replace(":", ",")
    output_str = output_str.replace("--", ",")
    output_str = output_str.replace("-", ",")
    output_str = output_str.replace("%", " percent")
    output_str = output_str.replace("&", " and")
    output_str = output_str.replace("\\", " ")
    output_str = output_str.replace('[{}]'.format(string.punctuation), '')
    return output_str.split(". ")


def get_noun_phrases(cleaned_str: list):
    dataset = []
    print("Extracting noun phrases ...")
    for idx, sen in tqdm(enumerate(cleaned_str)):
        blob = TextBlob(sen)
        entityIdx = []
        t = sen.lower()
        for each in blob.noun_phrases:
            i = t.find(each)
            j = i + len(each)
            entityIdx.append([each, (i,j)])
        data = TextData(idx=idx, sentence=sen, entityIdx=entityIdx, relations=[])
        dataset.append(data)
    
    return dataset


def generate_relations(dataset: list, threshold=0.70):
    # relation extraction by NER result OpenNRE:https://github.com/thunlp/OpenNRE
    model = opennre.get_model('wiki80_bert_softmax')
    new_dataset = []
    print("Extracting relations ...")
    for text_data in tqdm(dataset):
        empty_flag = True
        if len(text_data.entityIdx) == 0:
            continue
        for i in range(len(text_data.entityIdx)):
            for j in range(i+1,len(text_data.entityIdx)):
                res1 = model.infer({'text': text_data.sentence, 'h': {'pos': text_data.entityIdx[i][1]}, 't': {'pos': text_data.entityIdx[j][1]}})
                res2 = model.infer({'text': text_data.sentence, 'h': {'pos': text_data.entityIdx[j][1]}, 't': {'pos': text_data.entityIdx[i][1]}})
                # check if the confidence is larger than threshold
                if float(max(res1[1], res2[1])) <= threshold:
                    continue
                # check if A == B:
                if text_data.entityIdx[i][0] == text_data.entityIdx[j][0]:
                    continue
                # check if the relation is already appended in the relation list
                if [text_data.entityIdx[i][0], res1[0], text_data.entityIdx[j][0]] in text_data.relations or [text_data.entityIdx[j][0], res2[0], text_data.entityIdx[i][0]] in text_data.relations:
                    continue
                # choose the one with larger confidence
                if res1[1] > res2[1]:
                    text_data.relations.append([text_data.entityIdx[i][0], res1[0], text_data.entityIdx[j][0]])
                else:
                    text_data.relations.append([text_data.entityIdx[j][0], res2[0], text_data.entityIdx[i][0]])
                empty_flag = False
        if not empty_flag:
            new_dataset.append(text_data)
    
    return new_dataset


def main():

    example_str = "John, operates an illicit drug business and generates substantial cash proceeds. To conceal the illegal origins of the funds, John sets up a front business, a seemingly legitimate retail store. He commingles the drug profits with the store's revenue, creating a complex web of transactions, fake invoices, and inflated sales. By doing so, John disguises the illicit funds as legitimate business income, effectively laundering the money and making it difficult for law enforcement to trace its source."
    sen_list = split_sentences(example_str)
    dataset_without_relation = get_noun_phrases(sen_list)
    # print(dataset_without_relation[0].entityIdx)
    dataset_with_relation = generate_relations(dataset_without_relation)
    print(dataset_with_relation[-1].relations)

    # Todo: label analysis and selectioin

    # Todo: transform the dataset with labels into XML file
    create_xml("example.xml", dataset_with_relation)

    


if __name__ == '__main__':
    main()
