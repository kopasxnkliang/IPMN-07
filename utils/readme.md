Installation Procedures:

1. Download the code folders (utils and TextBox) from Google Drive link listed in our project report. Our raw data and processed dataset are available and saved in TextBox/dataset. The file structure of ./utils is as follow:
   
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
Folder ./utils/preprocessing_utils contains python scripts to transform raw data to dataset used to fine-tune the model.
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
	    └── str_data.yaml
    ├── quick_start
    ├── trainer
    └── utils
├── *run.sh
└── run_textbox.py
```

The filenames or foldernames with the star(*) sign are the newly added files that do not exist in original TextBox folder. 

3. Install TextBox according to https://github.com/RUCAIBox/TextBox. Additional packages are listed in requirements.txt in folder ./TextBox
```
conda create -n <your_env_name> python=3.8
conda activate <your_env_name>
cd <your_folder_path_to_TextBox>
bash install.sh
pip install -r requirements.txt
```

```
python
import nltk
nltk.download('brown')
nltk.download('punkt')
```

5. 



#### structure of the utils folder
```
├── app.py
├──model
    └── checkpoint_best
├── README.md
├── run_tuned_model.py
└── TextBox
```
#### ~~modification~~

~~1. TextBox/textbox/trainer/trainer.py line 502~~
~~change ```checkpoint_dir = self.saved_model_filename + '_best'``` to full path of ```model/checkpoint_best```~~

~~2. TextBox/textbox/quick_start/experiment.py comment out line 140 & 142~~

	```
	            # self._do_train_and_valid()
	            self._do_test()
	            # self._on_experiment_end()
	```
~~3. Backend/run_tuned_model.py line 23~~
~~change ```--model_path=../IPMN-07/Backend/model/checkpoint_best``` to full path of checkpoint_best~~

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



Citations:
TextBox: https://github.com/RUCAIBox/TextBox
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
