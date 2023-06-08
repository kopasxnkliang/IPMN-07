# preprocessing.py
# prepare raw string list data

import os
import csv
import json
import string
from io import StringIO
import pandas as pd
from tqdm import tqdm

from datasets import load_dataset

from labelling import get_noun_phrases, create_xml
from labelling import generate_relations


dataset_path = "../../datasets/kaggle_json"
txt_path = "../../datasets/kaggle_txt"
xml_path = "../../datasets/xmls"

important_words = ['laundering', 'launder', 'scam', 'scammer', 'fraud', 'transaction', 'illegal', 'illicit',
                    'criminal group', 'crime', 'crimes', 'criminal', 'terrorism', 'terrorist', 'financial',
                    'trafficking', 'terrorist financing', 'sexual exploitation', 'migrant smuggling', 'smuggle' \
                    'human trafficking', 'terrorists', 'child', 'children', 'sex', 'arms', 'stealing', 'steal', \
                    'stole', 'stealing', 'goods stolen', 'other goods', 'corruption', 'corrupt', 'bribery', \
                    'corrupted', 'corrupts', 'bribe', 'briberies', 'frauds', 'email', 'emails', 'email scam', \
                    'investment', 'invests', 'invest', 'invest scam', 'narcotic drugs', 'drug', 'drugs', \
                    'psychotropic', 'psychotropic substances', 'romance scam', 'romance', 'deceive', 'deception', \
                    'telephone', 'call', 'telecom', 'internet', 'currency', 'counterfeiting currency', 'environment', 
                    'environmental', 'piracy', 'product', 'products', 'murder', 'grievous', 'injuries', 'injury', 'hurt', \
                    'kidnapping', 'illegal restraint', 'restraint', 'hostage', 'hostage-taking', 'robbery', 'theft', \
                    'tax', 'taxes', 'custom', 'customs', 'extortion', 'forgery', 'forgeries', 'insider', 'trade', \
                    'trading', 'market', 'dollar', 'Manipulation', 'suspicious', 'suspected', 'report', 'amount', \
                    'dollar', 'organized', 'racketeer', 'fund', 'movement', 'trail', 'audit', 'pattern', 'intended', \
                    'break', 'indirect', 'direct', 'uneconomical', 'business', 'temporary', 'repository', 'finance', \
                    'financial', 'pep', 'customer', 'risk', 'cash', 'region', 'jurisdiction', 'cause', 'counterparty', \
                    'counterparties', 'companies', 'shell', 'fake', 'account', 'third party', 'party', 'personal', \
                    'holder', 'offshore', 'resident', 'nonresident', 'indicators', 'background', 'incommensurate', \
                    'unlicensed', 'service', 'operator', 'money', 'secure', 'security', 'coupon', 'securities', \
                    'bank', 'banks', 'stock', 'political', 'politically exposed person', 'courier', 'evasive', 'reluctant', \
                    'information', 'investigate', 'document', 'file', 'casino', 'charitable', 'organization', 'NPO', \
                    'questioned', 'source', 'destination', 'phone', 'address', 'transfer', 'transact', 'transaction', \
                    'entity', 'evasive', 'passive', 'background', 'human', 'person', 'period', 'balance', 'institution', \
                    'date', 'role', 'related', 'connected', 'connection', 'relation', 'link', 'area','oversea', 'overseas', \
                    'nature', 'incorporation', 'corporation', 'nation', 'law', 'disclosure', 'ordinance']

important_words_matching = ['laundering', 'launder', 'scam', 'scammer', 'fraud', 'illegal', 'illicit',
                    'criminal group', 'crime', 'criminal', 'terrorism', 'terrorist', 
                    'trafficking', 'terrorist financing', 'sexual exploitation', 'migrant smuggling', 'smuggle' \
                    'human trafficking', 'terrorists', 'child', 'sex', 'arms', 'stealing', 'steal', \
                    'stole', 'stealing', 'goods stolen', 'corrupt', 'bribery', \
                    'corrupted', 'corrupts', 'bribe', 'briberies', 'email scam', \
                    'invest scam', 'narcotic drugs', 'drug', 'drug dealing', \
                    'psychotropic', 'psychotropic substances', 'romance scam', 'romance', 'deceive', 'deception', \
                    'telephone scam', 'phone scam', 'internet scam', 'counterfeiting currency', 'environmental crime', 
                    'piracy', 'illegal product', 'murder', 'grievous bodily injury', 'injuries', 'body injury', \
                    'kidnapping', 'illegal restraint', 'restraint', 'hostage', 'hostage-taking', 'robbery', 'theft', \
                    'excise taxes', 'excise duties', 'extortion', 'forgery', 'forgeries', \
                    'manipulation', 'suspicious', 'suspected', 'Terrorist Financing', \
                    'organized crime', 'racketeer', 'illegal fund', 'movement', \
                    'indirect tax', 'uneconomical', 'third Party Laundering', \
                    'pep', 'risk investment', 'jurisdiction', 'counterparty', \
                    'counterparties', 'shell company', 'shell companies', 'fake account', 'fake identity', 'controlled by third party',  \
                    'offshore company', 'nonresident', 'incommensurate', 'operated by third party',\
                    'unlicensed', 'insecure', 'insecurity', \
                    'political', 'politically exposed person', 'courier', 'evasive', 'reluctant', \
                    'casino', 'charitable', 'npo', \
                    'questioned','evasive', 'passive', 'cyber crime', 'cybercrime' \
                    'oversea company', 'insider trading', 'weapon', 'gun', \
                    'violate law', 'violate ordinance']



