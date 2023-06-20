
# visualization.py
# visualize training process

import os
from torch.utils.tensorboard import SummaryWriter


def visualize(logfile):
    with open(logfile, 'r') as f:
        data = f.read()
    sen_list = data.split("\n")

    writer = SummaryWriter()

    for sen in sen_list:
        # if "2023" not in sen or len(sen) < 2:
        #     continue
        # if "WARNING" in sen:
        #     continue
        if "INFO" not in sen or "WARNING" in sen:
            continue
        if "Train epoch" in sen:
            n_iter = int(sen.split("Train epoch")[1].split(" ")[2])
            train_loss = float(sen.split("loss")[1].split(" ")[1][:-1])
            writer.add_scalar('Train/Loss', train_loss, n_iter)
        elif "Validation" in sen:
            validation_data = sen.split("Validation")[1]
            n_iter = int(validation_data.split(" ")[2])
            score_list = validation_data.split("score:")[1].split(" ")
            # print(score_list)
            sum_score = float(score_list[1][:-1])
            bleu_score = float(score_list[3][:-2])
            rouge2_score = float(score_list[7][:-2])
            meteor_score = float(score_list[11][:-2])
            # print(sum_score, bleu_score, rouge2_score, meteor_score)
            writer.add_scalars(f"Validation_Scores", {'Sum Score': sum_score, "BLEU": bleu_score, "ROUGE2": rouge2_score, "METEOR": meteor_score}, n_iter)

            writer.add_scalar('Validation/Sum Score', sum_score, n_iter)
            writer.add_scalar('Validation/BLEU', bleu_score, n_iter)
            writer.add_scalar('Validation/ROUGE2', rouge2_score, n_iter)
            writer.add_scalar('Validation/METEOR', meteor_score, n_iter)


        # writer.add_scalar('Loss/train', np.random.random(), n_iter)
        


def main():
    log_file = "../checkpoint_best_3e-5/project.log"
    visualize(log_file)


if __name__ == '__main__':
    main()

