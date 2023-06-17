#!/bin/bash
#SBATCH --gres=gpu:1 --cpus-per-task=4 --mail-type=ALL

## sbatch run.sh
## scancel pid

gpu-interactive
. $HOME/anaconda3/etc/profile.d/conda.sh
# sbatch run.sh
conda activate qa_env
# train

python run_textbox.py --model=MVP --dataset=str_data --model_path=RUCAIBox/mvp-data-to-text
