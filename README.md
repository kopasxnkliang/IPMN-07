# IPMN-07

### Our Project
To fine-tune a data-to-text generation model for generating descriptive sentences from input keywords in order to help investigators to prepare STR reports.
1. Prepare the STR dataset (data collection, filtering, label generating and EDA)
2. Fine-tune a data-to-text-generation model (fine-tuning, parameter-tuning, quantitave & qualitative evaluation)
3. Report with detailed analyis

#### Basic Project Framwork
<img src="https://github.com/kopasxnkliang/IPMN-07/blob/main/figures/Proposal2.0.png" alt="alt text" width="600" height="480">

#### STR data collection and preparation
<img src="https://github.com/kopasxnkliang/IPMN-07/blob/main/figures/datacollections.png" alt="alt text" width="480" height="400">

#### Train Loss
<img src="https://github.com/kopasxnkliang/IPMN-07/blob/main/figures/train_loss.png" alt="alt text" width="480" height="400">

#### Generation Score
<img src="https://github.com/kopasxnkliang/IPMN-07/blob/main/figures/generation_score.png" alt="alt text" width="480" height="400">

#### Before and After Fine-tuning
<img src="https://github.com/kopasxnkliang/IPMN-07/blob/main/figures/comparion_results.png" alt="alt text" width="480" height="400">

#### Parameters Tuning
<img src="https://github.com/kopasxnkliang/IPMN-07/blob/main/figures/parameter_tuning.png" alt="alt text" width="480" height="400">

#### Compariosn Results
<img src="https://github.com/kopasxnkliang/IPMN-07/blob/main/figures/comparison_result_1.png" alt="alt text" width="480" height="400">
<img src="https://github.com/kopasxnkliang/IPMN-07/blob/main/figures/comparison_result_4.png" alt="alt text" width="480" height="400">

### Installation Procedures for Fine-tuning and Evaluation

1. Download the code folders (utils and TextBox) from the Google Drive link listed in our project report. Our raw data and processed dataset are available and saved in TextBox/dataset. The file structure of ./utils is as follow:
   
```
├── preprocessing_utils
    ├── labelling.py
    ├── mergeXML.py
    ├── paraphrase.py
    ├── preprocessing.py
    └── xml2txt.py
├── evaluation_utils
    ├── mvp_original.py
    └── visualization.py
└── readme.md
```
Folder ./utils/preprocessing_utils contains python scripts to transform raw data to dataset used to fine-tune the model. paraphrase.py uses trained text-to-text generation model https://huggingface.co/tuner007/pegasus_paraphrase created by Arpit Rajauria to enlarge our STR dataset, and it is called by preprocessing.py. Functions in labelling.py are also called by preprocessing.py to create labels

Folder ./utils/evaluation_utils includes python scripts for result visualization and comparison.

2. Download the fine-tuned model (Best Fine-tuned Model) from Google Drive link listed in our project report and copy the model folder to ./TextBox/saved/<Checkpoint_best>. The ./TextBox file structure is as follow:

```
├── asset
├── dataset
    ├── *STR_data.xml
    └── *str_data
	├── train.src
	├── train.tgt
	├── valid.src
	├── valid.tgt
	├── test.src
	└── test.tgt 
├── instructions
├── saved
     └── *<Checkpoint_best>
	├── pytorch_model.bin
	├── added_token.json
	├── config.json
	├── generation.txt
	├── project.log
	├── pytorch_model.bin
	├── special_tokens_map.json
	├── optimizer.pt
	├── textbox_configuration.json
	├── tokenizer.json
	├── tokenizer_config.json
	└── vocab.json
├── packages
├── textbox
    ├── config
    ├── data
    ├── evaluator
    ├── model
    ├── properties
	├── overall.yaml
	└── dataset
	    └── *str_data.yaml
    ├── quick_start
    ├── trainer
    └── utils
├── *run.sh
└── run_textbox.py
```

The filenames or foldernames with the star(*) sign are the files that we add and edit, and they were not in original TextBox folder. 

3. Install TextBox according to https://github.com/RUCAIBox/TextBox. Additional packages are listed in requirements.txt in folder ./TextBox.
```
conda create -n <your_env_name> python=3.8
conda activate <your_env_name>
cd <your_folder_path_to_TextBox>
bash install.sh
pip install -r requirements.txt
```
After successfully installing TextBox, run the following python scripts in the same terminal in the same `<your_env_name>` conda environment. 
```
python
import nltk
nltk.download('brown')
nltk.download('punkt')
```

4. Before fine-tuning the original MVP-data-to-text model, check the parameter setting including the learning rate, batch size, evaluation metrics and other essential parameters in ./TextBox/textbox/properties/overall.yaml and ./TextBox/textbox/properties/dataset/str_data.yaml. Also, check if the remaining disk storage is larger than 10GB because while fine-tuning the pretrained model, the latest fine-tuned model as well as the best fine-tuned model will be saved in the ./TextBox/saved/STR_data_<start_training_time>. The best fine-tuned model is selected by the highest generation score, which sums up the selected evaluation metrics. The metrics include: bleu, rouge-1, rouge-2, rouge-l and meteor. These metrics can be assigned in <dataset_name>.yaml in the same folder as the str_data.yaml.

Besides, adjusting batch size according to the GPU memory. For a single RTX 2080 Ti with 12GB GPU memory, the batch size for training is limited to 2, while eval batch size can only be set as 1. For a single RTX 3090 with 24GB GPU memory, the training and evaluation batch size can be set as 20 and 10, respectively.

