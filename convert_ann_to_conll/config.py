"""File containing various constants used throughout the program."""
import os

# directory of the config file
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

ARTICLES_FOLDERPATH = os.path.join(CURRENT_DIR, "WLP-Dataset")

TRAIN_ARTICLES_PATH = os.path.join(CURRENT_DIR, "WLP-Dataset/train")

DEV_ARTICLES_PATH = os.path.join(CURRENT_DIR, "WLP-Dataset/dev")

TEST_ARTICLES_PATH = os.path.join(CURRENT_DIR, "WLP-Dataset/test")

PUBMED_AND_PMC_W2V_BIN = os.path.join(CURRENT_DIR, "preprocessing/PubMed-and-PMC-w2v.bin")

EMBEDDING_DIM = 200
MAX_SEQUENCE_LENGTH = 100
PF_EMBEDDING_DIM = 5

BASE_MODEL = "bilstm"

NUMBER_OF_VALIDATION_SAMPLES = 200

LEARNING_RATE = 0.5

LSTM_HIDDEN_SIZE = 200

LSTM_OUT_SIZE = 200

MAX_EPOCH = 500

VERBOSE = False

BATCH_SIZE = 16

POSITIVE_LABEL = 'Action'
NEG_LABEL = 'O'

CATEGORIES = None

OOP_FILEPATH = os.path.join(CURRENT_DIR, "preprocessing/oop.txt")
OOV_FILEPATH = os.path.join(CURRENT_DIR, "preprocessing/oov.txt")

MODEL_SAVE_DIR = os.path.join(CURRENT_DIR, "results/models")

FILTER_ALL_NEG = False

MAX_EPOCH_IMP = 20

MIN_EPOCH_IMP = 5

PER = (60, 20, 20)

TRAIN_PER = 100  # how much of the train dataset should be used in training.

LM_HIDDEN_SIZE = 200

LM_MAX_VOCAB_SIZE = 7500  # next try 3000

WORD_VOCAB = 0

LM_GAMMA = 0.1

REPLACE_DIGITS = True

PUBMED_VOCAB_FILE = os.path.join(CURRENT_DIR, "preprocessing/pubmed_vocab.txt")

CHAR_EMB_DIM = 50

CHAR_RECURRENT_SIZE = 200

CHAR_VOCAB = 0
CHAR_LEVEL = "None"

POS_EMB_DIM = 50
POS_VOCAB = None

REL_EMB_DIM = 50
REL_VOCAB = None

WORD_START = "<w>"
WORD_END = "</w>"
SENT_START = "<s>"
SENT_END = "</s>"

LOWERCASE = True
UNK = "<unk>"
MIN_WORD_COUNT = 1  # minimum word count for it to be part of vocabulary

RANDOM_TRAIN = True

BRAT_DIR = os.path.join(CURRENT_DIR, "results/brat_results")

CONF_DIR = os.path.join(BRAT_DIR, "confs")

PRED_BRAT_FULL = "results/brat_results/pred/brat_out"
TRUE_BRAT_FULL = "results/brat_results/true/brat_out"

PRED_BRAT_INC = "results/brat_results/pred/brat_inc_out"
TRUE_BRAT_INC = "results/brat_results/true/brat_inc_out"

CLIP = None

BEST_MODEL_SELECTOR = ["dev_conll_f", "dev_macro_f"]

RESULT_FILE = os.path.join(CURRENT_DIR, "test_results.txt")

TEXT_RESULT_DIR = os.path.join(CURRENT_DIR, "results/text_results")

CSV_RESULT_DIR = os.path.join(CURRENT_DIR, "results/csv_results")


DEP_PICKLE_DIR = os.path.join(CURRENT_DIR, "results/pickles/dep_graphs")
POS_PICKLE_DIR = os.path.join(CURRENT_DIR, "results/pickles/pos_tags")
POS_GENIA_DIR = os.path.join(CURRENT_DIR, "results/pickles/pos_genia_tags")
DEP_GENIA_DIR = os.path.join(CURRENT_DIR, "results/pickles/dep_genia_graphs")
PARSE_PICKLE_DIR = os.path.join(CURRENT_DIR, "results/pickles/parse_trees")
REL_PICKLE_DIR = os.path.join(CURRENT_DIR, "results/pickles/relations")

DB = os.path.join(CURRENT_DIR, "results/pickles/datasets.p")
DB_MAXENT = os.path.join(CURRENT_DIR, "results/pickles/dataset_maxent.p")
DB_MAXENT_WITH_PARSETREES = os.path.join(CURRENT_DIR, "results/pickles/dataset_maxent_parse_trees.p")
# Number of windows to use during training (offset is COUNT_WINDOWS_TEST, i.e. test windows will
# be loaded first)
COUNT_WINDOWS_TRAIN = 10000

# Number of windows to use during testing
COUNT_WINDOWS_TEST = 0

# Label for any word that has no named entity label
NO_NE_LABEL = "O"

# labels to accept when parsing data, all other labels will be treated as normal text
# e.g. in "Manhatten/NY" the "NY" will not be treated as a label and the full token
# "Manhatten/NY" will be loaded as one word
LABELS = ["Action", "Reagent", "Location", "Device", "Mention", "Method", "Amount", "Concentration", "Size", "Time",
          "Temperature", "pH", "Speed", "Seal", "Modifier", "Generic-Measure", "Numerical", "Measure-Type"]

RELATIONS = ["Acts-on", "Site", "Creates", "Using", "Count", "Measure-Type-Link", "Coreference-Link", "Mod-Link",
             "Setting", "Measure", "Meronym", "Or", "Of-Type"]

BIO_LABELS = [""]

FEATURE_SIZE = 0

POS_FEATURE = "No"
DEP_LABEL_FEATURE = "No"
DEP_WORD_FEATURE = "No"

FEAT_L2_REG = 0.3

SCRIPT_DIR = os.path.join(CURRENT_DIR, "scripts/jobs")

DB_200_WITH_FEATURES = os.path.join(CURRENT_DIR, "200_dataset_with_features.p")

TRAIN_WORD_EMB = False

VIS_SAVE_DIR = os.path.join(CURRENT_DIR, "visualization/results")

PLOT_SAVE_DIR = os.path.join(CURRENT_DIR, "results/plots")

BATCH_TYPE = "multi"

NEG_REL_LABEL = "0"

# SKIP_FILES = ["/Users/chaitanyakulkarni/Work/pHd/action-sequence-labeler/simple_input/protocol_29"]
SKIP_FILES = []
def ver_print(string, value):
    if VERBOSE:
        print(string + ':\n {0}'.format(value))