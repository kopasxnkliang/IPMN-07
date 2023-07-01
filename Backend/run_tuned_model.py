import os
import re
import glob

# need to move TextBox to Backend and change dir of checkpoint_best

def get_sentence(relation, sid):

    file1 = open("./TextBox/dataset/str_data/test.src", "w")
    file1.write(f"'{relation}' ")
    file1.close()
    filename = glob.glob(f"./TextBox/saved/{sid}/generation.txt")
    if len(filename) != 0:
        file1 = open(filename[0], "r")
        sentence = file1.readline().strip()
        file1.close()
        return sentence
    loadModel()
    sentence = findAndRename(sid)
    return sentence

def loadModel():
    os.system('cd TextBox ; python run_textbox.py --model=MVP --dataset=str_data --model_path=../IPMN-07/Backend/model/checkpoint_best')

def findAndRename(sid):
    curr_folder = glob.glob("./TextBox/saved/MVP*")[0]
    os.rename(curr_folder, f"./TextBox/saved/{sid}")
    filename = glob.glob(f"./TextBox/saved/{sid}/generation.txt")[0]
    file1 = open(filename, "r")
    sentence = file1.readline().strip()
    file1.close()
    return sentence


if __name__ == '__main__':
    relation = ["documents | main subject | victim's credit card details", "that | main subject | victim's credit card details", "that | main subject | documents"]
    sid = 12
    print(get_sentence(relation, sid))