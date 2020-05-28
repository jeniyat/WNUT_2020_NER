## Evaluation 

The following script can be used for evaluation of the the Named Entity Recgonizer:
  
      ./eval/evalutation.py 

The participants are required to produce entity sequence for each sentence and submit the predictions as [StandOff format](../../data/Readme.md##-The-standoff-format:).


The evaluation script takes `<location of StandOff format gold data>` and `<location of StandOff format predicted data>` as input, and then outputs the detailed perfromance of the NER tagger. 

For example, below is the detailed performance of the Linear CRF NER.

```
pprocessed 42517 tokens with 16326 phrases; found: 15885 phrases; correct: 11899.
accuracy:  81.78%; precision:  74.91%; recall:  72.88%; FB1:  73.88
           Action: precision:  83.97%; recall:  83.97%; FB1:  83.97 foundGuessed:  4135
           Amount: precision:  85.38%; recall:  83.36%; FB1:  84.36 foundGuessed:  1156
    Concentration: precision:  79.00%; recall:  79.29%; FB1:  79.14 foundGuessed:  538
           Device: precision:  60.74%; recall:  56.08%; FB1:  58.31 foundGuessed:  433
  Generic-Measure: precision:  35.92%; recall:  26.24%; FB1:  30.33 foundGuessed:  103
         Location: precision:  67.69%; recall:  68.15%; FB1:  67.92 foundGuessed:  1334
     Measure-Type: precision:  50.21%; recall:  45.02%; FB1:  47.47 foundGuessed:  243
          Mention: precision:  65.38%; recall:  60.71%; FB1:  62.96 foundGuessed:  52
           Method: precision:  48.28%; recall:  36.57%; FB1:  41.62 foundGuessed:  437
         Modifier: precision:  56.11%; recall:  50.59%; FB1:  53.21 foundGuessed:  1449
        Numerical: precision:  55.88%; recall:  57.58%; FB1:  56.72 foundGuessed:  238
          Reagent: precision:  73.96%; recall:  74.92%; FB1:  74.43 foundGuessed:  4051
             Seal: precision:  63.64%; recall:  65.62%; FB1:  64.62 foundGuessed:  66
             Size: precision:  65.85%; recall:  48.21%; FB1:  55.67 foundGuessed:  82
            Speed: precision:  84.21%; recall:  86.75%; FB1:  85.46 foundGuessed:  171
      Temperature: precision:  94.19%; recall:  89.18%; FB1:  91.62 foundGuessed:  499
             Time: precision:  89.11%; recall:  87.15%; FB1:  88.12 foundGuessed:  845
               pH: precision:  75.47%; recall:  64.52%; FB1:  69.57 foundGuessed:  53
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

