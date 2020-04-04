from parameter_settings_eval import parameters
import eval_utils
import conlleval_py
import os

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



def get_line(sentence_info):
	sentence = ""
	for word_info in sentence_info:
		sentence+= word_info[0]+" "

	sentence=sentence.strip()
	return sentence


def find_pred_sent_index(gold_sent, pred_sentences, list_of_matched_indices):

	for pred_sent_index in range(len(pred_sentences)):
		if pred_sent_index in list_of_matched_indices:
			continue

		pred_sent_info=pred_sentences[pred_sent_index]
		pred_sent = get_line(pred_sent_info)
		if pred_sent==gold_sent:
			return pred_sent_index


		

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

	
	

	fout=open(parameters["pred_file"],"w")

	list_of_matched_tuples = []
	list_of_matched_indices = []


	for gold_sent_index in range(len(gold_sentences)):

		gold_sent_info = gold_sentences[gold_sent_index]
		gold_sent = get_line(gold_sent_info)

		pred_sent_index = find_pred_sent_index(gold_sent, pred_sentences, list_of_matched_indices)
		if pred_sent_index:
			list_of_matched_indices.append(pred_sent_index)

			list_of_matched_tuples.append((gold_sent_index, pred_sent_index))
			# print((gold_sent_index, pred_sent_index))

	fout=open(parameters["pred_file"],"w")

	for (gold_sent_index, pred_sent_index) in list_of_matched_tuples:
		gold_sent_info =  gold_sentences[gold_sent_index]
		pred_sent_info = pred_sentences[pred_sent_index]

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

	eval_result = conlleval_py.evaluate_conll_file(inputFile=parameters["pred_file"])

	if to_latex:
		print_result(eval_result, perf_file)

	os.remove(parameters["pred_file"])












def evaluate(input_gold_folder="../../data/test_data/Standoff_Format/", input_pred_folder="../baseline_CRF/Standoff_Outputs/", to_latex=False, pref_file=None):
	conll_folder_gold = "Conll_Format_Data/gold/"
	conll_file_gold = 'Conll_Format_Data/gold.txt'

	conll_folder_pred = "Conll_Format_Data/pred/"
	conll_file_pred = 'Conll_Format_Data/pred.txt'

	eval_utils.preprocess_data_to_merge(input_gold_folder, conll_folder_gold, conll_file_gold,input_pred_folder, conll_folder_pred, conll_file_pred)
    

	compare_prediction(conll_file_gold, conll_file_pred, pref_file, to_latex)

	


if __name__ == '__main__':
	
	input_gold_folder = parameters["gold_data"]


	input_pred_folder = parameters["pred_data"]

	print_latex_format=parameters["print_latex_format"]

	perf_file = parameters["perf_file"]



	evaluate(input_gold_folder, input_pred_folder, print_latex_format, perf_file)
	