def check_important_words_matching(sentence):
    for word in important_words_matching:
        if word in sentence:
            return True
    return False


def check_important_words(sentence):

    word_list = sentence.split(' ')
    for word in important_words:
        if word in word_list:
            return True
    return False

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
    output_str = output_str.replace("—", ",")
    output_str = output_str.replace("%", " percent")
    output_str = output_str.replace("&", " and ")
    output_str = output_str.replace('[{}]'.format(string.punctuation), '')
    output_str += '.'
    return output_str.lower()


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


def read_from_json(filepath, filename):
    with open(os.path.join(filepath, filename), "r") as f:
        raw_data = json.load(f)
    df_tag = pd.read_csv(StringIO(raw_data['tag.txt']), sep='\t', na_filter=False)
    return list(df_tag['doc'])


def write_txt(filename, list_data):
    print(f"Writing {len(list_data)} pieces of text data to {os.path.join(xml_path, filename)} ... ")
    with open(os.path.join(xml_path, filename), "w") as f:
        f.write(str(list_data))


def filtering_fs(text_list):
    
    output_list = []
    for sentences in text_list:
        # split sentences
        sen_list = [each+'.' for each in sentences.split('. ')[:-1]]
        output_list.extend(sen_list)
    return output_list


def generate_financial_phrase_raw_dataset():
    raw_financial_phrase_bank_data = read_csv("../../datasets/kaggle_csv/all-data.txt")

    dataset_without_relation = get_noun_phrases(raw_financial_phrase_bank_data[:10])
    dataset_with_relation = generate_relations(dataset_without_relation)
    # print(dataset_with_relation)
    # no good results 


def generate_financial_statement_raw_dataset():
    json_file_list = ['2015q4.json', '2016q2.json', '2017q1.json', '2016q3.json', '2016q1.json', '2015q3.json', '2017q2.json', '2016q4.json']
    raw_text_data = {}
    total_text_data = []
    for json_file in tqdm(json_file_list):
        raw_text_data[json_file] = read_from_json(dataset_path, json_file)
        raw_text_data[json_file] = filtering_fs(raw_text_data[json_file])
        text_data = []
        for text in tqdm(raw_text_data[json_file]):
            text = simple_filtering(text)
            sen_list = text.split(".")
            for sen in sen_list:
                if len(sen.split(' ')) <= 10:
                    continue
                if "/" in sen or ",," in sen or "…" in sen or "[]" in sen or '\n' in sen or '\t' in sen:
                    continue 
                if check_important_words_matching(sen):
                    text_data.append(sen)
        total_text_data.extend(text_data)

        # generate XML files separately
        # txt_filename = json_file.split('.')[0] + '.txt'
        # with open(os.path.join(xml_path, txt_filename), "w") as f:
        #     f.write(str(text_data))  


        # dataset_without_relation = get_noun_phrases(raw_text_data[json_file])
        # dataset_with_relation = generate_relations(dataset_without_relation)
        
        # xml_filename = json_file.split('.')[0] + '.xml'
        # create_xml(os.path.join(xml_path, xml_filename), dataset_with_relation)

    # remove duplicates
    total_text_data = list(dict.fromkeys(total_text_data))
    
    txt_filename = 'financial_statements.txt'
    write_txt(txt_filename, total_text_data)
    
    dataset_without_relation = get_noun_phrases(total_text_data)
    dataset_with_relation = generate_relations(dataset_without_relation)

    xml_filename = 'financial_statements.xml'
    create_xml(os.path.join(xml_path, xml_filename), dataset_with_relation)

    return


def generate_trade_event_dataset():
    xml_path = "../../datasets/xmls"
    dataset = load_dataset("nickmuchi/trade-the-event-finance")
    print(dataset)
    # dataset_with_relation = generate_relations(dataset_without_relation)
    # create_xml(os.path.join(xml_path, 'trade_event.xml'), dataset_with_relation)
    return


def generate_news_finance_dataset():
    xml_path = "../../datasets/xmls"
    dataset = load_dataset("PaulAdversarial/all_news_finance_sm_1h2023")
    text_list = dataset['train']['description']
    text_data = []
    print(len(text_list))
    for text in tqdm(text_list):
        text = simple_filtering(text)
        sen_list = text.split(".")
        for sen in sen_list:
            if len(sen.split(' ')) <= 10:
                continue
            if "/" in sen or ",," in sen or "…" in sen or "[]" in sen or '\n' in sen or '\t' in sen:
                continue 
            if check_important_words_matching(sen):
                text_data.append(sen)
    print(len(text_data))
    with open(os.path.join(xml_path, 'news_finance.txt'), "w") as f:
        f.write(str(text_data))
    dataset_without_relation = get_noun_phrases(text_data)
    dataset_with_relation = generate_relations(dataset_without_relation)
    # print(len(dataset_with_relation))
    # create_xml(os.path.join(xml_path, 'news_finance.xml'), dataset_with_relation)


def main():
    # 1 financial phrase rank: results of relation extraction are not as good as expected
    # generate_financial_phrase_raw_dataset()

    # 2 financial statement -> 55 sentences datasets/xmls/financial_statements.txt
    generate_financial_statement_raw_dataset()

    # 3 trade the event finance: 
    # generate_trade_event_dataset()
    
    # 4 news finance
    # generate_news_finance_dataset()

    # dataset5 = load_dataset("JanosAudran/financial-reports-sec", "large_lite")

    # dataset4 = load_dataset("nlpaueb/finer-139", split="train")


if __name__ == '__main__':
    main()
