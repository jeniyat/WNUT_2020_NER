import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

import sys, os
import re


from collections import Counter
import json



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


import utils

import Feature_Extractor

from parameter_settings import parameters_crf as parameters
import conll2standoff

sys.path.insert(1, '../eval/')

import evalutation


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

	def Train(self, file_to_save_features=None, file_to_save_transition=None):
		self.crf.fit(self.list_of_train_sentence_features, self.list_of_train_sentence_labels)
		#print(list(self.crf.classes_))

		if file_to_save_features:
			fout_features=open(file_to_save_features,'w')
			for (attr, label), weight in Counter(self.crf.state_features_).most_common():
				fout_features.write("%0.6f %-8s %s\n" % (weight, label, attr))

		if file_to_save_transition:
			fout_transtion=open(file_to_save_transition,'w')
			for (label_from, label_to), weight in Counter(self.crf.transition_features_).most_common():
				fout_transtion.write("%-6s -> %-7s %0.6f \n" % (label_from, label_to, weight))
		


	def Make_Prediction(self, ):
		labels = list(self.crf.classes_)
		labels.remove('O')
		self.list_of_y_pred = self.crf.predict(self.list_of_test_sentence_features)

	
	def Convert_Pred_to_CoNLL(self, conll_output_folder, protocol_name):

		
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
		fout.write("\n\n\n")
		fout.close()

	
		




if __name__ == '__main__':

	#----------------preprocessing data-------------------
	
	

	input_standoff_folder_train = parameters["train_data"]
	conll_folder_train = "Conll_Format_Data/train/"
	conll_file_train = 'Conll_Format_Data/train_conll.txt'

	


	input_standoff_folder_test = parameters["test_data"]
	conll_folder_test = "Conll_Format_Data/test/"
	conll_file_test = 'Conll_Format_Data/test_conll.txt'

	


	input_standoff_folder_dev = parameters["dev_data"]
	conll_folder_dev = "Conll_Format_Data/dev/"
	conll_file_dev = 'Conll_Format_Data/dev_conll.txt'

	
	utils.preprocess_data(input_standoff_folder_train, conll_folder_train, conll_file_train,
	input_standoff_folder_test, conll_folder_test, conll_file_test,
	input_standoff_folder_dev, conll_folder_dev, conll_file_dev)

	sorted_entity_list_file_name="sorted_entity_list_by_count.json"

	utils.Sort_Entity_by_Count(conll_file_train,sorted_entity_list_file_name)

	with open(sorted_entity_list_file_name) as f:
		sorted_entity_list = json.load(f)

	lin_crf=Linear_CRF()
	
	lin_crf.Read_Train_Data(conll_file_train)
	lin_crf.Train()
	
	
	

	list_of_test_files=utils.Read_Files_in_Input_Folder(conll_folder_test)
	utils.make_dir_if_not_exists(parameters["conll_output_folder"])

	for file_name in list_of_test_files:
		file_values = file_name.split("/")
		
		phase_name= file_values[-2]
		protocol_name = file_values[-1]
		# # print(phase_name, protocol_name)
		lin_crf.Read_Test_Data(file_name)
		lin_crf.Make_Prediction()
		lin_crf.Convert_Pred_to_CoNLL(parameters["conll_output_folder"],  protocol_name)

	

	standoff_output_directory = parameters["standoff_output_folder"]
	utils.make_dir_if_not_exists(standoff_output_directory)
	list_of_test_files_stand_off = utils.Read_Files_in_Input_Folder(parameters["conll_output_folder"])

	for file_name in list_of_test_files_stand_off:
		file_values = file_name.split("/")
		protocol_name = file_values[-1]
		conll2standoff.process(file_name, standoff_output_directory)


	#------------removing temporary folders--------------------
	shutil.rmtree(parameters["conll_output_folder"])

	shutil.rmtree('Conll_Format_Data/')
	os.remove(sorted_entity_list_file_name)


	perf_file = parameters['perf_file']
	to_latex=parameters["print_latex_format"]


	evalutation.evaluate(input_gold_folder=parameters["test_data"],  input_pred_folder=parameters["standoff_output_folder"],pref_file= perf_file, to_latex=to_latex)

	if os.path.isdir('Conll_Format_Data/'): shutil.rmtree('Conll_Format_Data/')

	list_of_text_ops = os.listdir( parameters["standoff_output_folder"] )
	for file in list_of_text_ops:
		if file.endswith(".txt"):
			os.remove( os.path.join( parameters["standoff_output_folder"], file ) )


	

	










	
