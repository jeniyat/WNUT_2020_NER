#!/usr/bin/env python

# Convert text and standoff annotations into CoNLL format.

from __future__ import print_function

import os
import re
import sys
from collections import namedtuple
from io import StringIO
from os import path

import shutil
import glob

from sentencesplit import sentencebreaks_to_newlines

# assume script in brat tools/ directory, extend path to find sentencesplit.py
sys.path.append(os.path.join(os.path.dirname(__file__), '../server/src'))
sys.path.append('.')

options = None

EMPTY_LINE_RE = re.compile(r'^\s*$')
CONLL_LINE_RE = re.compile(r'^\S+\t\d+\t\d+.')
from nltk import word_tokenize
 


from map_text_to_char import map_text_to_char  #JT: Dec 6
class FormatError(Exception):
    pass


def argparser():
    import argparse

    ap = argparse.ArgumentParser(description='Convert text and standoff ' +
                                 'annotations into CoNLL format.')
    ap.add_argument('-a', '--annsuffix', default="ann",
                    help='Standoff annotation file suffix (default "ann")')
    ap.add_argument('-c', '--singleclass', default=None,
                    help='Use given single class for annotations')
    ap.add_argument('-n', '--nosplit', default=True, action='store_true',
                    help='No sentence splitting')
    ap.add_argument('-o', '--outsuffix', default="conll",
                    help='Suffix to add to output files (default "conll")')
    ap.add_argument('-v', '--verbose', default=False, action='store_true',
                    help='Verbose output')
    # ap.add_argument('text', metavar='TEXT', nargs='+',
    #                 help='Text files ("-" for STDIN)')
    return ap


def read_sentence(f):
    """Return lines for one sentence from the CoNLL-formatted file.

    Sentences are delimited by empty lines.
    """

    lines = []
    for l in f:
        lines.append(l)
        if EMPTY_LINE_RE.match(l):
            break
        if not CONLL_LINE_RE.search(l):
            raise FormatError(
                'Line not in CoNLL format: "%s"' %
                l.rstrip('\n'))
    return lines


def strip_labels(lines):
    """Given CoNLL-format lines, strip the label (first TAB-separated field)
    from each non-empty line.

    Return list of labels and list of lines without labels. Returned
    list of labels contains None for each empty line in the input.
    """

    labels, stripped = [], []

    labels = []
    for l in lines:
        if EMPTY_LINE_RE.match(l):
            labels.append(None)
            stripped.append(l)
        else:
            fields = l.split('\t')
            labels.append(fields[0])
            stripped.append('\t'.join(fields[1:]))

    return labels, stripped


def attach_labels(labels, lines):
    """Given a list of labels and CoNLL-format lines, affix TAB-separated label
    to each non-empty line.

    Returns list of lines with attached labels.
    """

    assert len(labels) == len(
        lines), "Number of labels (%d) does not match number of lines (%d)" % (len(labels), len(lines))

    attached = []
    for label, line in zip(labels, lines):
        empty = EMPTY_LINE_RE.match(line)
        assert (label is None and empty) or (label is not None and not empty)

        if empty:
            attached.append(line)
        else:
            attached.append('%s\t%s' % (label, line))

    return attached


# NERsuite tokenization: any alnum sequence is preserved as a single
# token, while any non-alnum character is separated into a
# single-character token. TODO: non-ASCII alnum.
TOKENIZATION_REGEX = re.compile(r'([0-9a-zA-Z]+|[^0-9a-zA-Z])')

NEWLINE_TERM_REGEX = re.compile(r'(.*?\n)')


def text_to_conll(f):
    """Convert plain text into CoNLL format."""
    global options
    # print(f)
    if options.nosplit:
        sentences = f.readlines()
        # print(sentences)
    else:
        sentences = []
        for l in f:
            l = sentencebreaks_to_newlines(l)
            
            sentences.extend([s for s in NEWLINE_TERM_REGEX.split(l) if s])

    lines = []

    offset = 0
    # print(sentences)
    for s in sentences:
        nonspace_token_seen = False
        # print(s)
        
        # tokens = s.split(" ")
        tokens =  word_tokenize(s)
        
        
        token_w_pos = map_text_to_char(s, tokens, offset)
        # print("token_w_pos: ",token_w_pos)

        for(t, pos) in token_w_pos:
            if not t.isspace():
                l1=['O', pos, pos + len(t), t]
                lines.append(l1)
                # print(l1)
        
        lines.append([])

        offset+=len(s)


        # tokens = [t for t in TOKENIZATION_REGEX.split(s) if t] # JT : Dec 6
        # for t in tokens:
        #     if not t.isspace():
        #         lines.append(['O', offset, offset + len(t), t])
        #         nonspace_token_seen = True
        #     offset += len(t)

        # # sentences delimited by empty lines
        # if nonspace_token_seen:
        #     lines.append([])

    # add labels (other than 'O') from standoff annotation if specified
    if options.annsuffix:
        textbounds, dict_of_entity, list_of_relns=get_annotations(f.name)
        lines = relabel(lines, textbounds , dict_of_entity, list_of_relns, f)
        # print(lines)

    # lines = [[l[0], str(l[1]), str(l[2]), l[3]] if l else l for l in lines] #JT: Dec 6
    lines = [[l[3],l[0]] if l else l for l in lines] #JT: Dec 6
    # lines = [[l[3],l[0],l[4],l[5],l[6]] if l else l for l in lines] #JT: Dec 6
    
    return StringIO('\n'.join(('\t'.join(l) for l in lines)))


