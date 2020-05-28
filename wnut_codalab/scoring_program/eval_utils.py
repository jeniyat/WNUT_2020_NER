# -*- coding: utf-8 -*-

#!/usr/bin/env python3
from collections import Counter
import json

import sys, os, shutil
import re
from glob import glob
from nltk import word_tokenize


import anntoconll_wlp
import conll2standoff

import filecmp


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


def copy_text_files(input_standoff_folder_gold, input_standoff_folder_pred):
    
    pattern   = "*.txt"
    start_dir =input_standoff_folder_gold
    txt_file_location_list=[]

    for dir,_,_ in os.walk(start_dir):
        txt_file_location_list.extend(glob(os.path.join(dir,pattern)))

    for file in txt_file_location_list:
        
        shutil.copy2(file,input_standoff_folder_pred)
        
        

        

    


def preprocess_data_to_merge(input_standoff_folder_gold, output_conll_folder_gold, output_conll_file_gold,
    input_standoff_folder_pred, output_conll_folder_pred, output_conll_file_pred):

    # if not os.path.exists(output_conll_folder_gold):
    #     os.makedirs(output_conll_folder_gold)
    # else:
    #     shutil.rmtree(output_conll_folder_gold)

    # anntoconll_wlp.covert_standoff_to_conll(input_folder_main= input_standoff_folder_gold, output_folder = output_conll_folder_gold)

    

    
    anntoconll_wlp.convert_standoff_conll_single_file(input_standoff_folder_gold, output_conll_folder_gold, output_conll_file_gold)

    list_of_test_files_stand_off = Read_Files_in_Input_Folder(output_conll_folder_gold)

    for file_name in list_of_test_files_stand_off:
        file_values = file_name.split("/")
        protocol_name = file_values[-1]
        conll2standoff.process(file_name, input_standoff_folder_gold)


    copy_text_files(input_standoff_folder_gold, input_standoff_folder_pred)


    anntoconll_wlp.convert_standoff_conll_single_file(input_standoff_folder_pred, output_conll_folder_pred, output_conll_file_pred)
    



