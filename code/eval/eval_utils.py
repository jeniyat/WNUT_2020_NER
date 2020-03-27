from collections import Counter
import json

import ftfy

import sys, os
import re
from glob import glob
from nltk import word_tokenize

sys.path.insert(1, '../scripts/convert_standoff_conll_ner/')
import anntoconll_wlp



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


def preprocess_data_to_merge(input_standoff_folder_gold, output_conll_folder_gold, output_conll_file_gold,
    input_standoff_folder_pred, output_conll_folder_pred, output_conll_file_pred):
    
    anntoconll_wlp.convert_standoff_conll_single_file(input_standoff_folder_pred, output_conll_folder_pred, output_conll_file_pred)
    anntoconll_wlp.convert_standoff_conll_single_file(input_standoff_folder_gold, output_conll_folder_gold, output_conll_file_gold)



class Fix_Char_Code:
    """docstring for Fix_Char_Code"""
    def __init__(self):
        pass

    def Get_List_of_Labels(self, tokenized_word_list_len, main_label):
        if main_label=="O":
            new_label="O"
        elif main_label[0]=="B":
            new_label=main_label.replace("B-","I-")
        else:
            new_label= main_label

        new_label_list=[main_label]
        for i in range(tokenized_word_list_len-1):
            new_label_list.append(new_label)
        # print(tokenized_word_list_len, main_label, new_label_list)
        return new_label_list

    def Fix_Word_Label(self, word, gold_label):
        if "&zwnj" in word or "&nbsp" in word or "&amp" in word:
            return ([word], [gold_label], False)

        fixed_word = ftfy.fix_text(word)
        #the following line is found from error analysis over the fixed encoding by finding  && in the text file

        fixed_word=fixed_word.replace("´","'").replace("ÂŁ","£").replace('Ăż','ÿ').replace('Âż','¿').replace('ÂŹ','¬').replace('รก','á').replace("â","†").replace("`ĚN","`̀N")
        modified=True
        if fixed_word==word:
            modified = False
            return ([fixed_word], [gold_label], modified)
        fixed_word_tokenized= word_tokenize(fixed_word)
        # try:
        #     fixed_word_tokenized= ark_twokenize.tokenizeRawTweetText(fixed_word)

        # except stokenizer.TimedOutExc as e:
        #     try:
        #         fixed_word_tokenized= ark_twokenize.tokenizeRawTweetText(fixed_word)
        #     except Exception as e:
        #         print(e)
        if len(fixed_word_tokenized)==2 and fixed_word_tokenized[0]=="'":
            return ([fixed_word], [gold_label],modified)
        
        # print(word, fixed_word, fixed_word_tokenized)
        new_gold_label_list = self.Get_List_of_Labels(len(fixed_word_tokenized), gold_label)
        
        return (fixed_word_tokenized, new_gold_label_list, modified)

    def Read_File(self, ip_file, op_file_name):
        # output_file_name = ip_file[:-4]+"_char_embed_resolved.txt"
        fout= open(op_file_name,'w')

        
        

        for line in open(ip_file):
            if line.strip()=="":
                fout.write(line)
                continue

            line_values=line.strip().split()
            gold_word=line_values[0]
            gold_label=line_values[1]

            (new_tokenized_word_list, new_gold_label_list,  if_modified) = self.Fix_Word_Label(gold_word, gold_label)
            # if if_modified:
            #   print(line.strip())
            #   print(new_tokenized_word_list)
            #   print("----")
            # print(new_tokenized_word_list, new_gold_label_list, new_raw_label_list)
            for word_iter in range(len(new_tokenized_word_list)):
                word = new_tokenized_word_list[word_iter]
                if word.strip()=="":
                    continue

                gold_label = new_gold_label_list[word_iter]

                if word == "'s":
                    gold_label="O"

                
                op_line = word+"\t"+gold_label+"\n"
                # print(op_line)
                fout.write(op_line)



















