#!/usr/bin/env python3
from collections import Counter

import sys, os, shutil
import re
from glob import glob
from os import listdir
from os.path import isfile, join
from nltk import word_tokenize

sys.path.insert(1, '../scripts/convert_standoff_conll_ner/')
sys.path.insert(1, '../scripts/convert_conll_to_standoff/')
import anntoconll_wlp
import conll2standoff



def save_perf_in_tex(table_dict,op_file, caption="", ):
    fout = open(op_file,'w')

    print("\\begin{table}[htbp]", file = fout)
    print("\\centering", file = fout)
    print("\\begin{tabular}{|",end='', file = fout)
    for i in range(len(table_dict["header"])):
        print("c|",end='', file = fout)
    print("}", file = fout)

    header=" & ".join(table_dict["header"])+"\\\\"
    print("\\hline", file = fout)
    print(header, file = fout)
    print("\\hline", file = fout)

    for row in table_dict["rows"]:
        row_=[str(x).replace("_"," ").replace("%","\\%") for x in row]
        row_str=" & ".join(row_)+"\\\\"
        print(row_str, file = fout)
        print("\\hline", file = fout)

    print("\\end{tabular}", file = fout)
    print("\\caption{"+caption+"}", file = fout)

    print("\\end{table}", file = fout)

    print("\n\n\n", file = fout)


    fout.close()

def tolatex(table_dict,caption=""):
    print("\n\n\n")
    print("\\begin{table}[htbp]")
    print("\\centering")
    print("\\begin{tabular}{|",end='')
    for i in range(len(table_dict["header"])):
        print("c|",end='')
    print("}")
    header=" & ".join(table_dict["header"])+"\\\\"
    print("\\hline")
    print(header)
    print("\\hline")
    for row in table_dict["rows"]:
        row_=[str(x).replace("_"," ").replace("%","\\%") for x in row]
        row_str=" & ".join(row_)+"\\\\"
        print(row_str)
        print("\\hline")
    #print("\\hline")
    print("\\end{tabular}")
    print("\\caption{"+caption+"}")
    #print("\\label{tab:-----}")
    print("\\end{table}")

    print("\n\n\n")



def Read_txt_Files_in_Input_Folder(input_folder):
    start_dir = input_folder
    # start_dir = "/Users/jeniya/Desktop/NER_RECOG_SW/brat-v1.3_Crunchy_Frog/data/so_annotated_data/selected/phase_01_01"
    pattern   = "*.txt"
    file_location_list=[]
    for dir,_,_ in os.walk(start_dir):
        file_location_list.extend(glob(os.path.join(dir,pattern)))

    # print("total prtocols in : ", input_folder," = ", len(file_location_list))
    return sorted(file_location_list)

def Read_all_files_in_Input_Folder(input_folder):
    start_dir = input_folder
    # start_dir = "/Users/jeniya/Desktop/NER_RECOG_SW/brat-v1.3_Crunchy_Frog/data/so_annotated_data/selected/phase_01_01"
    onlyfiles = [f for f in listdir(start_dir) if isfile(join(start_dir, f))]

    return sorted(onlyfiles)


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
    


def find_prediction_file_format(output_folder):
    list_of_files = Read_all_files_in_Input_Folder(output_folder)
    # print(list_of_files)
    if any(".ann" in s for s in list_of_files):
        return "Standoff"
    else:
        return "Conll"


def read_conll_file(file_name):
    all_lines = []
    current_line = []

    for line in open(file_name):
        if line.strip()=="":
            if len(current_line)!=0:
                all_lines.append(current_line)
                current_line=[]
            continue

        line_values = line.strip().split()
        if len(line_values)==2:
            current_line.append(line_values)
        else:
            print(line_values, file_name)

    return all_lines

        

def write_to_combined_file(gold_file_loc, pred_file_loc, output_file):

    fout = open(output_file,'a')
    set_gold_lines = []
    pred_lines = []

    all_gold_lines = read_conll_file(gold_file_loc)
    all_pred_lines = read_conll_file(pred_file_loc)

    

    for line_index in range(len(all_gold_lines)):
        gold_sent = all_gold_lines[line_index]
        pred_sent = all_pred_lines[line_index]

        for word_index in range(len(gold_sent)):
            
            gold_word_info = gold_sent[word_index]
            pred_word_info = pred_sent[word_index]

            word = gold_word_info[0]
            gold_label = gold_word_info[1]
            pred_label = pred_word_info[1]

            opline = word + " "+ gold_label+ " "+ pred_label+"\n"

            fout.write(opline)
        fout.write("\n")
            


    fout.close()



def combine_and_merge_gold_pred(input_gold_conll, input_pred_conll):
    # print(input_gold_conll, input_pred_conll)
    all_files = Read_txt_Files_in_Input_Folder(input_gold_conll)

    combined_pred_file = "predictions.txt"
    fout=open(combined_pred_file, 'w')
    fout.close()

    for file in all_files:
        file_name = file.split("/")[-1]
        # print(file_name)
        gold_file_loc = input_gold_conll+file_name
        pred_file_loc = input_pred_conll+file_name

        # print(gold_file_loc, pred_file_loc)
        write_to_combined_file(gold_file_loc, pred_file_loc, combined_pred_file)

    return combined_pred_file

















