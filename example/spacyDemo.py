from textblob import TextBlob
import spacy

example_str = "john was sentenced to seven years in prison for propping up the company's stock price and defrauding investors in two hedge funds he created."

exp1 = TextBlob(example_str)

# pip install spacy[cuda114] for GPU Farm
# if you want to use cuda, see https://spacy.io/usage
# python -m spacy download en_core_web_trf

nlp = spacy.load('en_core_web_trf')

exp2 = nlp(example_str)


print(exp1.noun_phrases)
for np in exp2.noun_chunks:
    print(np.text)