def Find_All_Reln(id_,  list_of_relns):
    type_id_counter = {}
    list_of_relns_w_id =[]

    for l in list_of_relns:
        type_ = l["type"]
        arg1= l["arg1"]
        arg2 = l["arg2"]
        # print(type_, arg1, arg2)
        if type_ not in type_id_counter:
            type_id_counter[(type_, arg1, arg2)]=0
        type_id_counter[(type_, arg1, arg2)]+=1

        type_w_id = type_+ str(type_id_counter[(type_, arg1, arg2)])
        reln = {}

        reln["arg1"]= l["arg1"]
        reln["arg2"] = l["arg2"]
        reln["type"]=type_w_id

        list_of_relns_w_id.append(reln)
        
        

    all_relations_w_id = []
    for reln in list_of_relns_w_id:
        type_ = reln["type"]
        arg1 = reln["arg1"]
        arg2 = reln["arg2"]
        # print(type_, arg1, arg2)
        if id_==arg1:
            l = (type_, 1)
            all_relations_w_id.append(l)
        if id_==arg2:
            l = (type_, 2)
            all_relations_w_id.append(l)
    # print(all_relations_w_id)
    return all_relations_w_id


def relabel(lines, annotations, dict_of_entity, list_of_relns, file_name):
    # print("lines: ",lines)
    # print("annotations", annotations)
    global options
    # print(dict_of_entity)
    # TODO: this could be done more neatly/efficiently
    offset_label = {}

    for tb in annotations:
        # print(tb)
        for i in range(tb.start, tb.end):
            if i in offset_label:
                print("Warning: overlapping annotations in ", file=sys.stderr)
            offset_label[i] = tb
    # print(offset_label)
    prev_label = None
    for i, l in enumerate(lines):
        if not l:
            prev_label = None
            continue
        tag, start, end, token = l
        # print(l)

        # TODO: warn for multiple, detailed info for non-initial
        label = None
        id_=None
        if (start, end) in dict_of_entity:
            tb, id_ = dict_of_entity[(start, end)]
            # print(id_)
        all_relations_w_id = []
        if id_:
            all_relations_w_id = Find_All_Reln(id_,  list_of_relns)
            # print(all_relations_w_id)
        for o in range(start, end):

            if o in offset_label:
                if o != start:
                    pass
                    # print('Warning: annotation-token boundary mismatch: "%s" --- "%s"' % (
                    #     token, offset_label[o].text), file=sys.stderr)
                label = offset_label[o].type
                break
        tag_prefix = ""
        if label is not None:
            if label == prev_label:
                tag = 'I-' + label
                tag_prefix= "I-"
            else:
                tag = 'B-' + label
                tag_prefix= "B-"
        prev_label = label
        relation = "[]"
        arg1 = "[]"
        arg2 = "[]"
        if len(all_relations_w_id)>0:
            # print(all_relations_ws_id)
            relation = "[ "
            arg1 = "[ "
            arg2 = "[ "
            for rel_info in all_relations_w_id:
                (type_, arg_num)= rel_info
                arg_num= int(arg_num)
                type_w_tag_prefix = tag_prefix+type_
                # print(type_w_tag_prefix, arg_num)

                relation += type_w_tag_prefix + ","
                if arg_num==1:
                    arg2 += "_ " + ","
                    arg1 += tag_prefix+"Arg1" + ","

                if arg_num==2:
                    arg1 += "_" + ","
                    arg2 += tag_prefix+"Arg2" + ","

            relation=relation[:-1]
            arg1=arg1[:-1]
            arg2=arg2[:-1]
            relation += " ]"
            arg1 += " ]"
            arg2 += " ]"




        lines[i] = [tag, start, end, token, relation, arg1, arg2]
        # print(lines[i])

    # optional single-classing
    if options.singleclass:
        for l in lines:
            if l and l[0] != 'O':
                l[0] = l[0][:2] + options.singleclass

    return lines


