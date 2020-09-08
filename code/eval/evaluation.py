#!/usr/bin/env python3
import eval_utils
import conlleval_py_exact
import conlleval_py_partial
import os

import shutil
from collections import OrderedDict
import argparse

import sys
sys.path.insert(1, 'scripts/convert_standoff_conll_ner/')
import anntoconll_wlp


def read_sentence(ip_file):
	sentences=[]
	current_sentence = []
	for line in open(ip_file):
		line=line.strip()


		if line=="" and len(current_sentence)>0:
			sentences.append(current_sentence)

			current_sentence=[]
			continue
		line_values = line.split()

		if len(line_values)==2:
			current_sentence.append(line_values)


	return sentences


def print_result(eval_result, perf_file):



	result={}
	result["header"]=["", "Precision", "Recall", "F1"]
	result["rows"]=[]

	over_all_result= eval_result['overall']

	by_category_result = eval_result['by_category']

	for entity in sorted(by_category_result):
		l = [entity, by_category_result[entity]["P"], by_category_result[entity]["R"], by_category_result[entity]["F1"]]
		result["rows"].append(l)

	l=["overall",over_all_result["P"],over_all_result["R"], over_all_result["F1"]]
	result["rows"].append(l)

	eval_utils.tolatex(result)
	eval_utils.save_perf_in_tex(result, perf_file)




def compare_prediction(conll_file_gold, conll_file_pred, perf_file, to_latex):

	gold_sentences = read_sentence(conll_file_gold)
	pred_sentences = read_sentence(conll_file_pred)

	pred_file= "prediction.txt"


	

	fout=open(pred_file,"w")

	for gold_sent_index in range(len(gold_sentences)):
		gold_sent_info =  gold_sentences[gold_sent_index]
		pred_sent_info = pred_sentences[gold_sent_index]

		for word_index in range(len(gold_sent_info)):
			gold_word_info = gold_sent_info[word_index]
			pred_word_info = pred_sent_info[word_index]

			word=gold_word_info[0]
			gold_tag=gold_word_info[1]
			pred_tag=pred_word_info[1]
			base_tag = gold_tag.replace("I-","").replace("B-","")
			op_line=word+" "+base_tag+" "+gold_tag+" "+pred_tag+"\n"
			fout.write(op_line)
		fout.write("\n\n")
	fout.write("\n\n")
	fout.close()

	print("-----------------------------")
	print(" Performance with exact match")
	print("-----------------------------")
	eval_result = conlleval_py_exact.evaluate_conll_file(inputFile=pred_file)
	print("\n\n")

	if to_latex:
		print_result(eval_result, perf_file)

	os.remove(pred_file)












def evaluate(input_gold_folder="../../data/test_data/Standoff_Format/", input_pred_folder="../baseline_CRF/Standoff_Outputs/", to_latex=False, pref_file=None):
	pred_file_type = eval_utils.find_prediction_file_format(input_pred_folder)
	ip_file_type = eval_utils.find_prediction_file_format(input_gold_folder) 

	if pred_file_type == "Standoff":
		conll_pred_folder = "Conll_OP/"
		eval_utils.make_dir_if_not_exists(conll_pred_folder)
		anntoconll_wlp.covert_standoff_to_conll(input_pred_folder, conll_pred_folder)
		input_pred_folder=conll_pred_folder


	if ip_file_type == "Standoff":
		conll_ip_folder = "Conll_IP/"
		eval_utils.make_dir_if_not_exists(conll_ip_folder)
		anntoconll_wlp.covert_standoff_to_conll(input_gold_folder, conll_ip_folder)
		input_gold_folder=conll_ip_folder


	

	combined_pred_file  = eval_utils.combine_and_merge_gold_pred(input_gold_folder, input_pred_folder)

	print("\n\n")


	print("-----------------------------")
	print(" Performance with exact match")
	print("-----------------------------")


	eval_result = conlleval_py_exact.evaluate_conll_file(inputFile=combined_pred_file)

	if to_latex:
		print_result(eval_result, perf_file)

	print("\n\n")

	print("-----------------------------")
	print(" Performance with partial match")
	print("-----------------------------")


	eval_result = conlleval_py_partial.evaluate_conll_file(inputFile=combined_pred_file)

	if to_latex:
		print_result(eval_result, perf_file)

	print("\n\n")
	
	os.remove(combined_pred_file)



	
	if pred_file_type=="Standoff":
		shutil.rmtree(conll_pred_folder)

	if ip_file_type=="Standoff":
		shutil.rmtree(conll_ip_folder)





if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parameters_eval = OrderedDict()




	# parser.add_argument(
	#     "-gold_data", default="../../data/test_data/Conll_Format/",
	#     help="Standoff_Format gold labeled files"
	# )


	parser.add_argument(
	    "-gold_data",  default="../gold_data/wlp_new_data_2020_Conll_Format/",
	    help="Standoff_Format gold labeled files"
	)

	# parser.add_argument(
	#     "-pred_data", default="../baseline_CRF/Conll_Outputs/",
	#     help="Standoff_Format prediction files"
	# )


	parser.add_argument(
	    "-pred_data",default="../all_system_output/Fancy_Man/",
	    help="Standoff_Format prediction files"
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



	parameters_eval["gold_data"]=opts.gold_data
	parameters_eval["pred_data"]=opts.pred_data
	parameters_eval["perf_file"]=opts.perf_file


	if opts.to_latex=="0":
	    parameters_eval["print_latex_format"]=False
	else:
	    parameters_eval["print_latex_format"]=True

	input_gold_folder = parameters_eval["gold_data"]




	input_pred_folder = parameters_eval["pred_data"]

	print_latex_format=parameters_eval["print_latex_format"]

	perf_file = parameters_eval["perf_file"]



	evaluate(input_gold_folder, input_pred_folder, print_latex_format, perf_file)



