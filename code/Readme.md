# Baseline Linear CRF:


The following script contains the baseline Feature Based CRF model:

      ./crf_ner_wlp.py


and the predicted outputs (as Standoff Format) of this model on the test data will be stored at:

      ./Standoff_Outputs/

To run and get the prediction on the test data we need to proved the script with `<location of StandOff format train data>` in `-train_data` parameter and the `<location of StandOff format test data>` in the `-test_data` parameter:

```
python crf_ner_wlp.py  -train_data "../../data/train_data/Standoff_Format/" -test_data "../../data/test_data/Standoff_Format/"
```



The above command will output the peformance of the CRF model on the test data in `stdout` and save the model predictions on the test data at `/Standoff_Outputs/` in [standOff format](../../data/Readme.md##-The-standoff-format:).



## Optional arguments for Feature Ablation


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



## Optional arguments for Latex format performane presentation

The perfomnace of the model can be viewed as latex table by using the  `-to_latex` parameter as below:

```
python crf_ner_wlp.py  -train_data "../../data/train_data/Standoff_Format/" -test_data "../../data/test_data/Standoff_Format/"  `-to_latex` 1
```

The default value of `-to_latex` is `0`. The latex table will be printed to `stdout` and also saved the latex formated table in `performance.tex` file. You can change the location of the preformance file with the `-perf_file` parameter as below:

```
python crf_ner_wlp.py  -train_data "../../data/train_data/Standoff_Format/" -test_data "../../data/test_data/Standoff_Format/"  `-to_latex` 1 -perf_file "performance_crf.tex"
```



