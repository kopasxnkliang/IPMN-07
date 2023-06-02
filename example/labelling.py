# labelling.py 
# preprocess raw text data and generate our dataset by labelling entity relations within each sentence

import os
from dataclasses import dataclass
from textblob import TextBlob
import nltk
# nltk.download('brown')
# nltk.download('punkt')

import opennre
# relation extraction by NER result OpenNRE:https://github.com/thunlp/OpenNRE
model = opennre.get_model('wiki80_bert_softmax')


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
    return output_str.split(". ")


def get_noun_phrases(cleaned_str: list):
    dataset = []
    for idx, sen in enumerate(cleaned_str):
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


def generate_relations(dataset: list):
    # data = dataset
    for text_data in dataset:
        for i in range(len(text_data.entityIdx)):
            for j in range(i+1,len(text_data.entityIdx)):
                res1 = model.infer({'text': text_data.sentence, 'h': {'pos': text_data.entityIdx[i][1]}, 't': {'pos': text_data.entityIdx[j][1]}})
                res2 = model.infer({'text': text_data.sentence, 'h': {'pos': text_data.entityIdx[j][1]}, 't': {'pos': text_data.entityIdx[i][1]}})
                # choose the one with larger confidence
                if res1[1]>res2[1]:
                    text_data.relations.append([text_data.entityIdx[i][0], res1[0], text_data.entityIdx[j][0]])
                else:
                    text_data.relations.append([text_data.entityIdx[j][0], res2[0], text_data.entityIdx[i][0]])
    
    return dataset


def main():

    example_str = "John, operates an illicit drug business and generates substantial cash proceeds. To conceal the illegal origins of the funds, John sets up a front business, a seemingly legitimate retail store. He commingles the drug profits with the store's revenue, creating a complex web of transactions, fake invoices, and inflated sales. By doing so, John disguises the illicit funds as legitimate business income, effectively laundering the money and making it difficult for law enforcement to trace its source."
    sen_list = split_sentences(example_str)
    dataset_without_relation = get_noun_phrases(sen_list)
    # print(dataset_without_relation[0].entityIdx)
    dataset_with_relation = generate_relations(dataset_without_relation)
    print(dataset_with_relation[-1].relations)
    


if __name__ == '__main__':
    main()
