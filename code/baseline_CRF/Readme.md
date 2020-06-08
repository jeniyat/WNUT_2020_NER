## Baseline Linear CRF:


We provided a simple Liner CRF model built using contextual, lexical and gazetter features. The following script contains the baseline Feature Based CRF model:

```
      ./crf_ner_wlp.py

```

The predicted outputs of this model on the test data will be stored as both StandOff and CoNLL fomat in the following directories respectively:
```
      ./Standoff_Outputs/
      ./Conll_Outputs/
```
To run and get the prediction on the test data, you need to provide the script with the following:

1) The `<location of StandOff format train data>` in `-train_data` parameter, and 
2) The `<location of StandOff format test data>` in the `-test_data` parameter


```
python crf_ner_wlp.py  -train_data "../../data/train_data/Standoff_Format/" -test_data "../../data/test_data/Standoff_Format/"
```





### Optional arguments for Feature Ablation


The following arguments can be passed to the crf_ner_wlp.py for feature ablation:

```

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

## Evaluting model performance:

The following script should be used to evaluate the pefromnace of the model predictions:
  
      ./evalutation.py

Please see the detailed evalution process at: [Eval folder](../eval/Readme.md)