import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

import sys, os
import re
from glob import glob


from collections import Counter

import json

import utils

from itertools import chain
import nltk
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn import metrics
from sklearn.model_selection  import cross_val_score

from sklearn.model_selection import RandomizedSearchCV
import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

import shutil



import tolatex
import conlleval_py
from utils import Sort_Entity_by_Count
import Feature_Extractor

from parameter_settings import parameters



class Linear_CRF:
	"""docstring for CRF_Tagger"""
	def __init__(self):
		self.feature_extractor=Feature_Extractor.Feature_Extractor()
		self.crf = sklearn_crfsuite.CRF(algorithm='lbfgs', c1=0.05, c2=0.01, max_iterations=50, all_possible_transitions=True, min_freq=0)#micro: 52.13

	def Read_File(self,ip_file):
		list_of_sentence_words_in_file=[]
		list_of_sentence_labels_in_file=[]


		current_sent_words=[]
		current_sent_labels=[]

		for line in open(ip_file):
			# print(line)
			line=line.strip()

			if line=="":
				list_of_sentence_words_in_file.append(current_sent_words)
				list_of_sentence_labels_in_file.append(current_sent_labels)

				current_sent_words=[]
				current_sent_labels=[]

				continue

			(word, gold_label)= line.split("\t")
			current_sent_words.append(word)

			if gold_label=="O":
				current_sent_labels.append(gold_label)

			else:
				gold_label_prefix = gold_label[0]
				gold_label_base = gold_label.replace("B-","").replace("I-","").replace("-","_")
				gold_label_updated = gold_label_prefix+"-"+gold_label_base
				current_sent_labels.append(gold_label_updated)



			
			

		return (list_of_sentence_words_in_file, list_of_sentence_labels_in_file)
			

	def Read_Train_Data(self, train_file):
		(self.list_of_train_sentence_words, self.list_of_train_sentence_labels) = self.Read_File(train_file)
		self.list_of_train_sentence_features=[]


		for i in range(0,len(self.list_of_train_sentence_words)):
			sent=self.list_of_train_sentence_words[i]
			sent_features = self.feature_extractor.get_sentence_features(sent)
			self.list_of_train_sentence_features.append(sent_features)


	def Read_Test_Data(self, test_file):
		(self.list_of_test_sentence_words, self.list_of_test_sentence_labels) = self.Read_File(test_file)
		self.list_of_test_sentence_features=[]

		for i in range(0,len(self.list_of_test_sentence_words)):
			sent=self.list_of_test_sentence_words[i]
			sent_features = self.feature_extractor.get_sentence_features(sent)
			self.list_of_test_sentence_features.append(sent_features)

	def Train(self, file_to_save_features, file_to_save_transition):
		self.crf.fit(self.list_of_train_sentence_features, self.list_of_train_sentence_labels)
		#print(list(self.crf.classes_))
		fout_transtion=open(file_to_save_transition,'w')
		fout_features=open(file_to_save_features,'w')
		for (label_from, label_to), weight in Counter(self.crf.transition_features_).most_common():
			fout_transtion.write("%-6s -> %-7s %0.6f \n" % (label_from, label_to, weight))
		for (attr, label), weight in Counter(self.crf.state_features_).most_common():
			fout_features.write("%0.6f %-8s %s\n" % (weight, label, attr))


	def Make_Prediction(self, ):
		labels = list(self.crf.classes_)
		labels.remove('O')
		self.list_of_y_pred = self.crf.predict(self.list_of_test_sentence_features)

	
	def Convert_Pred_to_CoNLL(self, conll_output_folder, phase_name, protocol_name):
		conll_output_folder = conll_output_folder+phase_name+"/"

		utils.make_dir_if_not_exists(conll_output_folder)

		


		conll_file_name = conll_output_folder+protocol_name
		


		fout=open(conll_file_name,"w")
		for i in range(len(self.list_of_test_sentence_features)):
			sent=self.list_of_test_sentence_features[i]
			list_of_words=[]
			for w in sent:
				word = w["word"]
				list_of_words.append(word)
			gold_labels=self.list_of_test_sentence_labels[i]
			predicted_labels=self.list_of_y_pred[i]
			
			for k in range(len(gold_labels)):
				word=list_of_words[k]
				gold_tag=gold_labels[k]
				pred_tag=predicted_labels[k]
				#print(gold_tag)
				if gold_tag=="O":
					base_tag="O"
				else:
					base_tag=gold_tag.split("-")[1]
				op_line=word+"\t"+pred_tag+"\n"
				fout.write(op_line)
			fout.write("\n")
		fout.close()


	def Evaluate_w_Conll_Eval_on_all(self,op_file_name, entity_list):
		#the current word, its base, the chunk tag according to the corpus and the predicted chunk tag [https://www.clips.uantwerpen.be/conll2000/chunking/output.html]
		fout=open(op_file_name,"w")
		for i in range(len(self.list_of_test_sentence_features)):
			sent=self.list_of_test_sentence_features[i]
			list_of_words=[]
			for w in sent:
				word = w["word"]
				list_of_words.append(word)
			gold_labels=self.list_of_test_sentence_labels[i]
			predicted_labels=self.list_of_y_pred[i]
			# print(list_of_words)
			# print(gold_labels)
			# print(predicted_labels)
			for k in range(len(gold_labels)):
				word=list_of_words[k]
				gold_tag=gold_labels[k]
				pred_tag=predicted_labels[k]
				#print(gold_tag)
				if gold_tag=="O":
					base_tag="O"
				else:
					base_tag=gold_tag.split("-")[1]
				op_line=word+" "+base_tag+" "+gold_tag+" "+pred_tag+"\n"
				fout.write(op_line)
			fout.write("\n")
		fout.close()
		# print("coneval:")
		eval_result = conlleval_py.evaluate_conll_file(inputFile=op_file_name)
		if parameters["print_latex_format"]:
			self.print_result(eval_result, entity_list)
		

	def print_result(self,eval_result, entity_list):
		Fout=open(parameters["perf_file"],'w')
		result={}
		result["header"]=["", "Precision", "Recall", "F1", "Predicted", "Correctly Predicted"]
		result["rows"]=[]

		Fout.write(" & ".join(result["header"]))
		Fout.write(" \\\\")
		Fout.write("\n")
		Fout.write("\\hline")
		Fout.write("\n")
		
		over_all_result= eval_result['overall']
		by_category_result = eval_result['by_category']
		#load_sorted_entity_file
		
		sorted_entity_list = entity_list


		for entity in sorted_entity_list: 
			if entity not in by_category_result: 
				continue
			l = [entity, by_category_result[entity]["P"], by_category_result[entity]["R"], by_category_result[entity]["F1"], by_category_result[entity]["Total Predicted"], by_category_result[entity]["Correctly Predicted"] ]
			result["rows"].append(l)
			
		
		l=["overall",over_all_result["P"],over_all_result["R"], over_all_result["F1"], over_all_result["Total Predicted"], over_all_result["Correctly Predicted"]]
		result["rows"].append(l)
		tolatex.tolatex(result)


		result={}
		result["header"]=["", "Precision", "Recall", "F1"]
		result["rows"]=[]
		
		over_all_result= eval_result['overall']
		by_category_result = eval_result['by_category']
		
		
		for entity in sorted_entity_list: 
			if entity not in by_category_result: 
				continue
			l = [entity, by_category_result[entity]["P"], by_category_result[entity]["R"], by_category_result[entity]["F1"]]
			result["rows"].append(l)
			Fout.write(" & ")
			Fout.write(" & ".join([str(i) for i in l]))
			Fout.write(" \\\\")
			Fout.write("\n")
			Fout.write("\\hline")
			Fout.write("\n")

		l=["overall",over_all_result["P"],over_all_result["R"], over_all_result["F1"]]
		result["rows"].append(l)
		
		Fout.write(" & ".join([str(i) for i in l]))
		Fout.write(" \\\\")
		Fout.write("\n")
		Fout.write("\\hline")
		Fout.write("\n")


		tolatex.tolatex(result)
		Fout.close()
		




