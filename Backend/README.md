
First, install TextBox. Then move TextBox to Backend and move checkpoint_best to Backend/model.

**structure**
```
├── app.py
├──model
    └── checkpoint_best
├── README.md
├── run_tuned_model.py
└── TextBox
```
**modification**

1. TextBox/textbox/trainer/trainer.py line 502 
change ```checkpoint_dir = self.saved_model_filename + '_best'``` to full path of ```model/checkpoint_best```

2. TextBox/textbox/quick_start/experiment.py comment out line 140 & 142 
	```
	            # self._do_train_and_valid()
	            self._do_test()
	            # self._on_experiment_end()
	```
3. Backend/run_tuned_model.py line 23 
change ```--model_path=../IPMN-07/Backend/model/checkpoint_best``` to full path of checkpoint_best
