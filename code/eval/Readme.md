## EVALUATION  

The following script can be used for evaluation of the the Named Entity Recgozizer:
  
      ./eval/evalutation.py 

The participants are required to produce entity sequence for each sentence and submit the predictions as [standoff format](../../data/Readme.md) .

##-The-standoff-format:

The evaluation script takes the gold and predicted entities as input and then evaluate the predicted entity with respect to the gold entities.


The predicted output file should have the exactly same number of lines as the gold file.


Each line has 2 columns 
  and separated by a tab in between, like this:
     | Binary Label (true/false) | Degreed Score (between 0 and 1, in the 4 decimal format) |
  if your system only gives binary labels, put "0.0000" in all second columns.  
  
  The output file names look like this:
      PIT2015_TEAMNAME_01_nameofthisrun.output 
      PIT2015_TEAMNAME_02_nameofthisrun.output      
    


How to Run Evaluation:
======


```

import evalutation



evalutation.evaluate(input_gold_folder= <path to standoff format gold data>,  
						input_pred_folder= <path to standoff format pred data data>, 
						pref_file= <location to save the perfomance>,
						to_latex= <binary value indicatiing choice for saving the performace to latex file>)

```

Example : `evalutation.evaluate(input_gold_folder="../../data/test_data/Standoff_Format/",input_pred_folder="Standoff_Outputs/", pref_file= "performance.tex",to_latex=True)`



