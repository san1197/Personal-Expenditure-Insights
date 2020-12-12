# Personal Expenditure Insights

## How does it work?
![Flowchart](/images/Flowchart.png)

## What does it do?
- Extracts useful information from transactional data.
- Compares expenditure of several users.
- Provides a visual representation of a user's monthly expenditure.
- Uses OWL Ontologies to map transactions into categories. Check the Ontology [here](http://www.visualdataweb.de/webvowl/#opts=cd=80;dd=90;%23iri=https://raw.githubusercontent.com/san1197/SER531-Project---Group-19/main/categories.owl)

## A glimpse of the insights generated:
**Expense Distribution of specific user:**
![ExpDist](/images/SpecificExpenseDist.png)

**Total Income of all users:**
![TotalIncome](/images/totalIncome.png)

## Requirements:
- Python3
- rdflib
- spacy
- owlready2
- matplotlib
- pandas

**System on which compiler and runtime are built:** Windows

**Tools used:** Python, Protege.

## Execution
- Install the required libraries and locate to the working directory.
- Open the terminal and run the following command:
```bash
    python preprocess.py
```
- The triples will be generated and stored in 'triples.txt'.
- Run the following command to generate insights.
```bash
    python tripleGen.py
```
- The output graphs can be seen through the terminal.
- If you want to summarize the triples back to sentences, run:
```bash
    python summarize.py
```
- The sentences will be generated at summarization.txt.

## Video Demonstration
[YouTube Video](https://www.youtube.com/watch?v=KmKTgx5wt_Y&feature=youtu.be)

## Ontology
[Ontology Visualization](http://www.visualdataweb.de/webvowl/#opts=cd=80;dd=90;#iri=https://raw.githubusercontent.com/san1197/SER531-Project---Group-19/main/categories.owl)