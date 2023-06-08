
# paraphrase.py


import os
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer



def paraphrase(text_list, num_return_sequences=2, num_beams=5):
    model_name = 'tuner007/pegasus_paraphrase'
    torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
    generated_data = []
    for input_text in text_list:
        tgt_text = []
        batch = tokenizer([input_text],truncation=True,padding='longest',max_length=60, return_tensors="pt").to(torch_device)
        translated = model.generate(**batch,max_length=60,num_beams=num_beams, num_return_sequences=num_return_sequences, temperature=1.5)
        tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
        generated_data.extend(tgt_text)
    return generated_data


def main():
    example = ["a tinyurl link takes users to a scamming site promising that users can earn thousands of dollars by becoming a google ( nasdaq , goog ) cash advertiser "]
    output_sens = paraphrase(text_list=example)
    print(output_sens)


if __name__ == "__main__":
    main()
