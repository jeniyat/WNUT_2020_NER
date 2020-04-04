## EVALUATION  

The following script can be used for evaluation of the the Named Entity Recgozizer:
  
      ./eval/evalutation.py 

The participants are required to produce entity sequence for each sentence and submit the predictions as [StandOff format](../../data/Readme.md##-The-standoff-format:) .


The evaluation script takes `<location of StandOff format gold data>` and `<location of StandOff format predicted data>` as input, and then output the detailed perfromance of the NER tagger. For example the below is the detailed performance of the Libnear CRF NER.

```
processed 41354 tokens with 15968 phrases; found: 15519 phrases; correct: 11749.
accuracy:  82.18%; precision:  75.71%; recall:  73.58%; FB1:  74.63
           Action: precision:  84.65%; recall:  84.48%; FB1:  84.56 foundGuessed:  4051
           Amount: precision:  85.70%; recall:  84.28%; FB1:  84.98 foundGuessed:  1126
    Concentration: precision:  78.07%; recall:  79.40%; FB1:  78.73 foundGuessed:  538
           Device: precision:  62.04%; recall:  56.29%; FB1:  59.03 foundGuessed:  411
  Generic-Measure: precision:  36.36%; recall:  25.53%; FB1:  30.00 foundGuessed:  99
         Location: precision:  68.57%; recall:  69.64%; FB1:  69.10 foundGuessed:  1298
     Measure-Type: precision:  51.04%; recall:  46.24%; FB1:  48.52 foundGuessed:  241
          Mention: precision:  60.00%; recall:  60.00%; FB1:  60.00 foundGuessed:  55
           Method: precision:  49.88%; recall:  37.75%; FB1:  42.97 foundGuessed:  423
         Modifier: precision:  57.18%; recall:  51.49%; FB1:  54.19 foundGuessed:  1420
        Numerical: precision:  57.14%; recall:  58.15%; FB1:  57.64 foundGuessed:  231
          Reagent: precision:  75.11%; recall:  75.56%; FB1:  75.34 foundGuessed:  3926
             Seal: precision:  68.25%; recall:  67.19%; FB1:  67.72 foundGuessed:  63
             Size: precision:  67.47%; recall:  51.38%; FB1:  58.33 foundGuessed:  83
            Speed: precision:  84.21%; recall:  86.75%; FB1:  85.46 foundGuessed:  171
      Temperature: precision:  93.78%; recall:  89.64%; FB1:  91.66 foundGuessed:  498
             Time: precision:  89.57%; recall:  87.47%; FB1:  88.51 foundGuessed:  834
               pH: precision:  72.55%; recall:  59.68%; FB1:  65.49 foundGuessed:  51
``` 
    


### How to Run Evaluation:


```
python evalutation.py  -gold_data "../../data/test_data/Standoff_Format/" -pred_data "../baseline_CRF/Standoff_Outputs/"
```

### Evaluation to Latex:

The evalutation script also provide the functionality to view the performance as a latex table (by using the `-to_latex` parameter):

```
python evalutation.py  -gold_data "../../data/test_data/Standoff_Format/" -pred_data "../baseline_CRF/Standoff_Outputs/" -to_latex 1
```

The default value of this parameter is `0`. The above command will also save the latex formated table in `performance.tex` file. You can change the location of this file with the `-perf_file` parameter.


### Importi evalution function inside another script:

The evalutaion funciton can also be called from other python scripts using the same parameters. Below is the sample code:

```

import evalutation


evalutation.evaluate(input_gold_folder="../../data/test_data/Standoff_Format/",input_pred_folder="Standoff_Outputs/", to_latex=True, pref_file= "performance.tex")

```

