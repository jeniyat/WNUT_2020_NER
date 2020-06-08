# The baseline NER:

We provided a simple Liner CRF model in the [baseline_CRF directory](./baseline_CRF/Readme.md). It utilized simple gazetters and hand-crafted feature to predict the entities from the test data.

# The evaluation system:

We provided the NER evalutation scipt in the [eval directory](./eval/Readme.md). To run the evalutaiton system the participants are required to produce entity sequence for each sentence and submit the predictions as either [StandOff format](../data/Readme.md##-The-standoff-format:) or [CoNLL format](../data/Readme.md##-The-conll-format:).

# The utility scripts:

We provided utility scripts to covert the StandOff format file to CoNLL format and vice versa in the [scripts directory](./scripts/Readme.md). 

# Requirements:

All the codes are written in python 3. The following python modules are required by the scripts provided in this code-base.


```
sklearn-crfsuite
nltk
codecs
io
re
os
sys
glob
shutil
argparse

```
