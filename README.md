# DatabaseFinalProject

This project will be implementing the Gene Expression Data Management assignment given by Dr. Lin. 

CSI 3335 Fall 19 Group Project – Gene Expression data management. We are developing a tool to keep track of a study of gene expression at the messenger RNA (mRNA) level in different yeast strains. 

* Data input (via GUI) 
  * New experimental conditions and new measurement type.
  * Base information about the sequence.
  * Experiment condition/results for each sequence.
     * Notice there may be many experiments with the same sequence. 
     * Each case need to specify its own condition and its own results.
* Data input (via csv file)
  * The user can supply a name of csv file. It will contains a matrix. Each row (except the first) is a sequence, with the first column its name. Each column (except the first) is a measurement type. The first row (starting from the second column) contain the name for the type. Each cell of the subsequent row contains the value of the measurement for that sequence. However, if there are multiple conditions for a sequence you should ask the user about which condition apply to that sequence.
* Query and analysis
  * Simple query based on sequence name, condition and measuremento.
  * Aggregating measurement value for various sequences

## Getting started

To get the frontend/backend running locally:

- Install git : `https://git-scm.com/download`
- Clone this repo : `git clone https://github.com/Michael-ibanez/DatabaseFinalProject.git`
- Move into geneExpressionProject directory : `cd geneExpressionProject`
- Start the local server: `python3 manage.py runserver`
- Open up [this](http://127.0.0.1:8000/)
