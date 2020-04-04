import sys, os
import re
from collections import Counter
import json
from itertools import chain
import nltk


import shutil

def regex_or(*items):
    return '(?:' + '|'.join(items) + ')'




class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split(' ')
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)




class Feature_Extractor:
	"""docstring for Feature_Extractor"""
	def __init__(self):
		
		self.include_camel_case = True
		self.include_context = True
		self.include_word_features= True
		self.context_window_len=0
		self.include_gazetteer=True

		self.gazetter_action_file = "gazetters/Actions.txt"
		self.gazetter_measure_unit_file = "gazetters/Meausre_Units.txt"
		self.gazetter_time_unit_file = "gazetters/Time_Units.txt"

		self.Load_Rule_Gazetteer()

	def Load_Rule_Gazetteer(self):
		self.list_of_actions=set()
		self.list_of_time_units= set()
		self.list_of_measure_units=set()

		for line in open(self.gazetter_action_file):
			word=line.strip()
			if word=="":continue
			self.list_of_actions.add(word)

		for line in open(self.gazetter_measure_unit_file):
			word=line.strip()
			if word=="":continue
			self.list_of_measure_units.add(word)

		for line in open(self.gazetter_time_unit_file):
			word=line.strip()
			if word=="":continue
			self.list_of_time_units.add(word)

	def merge_dicts(self,dict_list):
		merged_dicts = {k: v for d in dict_list for k, v in d.items()}
		return merged_dicts

	def get_camel_case_snake_case_features(self,word):
		# print(word)
		# print(type(word))
		word_dict={}
		if not self.include_camel_case:
			return word_dict


		Bound = r"(?:\W|^|$)"
		CAMEL_CASE= r'([\w]*(?:[a-z0-9]+[A-Z]+|[A-Z]+[a-z]+)[\w]*)'+"(?=" +Bound+")"
		camel_case_rule = re.compile(CAMEL_CASE)
		camel_case_words = camel_case_rule.findall(word)

		SNAKE_CASE = r'([\w]*(?:[\w]+_|_[\w]+)+[\w]+)'+"(?=" +Bound+")"
		snake_case_rule = re.compile(SNAKE_CASE)
		snake_case_words = snake_case_rule.findall(word)

		
		word_dict["snake_case"]=False
		word_dict["camel_case"]=False

		#print(snake_case_words, camel_case_words)
		if len(camel_case_words)>0:
			word_dict["camel_case"]=True
		if len(snake_case_words)>0:
			word_dict["snake_case"]=True
		return word_dict

	def if_temp(self,word):
		word_dict={}

		word_dict["if_temp"]=False
		if "°C" in word:
			word_dict["if_temp"]=True
		
		return word_dict


	def get_word_features(self,word):
		word_dict={}
		


		word_dict["word"]=word

		if not self.include_word_features:
			return word_dict


		word_dict["word_lower"]=word.lower()

		word_dict["prefix_1"]=word[0:1]
		word_dict["prefix_2"]=word[0:2]
		word_dict["prefix_3"]=word[0:3]

		word_dict["suffix_1"]=word[len(word)-1:len(word)]
		word_dict["suffix_2"]=word[len(word)-2:len(word)]
		word_dict["suffix_3"]=word[len(word)-3:len(word)]

		if re.search(r'^[A-Z]', word):
			word_dict['INITCAP']=True
		else:
			word_dict['INITCAP']=False

		if re.match(r'^[A-Z]+$', word):
			word_dict['ALLCAP']=True
		else:
			word_dict['ALLCAP']=False


		if re.match(r'.*[0-9].*', word):
			word_dict['HASDIGIT']=True
		else:
			word_dict['HASDIGIT']=False

		if re.match(r'[0-9]', word):
			word_dict['SINGLEDIGIT']=True
		else:
			word_dict['SINGLEDIGIT']=False

		if re.match(r'[0-9][0-9]', word):
			word_dict['DOUBLEDIGIT']=True
		else:
			word_dict['DOUBLEDIGIT']=False

		if re.match(r'[.,;:?!-+\'"]', word):
			word_dict['PUNCTUATION']=True
		else:
			word_dict['PUNCTUATION']=False


		if "°C" in word:
			word_dict["if_temp"]=True
		else:
			word_dict["if_temp"]=False

		if "%" in word:
			word_dict["has_percent_sign"]=True
		else:
			word_dict["has_percent_sign"]=False
		


		

		return word_dict

	


	


	def get_gazetter_featurs(self,word):
		word_dict={}

		if word.lower() in self.list_of_actions:
			word_dict["ACTION"]=True
		else:
			word_dict["ACTION"]=False


		if word.lower() in self.list_of_time_units:
			word_dict["TIME_UNIT"]=True
		else:
			word_dict["TIME_UNIT"]=False



		if word.lower() in self.list_of_measure_units:
			word_dict["MEASURE_UNIT"]=True
		else:
			word_dict["MEASURE_UNIT"]=False


		return word_dict


	def get_sentence_features(self,sent_words):
		# print(sent_words)
		# print(mark_down)

		list_of_word_features=[]
		for i in range(len(sent_words)):
			w=sent_words[i]
			w_dict={}
			
			word_feature_dict = self.get_word_features(w)
			camel_case_snake_case_features_dict = self.get_camel_case_snake_case_features(w)
			gazetter_features_dict = self.get_gazetter_featurs(w)
			
			if i==len(sent_words)-1:
				next_word = None
			else:
				next_word = sent_words[i]

			
			w_dict=self.merge_dicts([word_feature_dict,camel_case_snake_case_features_dict, gazetter_features_dict])

			w_dict["EOS"]=False
			w_dict["BOS"]=False

			#print("-------------------------word", w)
			if i==0:
				w_dict["BOS"]=True
			if i==len(sent_words)-1:
				w_dict["EOS"]=True
			
			

			




			if self.include_context:
				LEFT_RIGHT_WINDOW=self.context_window_len
			else:
				LEFT_RIGHT_WINDOW=0
			for j in range(i-LEFT_RIGHT_WINDOW,i+LEFT_RIGHT_WINDOW):
				
				diff=abs(i-j)
				if j >= 0 and j < i:
					left_window_word=sent_words[j]
					dict_key="LEFT_WINDOW:"+str(diff)
					#print("left: ",diff)
					w_dict[dict_key]=left_window_word
					#w_dict_left=self.get_word_features(left_window_word)
					#print(w_dict_left)
				elif j < len(sent_words) and j > i:
					right_window_word=sent_words[j]
					dict_key="RIGHT_WINDOW:"+str(diff)
					#print("right: ",diff)
					w_dict[dict_key]=right_window_word
			#print(w_dict)

			

			list_of_word_features.append(w_dict)
		#print(list_of_word_features[1].keys())
		return list_of_word_features