def process(f):
    return text_to_conll(f)


def process_files_v1(files):
    global options

    nersuite_proc = []

    try:
        for fn in files:
            # print("now_processing", fn)
            try:
                if fn == '-':
                    lines = process(sys.stdin)
                else:
                    with open(fn, 'rU') as f:
                        lines = process(f)

                # TODO: better error handling
                if lines is None:
                    raise FormatError

                if fn == '-' or not options.outsuffix:
                    sys.stdout.write(''.join(lines))
                else:
                    ofn = path.splitext(fn)[0] + options.outsuffix
                    with open(ofn, 'wt') as of:
                        of.write(''.join(lines))

            except BaseException:
                # TODO: error processing
                raise
    except Exception as e:
        for p in nersuite_proc:
            p.kill()
        if not isinstance(e, FormatError):
            raise   

def process_files(files, output_directory_main):
    global options
    # print("phase_name: ",phase_name)
    output_directory = output_directory_main
    try:
        os.mkdir(output_directory)
    except Exception as e:
        pass

    

    nersuite_proc = []

    
    for fn in files:
        # print("now_processing: ",fn)

        with open(fn, 'rU') as f:
            lines = text_to_conll(f)
            # print(lines)
            # TODO: better error handling
            lines_updated = []
            prev_word = ""
            for line in lines:
                if line.strip()=="":
                    lines_updated.append(line)

                if len(line.strip().split())==2:
                    prev_word=""
                    lines_updated.append(line)

                elif line.strip()=="O" and prev_word!="":
                    opline= prev_word+"\t"+"O"+"\n"
                    lines_updated.append(opline)

                elif line.strip().startswith("I-") and prev_word!="":
                    opline= prev_word+"\t"+line.strip()+"\n"
                    lines_updated.append(opline)

                elif line.strip().startswith("B-") and prev_word!="":
                    opline= prev_word+"\t"+line.strip()+"\n"
                    lines_updated.append(opline)
                else:
                    prev_word=line.strip()



            if lines is None:
                print("Line is None")
                continue
            file_name=fn.split("/")[-1][0:-4]
            ofn = output_directory+file_name+"_" +options.outsuffix.replace(".","")+".txt"
            with open(ofn, 'wt') as of:
                of.write(''.join(lines_updated))
                of.write("\n\n\n")

        
   

# start standoff processing


TEXTBOUND_LINE_RE1 = re.compile(r'^T\d+\t')
TEXTBOUND_LINE_RE2 = re.compile(r'^R\d+\t')
TEXTBOUND_LINE_RE3 = re.compile(r'^E\d+\t')

Textbound = namedtuple('Textbound', 'start end type text')


def parse_textbounds(f):
    """Parse textbound annotations in input, returning a list of Textbound."""

    textbounds = []
    dict_of_entity = {}
    list_of_relns = []

    for l in f:
        l = l.rstrip('\n')

        if TEXTBOUND_LINE_RE3.search(l):    
            try:
                # print(l.strip().split('\t'))
                id_, act_ = l.strip().split('\t')
                # print("----------------",act_.split())
                type_ = "Action" 
                arg_1_id, arg_2_id = act_.split()

                
                arg_1_id = arg_1_id.replace("Action:","")
                arg_2_id = arg_2_id.replace("Acts-on:","")
                
                # print(type_, arg_1_id, arg_2_id)
                reln_dict = {}
                reln_dict["type"]=type_
                reln_dict["arg1"]=arg_1_id
                reln_dict["arg2"]=arg_2_id
                list_of_relns.append(reln_dict)
                # start, end = int(start), int(end)
                # print(id_, type_offsets, text)
                # # textbounds.append(Textbound(start, end, type_, text))
            except Exception as e:
                continue

        if TEXTBOUND_LINE_RE2.search(l):    
            try:
                # print(l.strip().split('\t'))
                id_, rel_ = l.strip().split('\t')
                type_, arg_1_id, arg_2_id = rel_.split()
                type_ = type_.replace("_","-")
                # print(type_)
                
                arg_1_id = arg_1_id.replace("Arg1:","")
                arg_2_id = arg_2_id.replace("Arg2:","")



                reln_dict = {}
                reln_dict["type"]=type_

                reln_dict["arg1"]=arg_1_id
                reln_dict["arg2"]=arg_2_id
                list_of_relns.append(reln_dict)
                
                # print(type_, arg_1_id, arg_2_id)
                # start, end = int(start), int(end)
                # print(id_, type_offsets, text)
                # # textbounds.append(Textbound(start, end, type_, text))
            except Exception as e:
                # print("*********************************",l)
                print(f)
                print(e)


        if TEXTBOUND_LINE_RE1.search(l):    
            try:
                line_values = l.strip().split('\t')
                id_ = line_values[0]
                type_offsets = line_values[1]
                text = " ".join(l[1:])
                # id_, type_offsets, text = l.split('\t')
                type_, start, end = type_offsets.split()
                type_ = type_.replace("_","-")
                start, end = int(start), int(end)
                # print(id_, type_offsets, text)
                dict_of_entity[(start, end)]= (Textbound(start, end, type_, text),id_)
                textbounds.append(Textbound(start, end, type_, text))
            except Exception as e:
                # print("*********************************",l)
                print(f, e, l)


        
        
        

        
    # print(dict_of_entity)
    # print(list_of_relns)
    return textbounds, dict_of_entity, list_of_relns


