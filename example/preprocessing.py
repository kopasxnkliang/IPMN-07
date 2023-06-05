# preprocessing.py
# prepare raw string list data

import os
import csv
import json
from io import StringIO
import pandas as pd
from tqdm import tqdm

from datasets import load_dataset

from labelling import get_noun_phrases, create_xml
from labelling import generate_relations


def simple_filtering(input_str):
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
    output_str = output_str.replace("%", "percent")
    output_str = output_str.replace("&", " and ")
    return output_str


def read_csv(filename):
    """read csv data from /dataset/kaggle_csv/all-data.csv and return a list of rnd data"""
    with open(file=filename, mode='r') as f:
        data = f.read()
    raw_data = []
    string_data = data.split('\n')
    for line in string_data:
        if "neutral" in line.split(",")[0]:
            text = line.split("neutral,")[1]
        elif "negative" in line.split(",")[0]:
            text = line.split("negative,")[1]
        else:
            text = line.split("positive,")[1]
        if '"' == text[0]:
            text = text[1:-1]
        text = simple_filtering(text)
        raw_data.append(text)
    return raw_data


def generate_financial_phrase_raw_dataset():
    raw_financial_phrase_bank_data = read_csv("../../datasets/kaggle_csv/all-data.txt")
    dataset_without_relation = get_noun_phrases(raw_financial_phrase_bank_data[:10])
    dataset_with_relation = generate_relations(dataset_without_relation)
    # print(dataset_with_relation)
    # no good results 


def read_from_json(filepath, filename):
    with open(os.path.join(filepath, filename), "r") as f:
        raw_data = json.load(f)
    df_tag = pd.read_csv(StringIO(raw_data['tag.txt']), sep='\t', na_filter=False)
    return list(df_tag['doc'])


def filtering_fs(text_list):
    
    output_list = []
    for sentences in text_list:
        # split sentences
        sen_list = [each+'.' for each in sentences.split('. ')[:-1]]
        output_list.extend(sen_list)
    return output_list


def generate_financial_statement_raw_dataset():
    json_file_list = ['2015q4.json', '2016q2.json', '2017q1.json', '2016q3.json', '2016q1.json', '2015q3.json', '2017q2.json', '2016q4.json']
    dataset_path = "../../datasets/kaggle_json"
    txt_path = "../../datasets/kaggle_txt"
    raw_text_data = {}
    for json_file in tqdm(json_file_list[:1]):
        raw_text_data[json_file] = read_from_json(dataset_path, json_file)
        raw_text_data[json_file] = filtering_fs(raw_text_data[json_file])

    # print(raw_text_data['2015q4.json'][:3])
    # print(len(raw_text_data['2015q4.json']))
    dataset_without_relation = get_noun_phrases(raw_text_data['2015q4.json'][:1000])
    dataset_with_relation = generate_relations(dataset_without_relation)
    # print(len(dataset_with_relation))
    create_xml(os.path.join(txt_path, '2015q4.xml'), dataset_with_relation)

    # with open(os.path.join(txt_path, '2015q4.txt'), "w") as f:
    #     f.write(str(dataset_with_relation))
    # print(dataset_with_relation)
    return


def generate_trade_event():
    xml_path = "../../datasets/xmls"
    dataset = load_dataset("nickmuchi/trade-the-event-finance")
    print(dataset)
    # dataset_with_relation = generate_relations(dataset_without_relation)
    # create_xml(os.path.join(xml_path, 'trade_event.xml'), dataset_with_relation)
    return


def main():
    # 1 financial phrase rank: results of relation extraction are not as good as expected
    # generate_financial_phrase_raw_dataset()
    # 2 financial statement
    generate_financial_statement_raw_dataset()
    # 3 trade the event finance:
    # generate_trade_event()



if __name__ == '__main__':
    main()
