How to Run Evaluation:
======


```

import evalutation



evalutation.evaluate(input_gold_folder= <path to standoff format gold data>,  
						input_pred_folder= <path to standoff format pred data data>, 
						pref_file= <location to save the perfomance>,
						to_latex= <binary value indicatiing choice for saving the performace to latex file>)

```

Example : 
```
evalutation.evaluate(input_gold_folder="../../data/test_data/Standoff_Format/",
										input_pred_folder="Standoff_Outputs/",
										pref_file= "performance.tex",
										to_latex=True)
```


