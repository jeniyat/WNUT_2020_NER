How to Convert Conll format:
======


```

import anntoconll_wlp


anntoconll_wlp.convert_standoff_conll_single_file(input_standoff_folder,output_conll_folder_train, output_conll_file_train)


```

Example :`anntoconll_wlp.convert_standoff_conll_single_file("../../data/test_data/Standoff_Format/", "Conll_Outputs/", "all_test_sentences.txt")`


 The above command will conver the standoff format test data to conll format and then save the conll format files in `Conll_Outputs/` it will also create a text file `all_test_sentences.txt` containing all the senteces in the test set. 
