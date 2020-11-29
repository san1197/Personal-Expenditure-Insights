# SER 531 Project - Group 19
# Extracting insights from Personal Expenditure 

## Requirements:
- Python3
- rdflib
- spacy
- owlready2
- matplotlib
- pandas

**System on which compiler and runtime are built:** Windows

**Tools used:** Python, Protege.

## Video Demonstration
[YouTube Video]()

## Ontology
[Ontology Visualization](http://www.visualdataweb.de/webvowl/#opts=cd=80;dd=90;#iri=https://raw.githubusercontent.com/san1197/SER531-Project---Group-19/main/categories.owl)

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
