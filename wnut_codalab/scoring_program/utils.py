from collections import Counter
import json


import sys, os
import re
from glob import glob
from nltk import word_tokenize

import anntoconll_wlp





def Read_Files_in_Input_Folder(input_folder):
    start_dir = input_folder
    # start_dir = "/Users/jeniya/Desktop/NER_RECOG_SW/brat-v1.3_Crunchy_Frog/data/so_annotated_data/selected/phase_01_01"
    pattern   = "*.txt"
    file_location_list=[]
    for dir,_,_ in os.walk(start_dir):
        file_location_list.extend(glob(os.path.join(dir,pattern))) 
    
    # print("total prtocols in : ", input_folder," = ", len(file_location_list))
    return sorted(file_location_list)


def Merge_Files(list_of_ip_files, op_file):

    fout = open(op_file,'w')

    for file in list_of_ip_files:
        for line in open(file):
            fout.write(line)


def make_dir_if_not_exists(dir_name):
    try:
        os.mkdir(dir_name)
    except Exception as e:
        pass


def preprocess_data(input_standoff_folder_train, output_conll_folder_train, output_conll_file_train,
    input_standoff_folder_test, output_conll_folder_test, output_conll_file_test,
    input_standoff_folder_dev, output_conll_folder_dev, output_conll_file_dev):
    anntoconll_wlp.convert_standoff_conll_single_file(input_standoff_folder_train, output_conll_folder_train, output_conll_file_train)
    anntoconll_wlp.convert_standoff_conll_single_file(input_standoff_folder_test, output_conll_folder_test, output_conll_file_test)
    anntoconll_wlp.convert_standoff_conll_single_file(input_standoff_folder_dev, output_conll_folder_dev, output_conll_file_dev)





class Sort_Entity_by_Count:
    """docstring for Sort_Entity_by_Count"""
    def __init__(self, train_file,output_file):
        l = self.Read_File(train_file)
        #
        self.list_of_train_sentence_words=l[0]
        self.list_of_train_sentence_labels=l[1]

        train_label_counter = Counter(x for xs in self.list_of_train_sentence_labels for x in xs)
        train_result=self.get_label_counter(train_label_counter)


        list_keys= [x[0] for x in train_result["label_phrase_counter"].most_common()]
        with open(output_file, 'w') as outfile:
            json.dump(list_keys, outfile)



    def get_label_counter(self, label_counter):
        label_phrase_counter=Counter()
        label_word_counter=Counter()

        word_count=0
        entities_count=0

        for c in label_counter:
            split_c=c.split("-",1)
            type_c=split_c[0]
            if type_c=="O":
                word_count+=label_counter[c]
                continue
            entity_name=split_c[1]
            #print(entity_name, split_c, type_c)
            if type_c=="B":
                label_phrase_counter[entity_name]+=label_counter[c]
                label_word_counter[entity_name]+=label_counter[c]
                word_count+=label_counter[c]
                entities_count+=label_counter[c]
            elif type_c=="I":
                label_word_counter[entity_name]+=label_counter[c]

        result={}
        result["label_phrase_counter"]=label_phrase_counter
        result["word_count"]=word_count
        result["entity_count"]=entities_count
        result["label_word_counter"]=label_word_counter
        return result


    def Read_File(self, ip_file):
        list_of_sentence_words_in_file=[]
        list_of_sentence_labels_in_file=[]
        current_sent_words=[]
        current_sent_labels=[]

        for line in open(ip_file):
            line=line.strip()
            if line=="":
                list_of_sentence_words_in_file.append(current_sent_words)
                list_of_sentence_labels_in_file.append(current_sent_labels)
                current_sent_words=[]
                current_sent_labels=[]
                continue


            (word, gold_label)= line.split("\t")
            current_sent_words.append(word)
            current_sent_labels.append(gold_label)

        return (list_of_sentence_words_in_file, list_of_sentence_labels_in_file)















