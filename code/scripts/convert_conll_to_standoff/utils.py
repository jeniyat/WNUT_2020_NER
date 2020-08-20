from collections import Counter


import sys, os
import re
from glob import glob
from nltk import word_tokenize

sys.path.append('../../scripts/convert_standoff_conll_ner/')
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

















