
First, install TextBox. Then move TextBox to Backend and move checkpoint_best to Backend/model.

#### structure
```
├── app.py
├── ConfigforTextBox
    ├── dataset
    └── textbox
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
`python run_tuned_model.py` Run this file to test your environment without flask