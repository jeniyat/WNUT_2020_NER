
This repository contains a feature based basline CRF model for the shared task.

Command to run the model:
```
    python CRF_NER_WLP.py

```

This will output the model performance on the test data and create CoNLL format combined prediction file `"prediction.txt"`.

This will also generate a directory named `Conll_Outputs` which will contain separate predictions for all the test files in conll format. To convert it to standoff format run the following command:


```
    python conll2standoff.py

```