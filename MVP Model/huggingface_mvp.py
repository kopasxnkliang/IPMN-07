from transformers import MvpTokenizer, MvpForConditionalGeneration

tokenizer = MvpTokenizer.from_pretrained("RUCAIBox/mvp")
model = MvpForConditionalGeneration.from_pretrained("RUCAIBox/mvp-data-to-text")

inputs = tokenizer(
    # "Describe the following data: Iron Man | instance of | Superhero [SEP] Stan Lee | creator | Iron Man",
    "Describe the following data: John | identity | criminal suspect [SEP] crime | action | money laundering [SEP] crime | action | drug business [SEP] drug business | purpose | cash proceeds ",
    return_tensors="pt",
)
generated_ids = model.generate(**inputs, max_length=30)
print(tokenizer.batch_decode(generated_ids, skip_special_tokens=True))