def Merge_Files(list_of_ip_files, op_file):

	fout = open(op_file,'w')

	for file in list_of_ip_files:
		for line in open(file):
			fout.write(line)





if __name__ == '__main__':
	
	output_folder_location="temp_files/"
	utils.make_dir_if_not_exists(output_folder_location)

	conll_format_train_files = "../../data/train_data/Conlll_Format/"
	conll_format_test_files = "../../data/dev_data/Conlll_Format/"


	list_of_train_files = utils.Read_Files_in_Input_Folder(conll_format_train_files)
	merged_train_file=output_folder_location+"train.txt"
	Merge_Files(list_of_train_files, merged_train_file)
	

	sorted_entity_list_file_name="sorted_entity_list_by_count.json"
	Sort_Entity_by_Count(merged_train_file,sorted_entity_list_file_name)

	with open(sorted_entity_list_file_name) as f:
		sorted_entity_list = json.load(f)

	lin_crf=Linear_CRF()
	
	lin_crf.Read_Train_Data(merged_train_file)
	

	op_transition_file_name="sorted_transitions.txt"
	op_feature_file_name="sorted_features.txt"

	lin_crf.Train(op_feature_file_name, op_transition_file_name)

	list_of_test_files = utils.Read_Files_in_Input_Folder(conll_format_test_files)
	merged_test_file=output_folder_location+"test.txt"
	Merge_Files(list_of_test_files, merged_test_file)
	lin_crf.Read_Test_Data(merged_test_file)
	
	lin_crf.Make_Prediction()
	op_file_name=parameters["pred_file"]
	lin_crf.Evaluate_w_Conll_Eval_on_all(op_file_name, sorted_entity_list)
	utils.make_dir_if_not_exists(parameters["conll_output_folder"])

	for file_name in list_of_test_files:
		file_values = file_name.split("/")
		# print(file_values)
		phase_name= file_values[-2]
		protocol_name = file_values[-1]
		# print(phase_name, protocol_name)
		lin_crf.Read_Test_Data(file_name)
		lin_crf.Make_Prediction()
		lin_crf.Convert_Pred_to_CoNLL(parameters["conll_output_folder"],  phase_name, protocol_name)
		

































