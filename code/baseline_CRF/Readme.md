How to Run Linear CRF:
======


```
python crf_ner_wlp.py

```
Output: Will Output the peformance of the CRF model on the test data in latex format in in stdout.

```

```

Output will also create following two files:

1) `Standoff_Outputs/`: to store the prediction of them model.

2) `performance.tex`: store the performance in latex format.


Optional arguments for Feature Ablation
======

The following arguments can be passed to the crf_ner.py for feature ablation
```
  -h, --help            show this help message and exit
  --train_data TRAIN          Train set location (default is "../../data/train_data/Standoff_Format/")
  --dev_data DEV              Dev set location  (default is "../../data/dev_data/Standoff_Format/")
  --test_data TEST            Test set location  (default is "../../data/test_data/Standoff_Format/")

  
  -perf_file PERF_FILE  Output file to store the final latex table (default is "performance.tex")
  
  -include_word_features INCLUDE_WORD_FEATURES
                        string feature inclusion (0 to disable)
  -include_context INCLUDE_CONTEXT
                        context feature inclusion (0 to disable)
  -include_gazetteer INCLUDE_GAZETTEER
                        gazetteer feature inclusion (0 to disable) 
                        [gazetters used in this model can be found in the  'gazetters/' folder]
```

Example: Exclude String Features:  `python crf_ner.py -include_camel_case 0 -include_word_features 0`

Example: Exclude Context Features:  `python crf_ner.py -include_context 0 -include_word_features 0`


Example: Exclude Gazetteer Features:  `python crf_ner.py -include_gazetteer 0`





