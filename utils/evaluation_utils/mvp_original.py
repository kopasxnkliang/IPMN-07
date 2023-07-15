# MVP origial
# generate sentences using the original publicly available trained MVP model from huggingface

from transformers import MvpTokenizer, MvpForConditionalGeneration
from tqdm import tqdm

def testing(test_sen):
    tokenizer = MvpTokenizer.from_pretrained("RUCAIBox/mvp")
    model = MvpForConditionalGeneration.from_pretrained("RUCAIBox/mvp-data-to-text")

    sen = "Describe the following data: " + test_sen

    inputs = tokenizer(
        sen ,
        return_tensors="pt",
    )
    generated_ids = model.generate(**inputs, max_length=128)
    print(tokenizer.batch_decode(generated_ids, skip_special_tokens=True))


def generate_sentences(in_file, out_file):
    
    with open(in_file, "r") as f_in:
        input_data = f_in.read()

    input_data = input_data.split('\n')

    write_data = ""

    tokenizer = MvpTokenizer.from_pretrained("RUCAIBox/mvp")
    model = MvpForConditionalGeneration.from_pretrained("RUCAIBox/mvp-data-to-text")

    for prompts in tqdm(input_data):
        sen, generate_sen = "", ""
        sen = "Describe the following data: " + prompts[1:-1]

        inputs = tokenizer(
            sen,
            return_tensors="pt",
        )
        generated_ids = model.generate(**inputs, max_length=128)
        generate_sen = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        # print(generate_sen)
        write_data += generate_sen + '\n'
    
    with open(out_file, "w") as f_out:
        output_data = f_out.write(write_data[:-1])
    


def main():
    sen_1 = "Iron Man | instance of | Superhero [SEP] Stan Lee | creator | Iron Man"

    sen_2 = "John | identity | criminal suspect [SEP] crime | action | money laundering [SEP] crime | action | drug business [SEP] drug business | purpose | cash proceeds "
    # $500,000 was transferred from the Apple Bank account to the Pear Bank account on June 30th.
    sen_3 = "$500,000 | main subject | transaction amount [SEP] Apple Bank | main subject | account [SEP] Pear Bank | main subject | account [SEP] June 30th | transaction time | date"
    # The bank account of the Banana Inc. received multiple large-amount cross-border electronic remittances from unknown sources.
    sen_4 = '$20,000 | main subject | transaction amount [SEP] offshore companies | main subject | account [SEP] the Banana Inc | main subject | account [SEP] June 30th | transaction time | date'
    # 4 not good

    # Most of the funds were used to open a new account for Company A

    # Ken made $200,000 in illegal proceeds from smuggling tobacco. 
    # ['Ken was a criminal suspect in a crime action that netted $200,000 in illegal proceeds from smuggling tobacco.']
    sen_5 = 'Ken | member of | criminal suspect [SEP] $200,000 | main subject | illegal proceeds [SEP] smuggling tobacco | main subject | crime action'
    
    # Bob use offshore accounts and shell companies to avoid paying taxes
    # ['The use of offshore accounts and shell companies is one of the most common methods of tax evasion and crime action.']
    sen_6 = 'tax evasion | main subject | crime action [SEP] shell companies | main subject | crime method [SEP] offshore accounts | main subject | crime method'
    
    # Jim uses a third-party company to launder illicit funds 
    # ['A third-party company (also known as a "third party" or "third-party" company) is a type of criminal organization that is involved in illicit funds laundering.']
    sen_7 = 'third-party company | main subject | crime action [SEP] illicit funds laundering | main subject | purpose'

    # Ken bought Bitcoins to launder illicit proceeds from drug smuggling
    # ['Flower Bank is a crime body that uses bitcoin as a digital asset for the purpose of illicit proceeds laundering.']
    sen_8 = 'Flower Bank | instance of | crime body [SEP] Bitcoin | available for purchase | digital assets [SEP] illicit proceeds laundering | has part | crime purpose'

    testing(sen_8)


    # input_file = "./test.src"
    # output_file = "./generation.txt"
    # generate_sentences(input_file, output_file)


if __name__ == '__main__':
    main()