def eliminate_overlaps(textbounds, fn):
    eliminate = {}

    # TODO: avoid O(n^2) overlap check
    for t1 in textbounds:
        for t2 in textbounds:
            if t1 is t2:
                continue
            if t2.start >= t1.end or t2.end <= t1.start:
                continue
            # eliminate shorter
            if t1.end - t1.start > t2.end - t2.start:
                print("Eliminate %s due to overlap with %s" % (
                    t2, t1), file=sys.stderr)
                print(fn)
                eliminate[t2] = True
            else:
                print("Eliminate %s due to overlap with %s" % (
                    t1, t2), file=sys.stderr)
                eliminate[t1] = True
                print(fn)

    return [t for t in textbounds if t not in eliminate]


def get_annotations(fn):
    global options

    annfn = path.splitext(fn)[0] + options.annsuffix

    with open(annfn, 'rU') as f:
        textbounds, dict_of_entity, list_of_relns = parse_textbounds(f)

    textbounds = eliminate_overlaps(textbounds, fn)
    

    return textbounds, dict_of_entity, list_of_relns

# end standoff processing

def Read_Main_Input_Folder(input_folder):
    start_dir = input_folder
    # start_dir = "/Users/jeniya/Desktop/NER_RECOG_SW/brat-v1.3_Crunchy_Frog/data/so_annotated_data/selected/phase_01_01"
    pattern   = "*.txt"
    file_location_list=[]
    # print(start_dir)
    for dir,_,_ in os.walk(start_dir):
        file_location_list.extend(glob.glob(os.path.join(dir,pattern))) 
    # print(file_location_list)
    # for txt_file_loc in file_location_list:
    #     print("txt_file_loc: ",txt_file_loc)
    #     #print("phase_name: ", phase_name)
    #     try:
    #         ann_file_loc=txt_file_loc[:-4]+".ann"
            
    #     except:
    #         continue
    return file_location_list


def covert_standoff_to_conll(input_folder_main= "checked_annotations_training/", output_folder = 'Conlll_Output_ANN/' ):
    
    # print(input_folder_main, output_folder)
    global options
    options = argparser().parse_args("")

    # make sure we have a dot in the suffixes, if any
    if options.outsuffix and options.outsuffix[0] != '.':
        options.outsuffix = '.' + options.outsuffix
    if options.annsuffix and options.annsuffix[0] != '.':
        options.annsuffix = '.' + options.annsuffix

    list_of_files=Read_Main_Input_Folder(input_folder_main)
    # print(list_of_files)
    process_files(list_of_files, output_folder)



def merge_files(input_folder, output_file):
    all_files = glob.glob(input_folder+"*.txt")
    # print(len(all_files), input_folder, output_file)
    fout = open(output_file,'w')


    for file in all_files:

        for line in open(file):
            fout.write(line)

    fout.close()




def convert_standoff_conll_single_file(input_standoff_folder, output_conll_folder, output_file):
    if not os.path.exists(output_conll_folder):
        os.makedirs(output_conll_folder)
    else:
        shutil.rmtree(output_conll_folder)
    covert_standoff_to_conll(input_folder_main= input_standoff_folder, output_folder = output_conll_folder)



    merge_files(output_conll_folder, output_file)

if __name__ == "__main__":
    input_folder_main = "../../../data/test_data/Standoff_Format/"
    output_folder = "../../../data/test_data/Conll_Format/"
    covert_standoff_to_conll(input_folder_main, output_folder)

    input_folder_main = "../../../data/dev_data/Standoff_Format/"
    output_folder = "../../../data/dev_data/Conll_Format/"
    covert_standoff_to_conll(input_folder_main, output_folder)

    input_folder_main = "../../../data/train_data/Standoff_Format/"
    output_folder = "../../../data/train_data/Conll_Format/"
    covert_standoff_to_conll(input_folder_main, output_folder)






