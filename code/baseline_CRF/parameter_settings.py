from collections import OrderedDict
import argparse

parser = argparse.ArgumentParser()



parameters_crf = OrderedDict()




parser.add_argument(
    "-train_data", default="../../data/train_data/Standoff_Format/",
    help="Standoff_Format training files"
)
parser.add_argument(
    "-test_data", default="../../data/test_data/Standoff_Format/",
    help="Standoff_Format test files"
)

parser.add_argument(
    "-dev_data", default="../../data/dev_data/Standoff_Format/",
    help="Standoff_Format dev files"
)



parser.add_argument(
    "-perf_file", default="performance.tex",
    help="Output file to store the final latex table"
)


parser.add_argument(
    "-pred_file", default="prediction.txt",
    help="Output file to save all prediction"
)




parser.add_argument(
    "-include_word_features", default="1",
    help="string feature inclusion (0 to disable)"
) 


parser.add_argument(
    "-include_context", default="1",
    help="context feature inclusion (0 to disable)"
) 


parser.add_argument(
    "-context_window_len", default="5",
    help="context window length (default 5)"
) 




parser.add_argument(
    "-include_gazetteer", default="1",
    help="gazetteer feature inclusion (0 to disable)"
) 


parser.add_argument(
    "-to_latex", default="0",
    help="if print in latex format (1 to enable)"
) 


opts = parser.parse_args()



parameters_crf["train_data"]=opts.train_data
parameters_crf["test_data"]=opts.test_data
parameters_crf["dev_data"]=opts.dev_data


parameters_crf["perf_file"]=opts.perf_file
parameters_crf["pred_file"]=opts.pred_file




if opts.include_gazetteer=="0":
    parameters_crf["include_gazetteer"]=False
else:
    parameters_crf["include_gazetteer"]=True

if opts.include_word_features=="0":
    parameters_crf["include_word_features"]=False
else:
    parameters_crf["include_word_features"]=True

if opts.include_context=="0":
    parameters_crf["include_context"]=False
else:
    parameters_crf["include_context"]=True

if opts.to_latex=="0":
    parameters_crf["print_latex_format"]=False
else:
    parameters_crf["print_latex_format"]=True



parameters_crf["context_window_len"]=int(opts.context_window_len)

parameters_crf["conll_output_folder"]="Conll_Outputs/"
parameters_crf["standoff_output_folder"]="Standoff_Outputs/"



