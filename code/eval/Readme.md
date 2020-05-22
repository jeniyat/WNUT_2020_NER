## Evaluation 

The following script can be used for evaluation of the the Named Entity Recgonizer:
  
      ./eval/evalutation.py 

The participants are required to produce entity sequence for each sentence and submit the predictions as [StandOff format](../../data/Readme.md##-The-standoff-format:).


The evaluation script takes `<location of StandOff format gold data>` and `<location of StandOff format predicted data>` as input, and then outputs the detailed perfromance of the NER tagger. 

For example, below is the detailed performance of the Linear CRF NER.

```
processed 42517 tokens with 16326 phrases; found: 15857 phrases; correct: 11971.
accuracy:  82.01%; precision:  75.49%; recall:  73.32%; FB1:  74.39
           Action: precision:  84.56%; recall:  84.23%; FB1:  84.40 foundGuessed:  4119
           Amount: precision:  85.21%; recall:  83.19%; FB1:  84.19 foundGuessed:  1156
    Concentration: precision:  77.70%; recall:  79.29%; FB1:  78.49 foundGuessed:  547
           Device: precision:  61.25%; recall:  56.29%; FB1:  58.67 foundGuessed:  431
  Generic-Measure: precision:  36.00%; recall:  25.53%; FB1:  29.88 foundGuessed:  100
         Location: precision:  68.83%; recall:  69.51%; FB1:  69.17 foundGuessed:  1338
     Measure-Type: precision:  51.64%; recall:  46.49%; FB1:  48.93 foundGuessed:  244
          Mention: precision:  59.65%; recall:  60.71%; FB1:  60.18 foundGuessed:  57
           Method: precision:  50.69%; recall:  38.30%; FB1:  43.63 foundGuessed:  436
         Modifier: precision:  56.82%; recall:  51.34%; FB1:  53.94 foundGuessed:  1452
        Numerical: precision:  56.36%; recall:  57.58%; FB1:  56.96 foundGuessed:  236
          Reagent: precision:  74.75%; recall:  75.22%; FB1:  74.98 foundGuessed:  4024
             Seal: precision:  68.25%; recall:  67.19%; FB1:  67.72 foundGuessed:  63
             Size: precision:  66.67%; recall:  50.00%; FB1:  57.14 foundGuessed:  84
            Speed: precision:  84.21%; recall:  86.75%; FB1:  85.46 foundGuessed:  171
      Temperature: precision:  93.85%; recall:  89.75%; FB1:  91.76 foundGuessed:  504
             Time: precision:  89.69%; recall:  87.62%; FB1:  88.64 foundGuessed:  844
               pH: precision:  72.55%; recall:  59.68%; FB1:  65.49 foundGuessed:  51
``` 
    


### How to run evaluation:

To run the evalutaion script, you need to provide it with-

1) The `<location of StandOff format gold data>` in `-gold_data` parameter, and 
2) The `<location of StandOff format predicted data>` in the `-pred_data` parameter

The folder containing StandOff format predicted data only needs to contain the `.ann` files.


```
python evalutation.py  -gold_data "../../data/test_data/Standoff_Format/" -pred_data "../baseline_CRF/Standoff_Outputs/"
```

### Print performance as LaTex table:

The evalutation script also provides the functionality to view the performance as a LaTex table (by using the `-to_latex` parameter):

```
python evalutation.py  -gold_data "../../data/test_data/Standoff_Format/" -pred_data "../baseline_CRF/Standoff_Outputs/" -to_latex 1
```

The default value of `-to_latex` is `0`. The latex table will be printed to `stdout` and saved in `performance.tex` file. You can change the location of this file with the `-perf_file` parameter.


### Import evalution function inside another script:

The evalutaion funciton can also be called from other python scripts using the same parameters. Below is a sample code:

```

import evalutation


evalutation.evaluate(input_gold_folder="../../data/test_data/Standoff_Format/",input_pred_folder="Standoff_Outputs/", to_latex=True, pref_file= "performance.tex")

```

