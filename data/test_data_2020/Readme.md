This folder contains the surprised test data for the WNUT-2020 shared task on "Entity Recognition over Wet Lab Protocols". 

Currently the data of this folder do not contain any gold labels. All `*.ann` file are empty and all the `*_conll.txt` files have all labels as 'O'. The gold labels for this dataset will be released after the evalauation period.



# Submission of System Output
 
You need to submit your model prediction on these new data by  **September 4, 2020 (AoE)**, with a brief description (<= 280 characters) of your model  using the [output submission the form](https://forms.gle/xMjAVnN4YgNS7LpSA). 
 
 
## Submission Instructions

You are required to submit your model predictions in a zip file. The name of the zipped file must be in the following format:

```
	<team_name>.zip  
	[e.g., ‘OSU_NLP’ team must submit the predictions in ‘OSU_NLP.zip’]
```

The zipped file should contain the predictions on these 111 protocols. You can submit your prediction in any format: [conll](../../data#the-conll-format) / [standoff](../../data#the-standoff-format).


If you choose to submit predictions as standoff format below is the required directory structure. 

```
OSU_NLP/
	├── protocol_0623.ann
	├── protocol_0623.txt
	├── protocol_0624.ann
	├── protocol_0624.txt
	├── protocol_0625.ann
	├── protocol_0625.txt
	├── protocol_0626.ann
	├ ….
```

If you choose to submit predictions as conll format below is the required directory structure. 

```
OSU_NLP/
	├── protocol_0623_conll.txt
	├── protocol_0624_conll.txt
	├── protocol_0625_conll.txt
	├── protocol_0626_conll.txt
	├  ...
 
 
```