"""
This script allows user to load the fine-tuned MVP model and generate the sentence from the input.

This script requires TextBox be installed in Backend within the Python
environment you are running this script in.

Please install TextBox according to the instructions in the following link: 
https://github.com/RUCAIBox/TextBox.

This file can also be imported as a module (used in Backend/app.py).
"""

import os
import sys
import torch

sys.path.append(os.path.join(os.getcwd(), 'TextBox'))

from accelerate import Accelerator
from TextBox.textbox.utils.utils import get_model, get_tokenizer
from TextBox.textbox.config.configurator import Config


# # need to move TextBox to Backend and change dir of checkpoint_best
# # export LD_LIBRARY_PATH="/root/anaconda3/envs/proj/lib:$LD_LIBRARY_PATH"
# def get_sentence(relation, sid):
#     file1 = open("./TextBox/dataset/str_data/test.src", "w")
#     file1.write(f"'{relation}' ")
#     file1.close()
#     filename = glob.glob(f"./TextBox/saved/{sid}/generation.txt")
#     if len(filename) != 0:
#         file1 = open(filename[0], "r")
#         sentence = file1.readline().strip()
#         file1.close()
#         return sentence
#     loadModel()
#     sentence = findAndRename(sid)
#     return sentence
#
#
# def loadModel():
#     os.system(
#         'cd TextBox ; python run_textbox.py --model=MVP --dataset=str_data --model_path=/root/Project/IPMN-07/Backend/model/checkpoint_best')
#
#
# def findAndRename(sid):
#     curr_folder = glob.glob("./TextBox/saved/MVP*")[0]
#     os.rename(curr_folder, f"./TextBox/saved/{sid}")
#     filename = glob.glob(f"./TextBox/saved/{sid}/generation.txt")[0]
#     file1 = open(filename, "r")
#     sentence = file1.readline().strip()
#     file1.close()
#     return sentence


class MVP:
    def __init__(self):
        self.config = Config('MVP', 'str_data', [], {})
        self.config.update({
            'model_path': os.path.join(os.getcwd(), 'model/checkpoint_best')
        })
        self.tokenizer = None
        # self.unwrap_model = None
        self.modelClass = None
        self.accelerator = None
        self._loadModel()

    # load the model when start up
    def _loadModel(self):
        from accelerate import DistributedDataParallelKwargs
        ddp_kwargs = DistributedDataParallelKwargs(find_unused_parameters=self.config['find_unused_parameters'])
        self.accelerator = Accelerator(
            gradient_accumulation_steps=self.config['accumulation_steps'], kwargs_handlers=[ddp_kwargs]
        )
        # print(config['model_path'])
        self.config.update({
            '_is_local_main_process': self.accelerator.is_local_main_process,
            'device': self.accelerator.device,
            'tokenizer_path': self.config['model_path']
        })
        self.tokenizer = get_tokenizer(self.config)
        self.modelClass = get_model(self.config['model_name'])(self.config, self.tokenizer).to(self.config['device'])

        self.accelerator.wait_for_everyone()
        unwrap_model = self.accelerator.unwrap_model(self.modelClass)
        unwrap_model.from_pretrained(self.config['model_path'])
        unwrap_model.tokenizer.from_pretrained(self.config['model_path'])

    # transfer triple sets to model input
    def genModelInput(self, tripleSets):
        s = "Describe the following data: " + ' [SEP] '.join(tripleSets)
        token = self.tokenizer(
            s,
            add_special_tokens=False,
            return_token_type_ids=False,
            return_attention_mask=False,
        )["input_ids"]
        ids = self.tokenizer.build_inputs_with_special_tokens(token)
        l = len(ids)
        inputs = {'source_text': [s],
                  'source_ids': torch.tensor([ids], dtype=torch.long),
                  'source_mask': torch.ones(1, l, dtype=torch.long),
                  'source_length': torch.tensor([l], dtype=torch.long),
                  'target_text': ['']}
        return inputs

    # generate sentence
    def generate(self, tripleSets):
        data = self.genModelInput(tripleSets)
        generated = self.accelerator.unwrap_model(self.modelClass).generate(data, self.accelerator)
        # print(generated)
        return generated[0]


if __name__ == '__main__':
    relation = ["documents | main subject | victim's credit card details", "that | main subject | victim's credit card details", "that | main subject | documents"]
    # sid = 12
    # print(get_sentence(relation, sid))
    m = MVP()
    print(m.generate(relation))