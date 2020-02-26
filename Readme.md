WNUT 2020
===============

WNUT 2020 coduct shared task on the wet lab protocol data. All of the protocols were collected from [protocols.io](https://www.protocols.io/) using their public APIs. The full protocols dump is also available in json format their [github repository](https://github.com/protocolsio/protocols).  

Wet Lab Protocol(WLP) dataset annotations were created in brat and are stored in both StandOff and CoNLL format in the  `data` directory.

The brat styled annotated protocols can be visulalized in: http://bit.ly/WNUT2020


Instructions to setup on BRAT:
------------------

To set up a brat server with WLP data follow these steps: 

1. Setting up a brat server by following the instructions from [brat official pag](http://brat.nlplab.org/installation.html)
2. Once your installation is ready, Place the `data` directory under "data" directory of your brat installation.
3. make sure it has the right permissions using chmod: `chmod -R g+rwx data`.
4. You can now access this dataset on your brat installation, through one of the [supported web browsers](http://brat.nlplab.org/supported-browsers.html).

