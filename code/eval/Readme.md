How to Run Evaluation:
======


```

import evalutation



evalutation.evaluate(<path to standoff format gold data>,  <path to standoff format pred data data>, <if you want to save the performace to latex file>, <location to save the perfomance>, )

```

Example : `evalutation.evaluate(input_gold_folder="../../data/test_data/Standoff_Format/",  input_pred_folder="Standoff_Outputs/", pref_file= "performance.tex", to_latex=True)`


