# WNUT 2020


WNUT 2020 coduct shared task on the wet lab protocol data. All of the protocols were collected from [protocols.io](https://www.protocols.io/) using their public APIs. The full protocols dump is also available in json format their [github repository](https://github.com/protocolsio/protocols). For this shared task we started with 622 protocols from [Kulkarni et al.](https://www.aclweb.org/anthology/N18-2016/) and added the missing annotations. The brat styled annotated protocols can be visulalized in: http://bit.ly/WNUT2020



## Data
Wet Lab Protocol(WLP) dataset annotations were created in brat and are stored in both StandOff and CoNLL format in the  [data directory](./data/Readme.md).


## Baselines

## Evaluation

The participants are required to produce prediction as [StandOff format](../../data/Readme.md##-The-standoff-format:) which will be compared with the gold data using the [evalution script](./code/eval/Readme.md).
