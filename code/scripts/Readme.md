How to Convert Standoff files to Conll format:
======


```

import anntoconll_wlp


anntoconll_wlp.convert_standoff_conll_single_file(input_standoff_folder,output_conll_folder_train, output_conll_file_train)


```

Example :`anntoconll_wlp.convert_standoff_conll_single_file("../../data/test_data/Standoff_Format/", "Conll_Outputs/", "all_test_sentences.txt")`


 The above command will conver the standoff format test data to conll format and then save the conll format files in `Conll_Outputs/` it will also create a text file `all_test_sentences.txt` containing all the senteces in the test set. 



How to Convert a Conll file to Standoff Format:
======


```

import anntoconll_wlp


anntoconll_wlp.conll2standoff.process(conll_file_name, standoff_output_directory)



```

Example :`anntoconll_wlp.conll2standoff.process('Conll_Outputs/protocol_2_conll.txt','Standoff_Outputs/')`


 The above command will conver the conll format file 'Conll_Outputs/protocol_2_conll.txt' to standoff format and save in the 'Standoff_Outputs/' as 'Standoff_Outputs/protocol_2.txt' and 'Standoff_Outputs/protocol_2.ann' 