# DatabaseFinalProject

This project implements the Gene Expression Data Management assignment given by Dr. Lin.

CSI 3335 Fall 19 Group Project – Gene Expression Management System - GEMS. 
GEMS is a tool to keep track of a study of gene expression at the messenger RNA (mRNA) level in different yeast strains.

- Data input (via GUI)
  - New experimental conditions and new measurement type.
  - Base information about the sequence.
  - Experiment condition/results for each sequence.
    - Notice there may be many experiments with the same sequence.
    - Each case need to specify its own condition and its own results.
- Data input (via csv file)
  - The user can supply a name of csv file. It will contains a matrix. Each row (except the first) is a sequence, with the first column its name. Each column (except the first) is a measurement type. The first row (starting from the second column) contain the name for the type. Each cell of the subsequent row contains the value of the measurement for that sequence. However, if there are multiple conditions for a sequence you should ask the user about which condition apply to that sequence.
- Query and analysis
  - Experiment info : the user entered in formation of an experiment and the system should display all the measurements associated with it.
  - Side-by-side comparisons : The user should select two experiments, the system should display the measurements that are common to both experiments side-by-side
- Views across multiple experiments
  - The user should enter a list of sequences and conditions.Then the system should retrieve all experiments that has the sequence and (at least) one of the conditions and list them
  - The user can also enter a list of measurements and the system will return the value of the measurements for all the experiments above as a table

## Getting started
Make sure you have a MySQL server running on localhost on port `3306` with user `root`. The password for `root` can be changed in `geneExpressionProject/settings.py`. Make sure this server has a pre-made, clean schema named `databaseFinalProject`.
- Install Python 3: `https://www.python.org/downloads/`
- Install git : `https://git-scm.com/download`
- Clone this repo : `git clone https://github.com/Michael-ibanez/DatabaseFinalProject.git`
- Install packages with pip : `pip install -r requirements.txt`
- Migrate the database: `python3 manage.py migrate`
- Start the local server: `python3 manage.py runserver`
- Open up [localhost:8000](http://127.0.0.1:8000/)

# User Manual to GEMS
Using GEMS is as simple as it looks. At its landing page, there is a video explaining the basics of Transcription and mRNA processing (Thanks to Khan Academy for the informational video), along with a short description of our tool.

Following this, the user can click on any of the buttons at the bottom of the page or on a header in the navbar at the top of the page to bring them to `Insert Data`, `Queries`, `Experiment Comparisons`, and `Presentation`.

Below are short subsections on each page.

## Insert Data
At the `Insert Data` page, you can insert data in a few ways.

1. You can input a CSV. This CSV must be formatted in the following format:
    - The first line must be the sequences and their conditions, all separated within each sequence/condition pair with `_`, and each sequence/condition pair is separated with `,`.
    - The second lines and all following lines must have the first value as the measurement name, and all following values are measurement values for their consecutive sequence/condition pairs, separated by `,`.
2. You can input conditions manually...
    - The first value is the name of the sequence
    - The second value is the domain of the sequence (it must be an integer, a float, a string, or a boolean)
    - The final value is the actual value of the aforementioned domain
3. You can input measurements manually...
    - The first value is the name of the measurement
    - The second value is the domain of the measurement (it must be an integer, a float, a string, or a boolean)
    - The final value is the actual value of the aforementioned domain
4. You can input sequence and information about that sequence...
    - The first value is the name of the sequence
    - The second value is any optional information about the sequence
    - The final value is an optional file name to a file containing the sequence
5. You can insert an experiment with condition and results
    - The first value is the sequence name
    - The second value are the conditions, separated by `,`, in the format `condition:value`
    - The final value are the measurements, separated by `,`, in the format `measurement:value`

## Queries
At the `Queries` page, you can query for information within the database.

1. You can query for individual sequence information
    - The first value is the sequence name
    - The second value is the sequence conditions in the format `condition:value`, with multiple conditions separated by `,`.
2. You can choose between sequences to perform a side by side comparison
    - This provides a simple drop-down menu for selecting between different experiments to compare

## Experiment Comparisons
Here, one can choose between experiments to compare. You can hold `Ctrl` and click on multiple sequences, conditions, and measurements, and then click `submit`.

This will present all chosen sequences with any of the conditions or measurements.

## Presentation
This is a simple powerpoint of our slides as well as the README. Feel free to look through our presentation and README!