To fine-tune a new MVP-data-to-text model, run
```
cd TextBox
conda activate <your_env_name>
python run_textbox.py --model=MVP --dataset=str_data --model_path=RUCAIBox/mvp-data-to-text
```
TextBox will automatically create a folder in ./TextBox/saved/STR_data_<start_training_time> and save all generated config file and model weights.

To resume fine-tuning process using an existing fine-tuned model, run
```
python run_textbox.py --model=MVP --dataset=str_data --model_path=<fine-tuned_model_folder_path>
```

5. To quantitatively evaluate the generation ability of the original MVP-data-to-text model on a specific dataset, set learning rate=0 in ./TextBox/textbox/properties/dataset/<dataset_name>.yaml and set epochs=1 in the same <dataset_name>.yaml. Run the following command in terminal. 
```
python run_textbox.py --model=MVP --dataset=<dataset_name> --model_path=RUCAIBox/mvp-data-to-text
```
Evaluation result will be listed in ./TextBox/textbox/<dataset_name>_<start_time>/project.log

6. To evaluate a fine-tuned model, editions are needed. In ./TextBox/textbox/quick_start/experiment.py, comment line 142 & 144
```
	            # self._do_train_and_valid()
	            self._do_test()
	            # self._on_experiment_end()
```
And comment line 502 in ./TextBox/textbox/trainer/trainer.py and add following line in the next line.
```
checkpoint_dir = <the_absolute_file_path_of_the_fine-tuned_model>
```
Run following command and the evaluation result will be shown in ./TextBox/textbox/<dataset_name>_<start_time>/project.log
```
python run_textbox.py --model=MVP --dataset=<dataset_name> --model_path=<fine-tuned_model_folder_path>
```
### Installation Procedures for the Back-end:
#### structure of the utils folder
```
├── app.py
├──model
    └── checkpoint_best
├── README.md
├── run_tuned_model.py
└── TextBox
```

#### Requirements
    TextBox (https://github.com/RUCAIBox/TextBox)
    Flask (https://github.com/pallets/flask)

#### Installation
    1. Clone IPMN-07 project
    2. cd ./Backend 
    3. Clone TextBox
    4. Install all requirements (Textbox and Flask)
    4.1 pip install flask
    4.2 Please check TextBox github page for install guideline
    5. Copy model files to ./model/checkpoint_best
    6. Move all files in ./ConfigforTextBox into ./TextBox
    7. If you wish to change the model path, please modify 
        MVP.config['model_path'] in run_tuned_model.py.

#### Run
`python app.py` The backend would run on port 5000.
`python run_tuned_model.py` Run this file to test your environment without flask

### Installation for the Front-end 
#### Requirements
    Node.js >= 16.0 for Vue3

    "axios": "^1.4.0",
    "element-plus": "^2.3.7",
    "vue": "^3.2.8",
    "vue-axios": "^3.5.2",
    "vue-clipboard3": "^2.0.0"
    * For more details please check ./package.json

#### Installation
    1. Install Node.js (https://nodejs.org/en)
    2. Open cmd at Frontend folder, run "npm install"
    3. Edit ./vite.config.js, set target url to the real url of your backend

#### Run
    npm run dev


### Package and Code Citations:

1 TextBox: https://github.com/RUCAIBox/TextBox

```
@inproceedings{tang-etal-2022-textbox,
    title = "{T}ext{B}ox 2.0: A Text Generation Library with Pre-trained Language Models",
    author = "Tang, Tianyi  and  Li, Junyi  and  Chen, Zhipeng  and  Hu, Yiwen  and  Yu, Zhuohao  and  Dai, Wenxun  and  Zhao, Wayne Xin  and  Nie, Jian-yun  and  Wen, Ji-rong",
    booktitle = "Proceedings of the The 2022 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    month = dec,
    year = "2022",
    address = "Abu Dhabi, UAE",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.emnlp-demos.42",
    pages = "435--444",
}

@inproceedings{textbox,
    title = "{T}ext{B}ox: A Unified, Modularized, and Extensible Framework for Text Generation",
    author = "Li, Junyi  and  Tang, Tianyi  and  He, Gaole  and  Jiang, Jinhao  and  Hu, Xiaoxuan  and  Xie, Puzhao  and  Chen, Zhipeng  and  Yu, Zhuohao  and  Zhao, Wayne Xin  and  Wen, Ji-Rong",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing: System Demonstrations",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.acl-demo.4",
    doi = "10.18653/v1/2021.acl-demo.4",
    pages = "30--39",
}
```

2. OpenNRE: https://github.com/thunlp/OpenNRE
```
@inproceedings{han-etal-2019-opennre,
    title = "{O}pen{NRE}: An Open and Extensible Toolkit for Neural Relation Extraction",
    author = "Han, Xu and Gao, Tianyu and Yao, Yuan and Ye, Deming and Liu, Zhiyuan and Sun, Maosong",
    booktitle = "Proceedings of EMNLP-IJCNLP: System Demonstrations",
    year = "2019",
    url = "https://www.aclweb.org/anthology/D19-3029",
    doi = "10.18653/v1/D19-3029",
    pages = "169--174"
}
```

3. SpaCy: https://github.com/explosion/spaCy and https://spacy.io/

4. Framework: Vue3 (https://cn.vuejs.org/guide/quick-start.html)

5. UI library: Element-plus (https://element-plus.org/zh-CN/)

6. Http request: Axios (https://www.npmjs.com/package/vue-axios)



    
    

