How to Convert Conll format:
======


```

import anntoconll_wlp


anntoconll_wlp.convert_standoff_conll_single_file(input_standoff_folder,output_conll_folder_train, output_conll_file_train)


```

Example : `anntoconll_wlp.convert_standoff_conll_single_file("../../data/test_data/Standoff_Format/", "Standoff_Outputs/", "all_test_sentences.txt")`
