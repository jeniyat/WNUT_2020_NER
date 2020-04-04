from collections import OrderedDict
import argparse

parser = argparse.ArgumentParser()



parameters = OrderedDict()




parser.add_argument(
    "-gold_data", default="../../data/test_data/Standoff_Format/",
    help="Standoff_Format gold labeled files"
)

parser.add_argument(
    "-pred_data", default="../baseline_CRF/Standoff_Outputs/",
    help="Standoff_Format prediction files"
)

parser.add_argument(
    "-pred_file", default="prediction.txt",
    help="Output file to save all prediction"
)


parser.add_argument(
    "-perf_file", default="performance.tex",
    help="Output file to store the final latex table"
)

parser.add_argument(
    "-to_latex", default="0",
    help="if print in latex format (1 to enable, 0 to disable)"
) 


opts = parser.parse_args()



parameters["gold_data"]=opts.gold_data
parameters["pred_data"]=opts.pred_data
parameters["perf_file"]=opts.perf_file
parameters["pred_file"]=opts.pred_file

if opts.to_latex=="0":
    parameters["print_latex_format"]=False
else:
    parameters["print_latex_format"]=True