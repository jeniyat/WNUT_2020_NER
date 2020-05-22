#!/usr/bin/env python
#!/usr/bin/env python

# Script to convert a CoNLL 2002-flavored BIO-formatted entity-tagged
# file into BioNLP ST-flavored standoff and a reconstruction of the
# original text.



import codecs
import os
import re
import sys
import utils


INPUT_ENCODING = "UTF-8"
OUTPUT_ENCODING = "UTF-8"



def quote(s):
    return s in ('"', )


def space(t1, t2, quote_count=None):
    # Helper for reconstructing sentence text. Given the text of two
    # consecutive tokens, returns a heuristic estimate of whether a
    # space character should be placed between them.

    if re.match(r'^[\(]$', t1):
        return False
    if re.match(r'^[.,\)\?\!]$', t2):
        return False
    if quote(t1) and quote_count is not None and quote_count % 2 == 1:
        return False
    if quote(t2) and quote_count is not None and quote_count % 2 == 1:
        return False
    return True


def tagstr(start, end, ttype, idnum, text):
    # sanity checks
    assert '\n' not in text, "ERROR: newline in entity '%s'" % (text)
    assert text == text.strip(), "ERROR: tagged span contains extra whitespace: '%s'" % (text)
    return "T%d\t%s %d %d\t%s" % (idnum, ttype, start, end, text)


def output(infn, output_directory, sentences):
    

    if output_directory is None:
        txtout = sys.stdout
        soout = sys.stdout
    else:
        outfn = os.path.join(
            output_directory,
            os.path.basename(infn))
        opfile_name = outfn.replace("_conll.txt","")
        
        txtout = codecs.open(opfile_name + '.txt', 'w')
        soout = codecs.open(opfile_name + '.ann', 'w')

    offset, idnum = 0, 1

    doctext = ""

    for si, sentence in enumerate(sentences):
        # print(sentences)
        prev_token = None
        curr_start, curr_type = None, None
        quote_count = 0

        for token, ttag, ttype in sentence:

            if curr_type is not None and (ttag != "I" or ttype != curr_type):
                # a previously started tagged sequence does not
                # continue into this position.
                print(tagstr(
                    curr_start, offset, curr_type, idnum, doctext[curr_start:offset]), file=soout)
                idnum += 1
                curr_start, curr_type = None, None

            if prev_token is not None and space(
                    prev_token, token, quote_count):
                doctext = doctext + ' '
                offset += 1

            if curr_type is None and ttag != "O":
                # a new tagged sequence begins here
                curr_start, curr_type = offset, ttype

            doctext = doctext + token
            offset += len(token)

            if quote(token):
                quote_count += 1

            prev_token = token

        # leftovers?
        if curr_type is not None:
            print(tagstr(
                curr_start, offset, curr_type, idnum, doctext[curr_start:offset]), file=soout)
            idnum += 1

        if si + 1 != len(sentences):
            doctext = doctext + '\n'
            offset += 1

    print(doctext, file=txtout)


def process(fn,  output_directory ):
    # print(fn)

    docnum = 1
    sentences = []

    with codecs.open(fn, encoding=INPUT_ENCODING) as f:

        # store (token, BIO-tag, type) triples for sentence
        current = []

        lines = f.readlines()
        # print(lines)
        if len(lines)==0:
            print(fn, "is empty")

        for ln, l in enumerate(lines):
            l = l.strip()

            if re.match(r'^\s*$', l):
                # blank lines separate sentences
                if len(current) > 0:
                    sentences.append(current)
                current = []
                continue
            elif (re.match(r'^===*\s+O\s*$', l) or
                  re.match(r'^-DOCSTART-', l)):
                # special character sequence separating documents
                if len(sentences) > 0:
                    output(fn, output_directory,  sentences)
                sentences = []
                docnum += 1
                continue

            if (ln + 2 < len(lines) and
                re.match(r'^\s*$', lines[ln + 1]) and
                    re.match(r'^-+\s+O\s*$', lines[ln + 2])):
                # heuristic match for likely doc before current line
                if len(sentences) > 0:
                    output(fn, output_directory, sentences)
                sentences = []
                docnum += 1
                # go on to process current normally

            # Assume it's a normal line. The format for spanish is
            # is word and BIO tag separated by space, and for dutch
            # word, POS and BIO tag separated by space. Try both.
            m = re.match(r'^(\S+)\s(\S+)$', l)
            if not m:
                m = re.match(r'^(\S+)\s\S+\s(\S+)$', l)
            assert m, "Error parsing line %d: %s" % (ln + 1, l)
            token, tag = m.groups()

            # parse tag
            m = re.match(r'^([BIO])((?:-[A-Za-z_\-]+)?)$', tag)
            assert m, "ERROR: failed to parse tag '%s' in %s" % (tag, fn)
            ttag, ttype = m.groups()
            if len(ttype) > 0 and ttype[0] == "-":
                ttype = ttype[1:]

            current.append((token, ttag, ttype))

        # process leftovers, if any
        if len(current) > 0:
            sentences.append(current)
        # print(sentences)
        if len(sentences) > 0:
            output(fn, output_directory,  sentences)




if __name__ == "__main__":
    conll_format_test_files = "Conll_Outputs/"
    list_of_test_files = utils.Read_Files_in_Input_Folder(conll_format_test_files)
    standoff_output_directory = "Standoff_Outputs/"
    utils.make_dir_if_not_exists(standoff_output_directory)
    for file_name in list_of_test_files:
        file_values = file_name.split("/")
        
        protocol_name = file_values[-1]

        output_directory= standoff_output_directory


        process(file_name, output_directory)
        # # for line in open(file):
        #     # print(line)
    