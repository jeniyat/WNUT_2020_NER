# WNUT 2020: Named Entity Extraction from wet lab protocols


WNUT 2020 coduct shared task on the wet lab protocol data. All of the protocols were collected from [protocols.io](https://www.protocols.io/) using their public APIs. The full protocols dump is also available in json format their [github repository](https://github.com/protocolsio/protocols). For this shared task we provide the annotation of 622 protocols. The brat styled annotated protocols can be visulalized in: http://bit.ly/WNUT2020



## Data
Wet Lab Protocol(WLP) dataset annotations were created in brat and are stored in both StandOff and CoNLL format in the [data directory](./data/Readme.md).


## Baselines

We provided a feature based Linear CRF tagger for the [Named Entity Recognition Task](./code/baseline_CRF/).


## Evaluation

The participants are required to produce prediction as [StandOff format](../../data/Readme.md##-The-standoff-format:) which will be compared with the gold data using the [evalution script](./code/eval/).


## RELEVANT PAPERS 

 Paper about the dataset:
   
	@inproceedings{kulkarni2018wetlab,
	  author     = {Kulkarni, Chaitanya and Xu, Wei and Ritter, Alan and Machiraju, Raghu},
	  title      = {An Annotated Corpus for Machine Reading of Instructions in Wet Lab Protocols},
	  booktitle = {Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL)},
	  year       = {2018}
	} 

  