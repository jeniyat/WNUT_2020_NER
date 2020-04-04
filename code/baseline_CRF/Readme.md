## Baseline Linear CRF:


The following script contains the baseline Feature Based CRF model:
```
      ./crf_ner_wlp.py

```

The predicted outputs (as Standoff Format) of this model on the test data will be stored at:
```
      ./Standoff_Outputs/
```
To run and get the prediction on the test data, you need to provide the script with the following:

1) The `<location of StandOff format gold data>` in `-gold_data` parameter, and 
2) The `<location of StandOff format predicted data>` in the `-pred_data` parameter


```
python crf_ner_wlp.py  -train_data "../../data/train_data/Standoff_Format/" -test_data "../../data/test_data/Standoff_Format/"
```



The above command will output the peformance of the CRF model on the test data in `stdout` and save the model predictions on the test data at `/Standoff_Outputs/` in [standOff format](../../data/Readme.md##-The-standoff-format:).



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



### Optional arguments for Latex format performane presentation

The performnace of the model can be viewed as LaTex table using the  `-to_latex` parameter as below:

```
python crf_ner_wlp.py  -train_data "../../data/train_data/Standoff_Format/" -test_data "../../data/test_data/Standoff_Format/"  `-to_latex` 1
```

The default value of `-to_latex` is `0`. The LaTex table will be printed to `stdout` and saved in `performance.tex` file. You can change the location of the performance file with the `-perf_file` parameter as below:

```
python crf_ner_wlp.py  -train_data "../../data/train_data/Standoff_Format/" -test_data "../../data/test_data/Standoff_Format/"  `-to_latex` 1 -perf_file "performance_crf.tex"
```



