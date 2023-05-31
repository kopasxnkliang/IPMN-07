example = "John, operates an illicit drug business and generates substantial cash proceeds. To conceal the illegal origins of the funds, John sets up a front business, a seemingly legitimate retail store. He commingles the drug profits with the store's revenue, creating a complex web of transactions, fake invoices, and inflated sales. By doing so, John disguises the illicit funds as legitimate business income, effectively laundering the money and making it difficult for law enforcement to trace its source."
example = [each+'.' for each in example.split('.')[:-1]]
# 原字符串这里不能转成全小写
# step1. nouns recognition
# from transformers import pipeline

# pipe = pipeline('ner', model="hadifar/entityextraction")
# ans = pipe(example)
# print(ans)

from textblob import TextBlob
blob = TextBlob(example[0])
print(blob.noun_phrases)
entityIdx = []
# 转换成小写否则查不到id
t = example[0].lower()
for each in blob.noun_phrases:
    i = t.find(each)
    j = i+len(each)
    entityIdx.append([each, (i,j)])
print(entityIdx)

# step2. relation extraction by NER result OpenNRE:https://github.com/thunlp/OpenNRE
import opennre
model = opennre.get_model('wiki80_bert_softmax')
print()
for i in range(len(entityIdx)):
    for j in range(i+1,len(entityIdx)):
        res1 = model.infer({'text': example[0], 'h': {'pos': entityIdx[i][1]}, 't': {'pos':entityIdx[j][1]}})
       
        res2 = model.infer({'text': example[0], 'h': {'pos': entityIdx[j][1]}, 't': {'pos':entityIdx[i][1]}})
        
        # choose larger confidence one
        if res1[1]>res2[1]:
            print(entityIdx[i][0],res1,entityIdx[j][0])
        else:
            print(entityIdx[j][0],res2,entityIdx[i][0])