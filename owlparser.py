from owlready2 import get_ontology
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF , XSD

import spacy

'''Extracting sub, pred and obj from unstructured data'''
nlp = spacy.load('en_core_web_sm')

file_doc = open("input.txt", "r")

doc = file_doc.read()

complete_doc = nlp(doc)

nouns = []
pronoun = []
values= []

spo = []

for token in complete_doc:
    if token.pos_ == 'NOUN':
        nouns.append(token.text)
    if token.pos_ == 'PROPN':
        pronoun.append(token.text)
    if token.ent_type_ == 'MONEY':
        values.append(token.lemma_)

i = 0
j = 0
k = 0
while i < len(nouns) and j < len(values) and k < len(pronoun):
    spo_values = [pronoun[k], nouns[i], values[j]]
    spo.append(spo_values)
    i += 1
    j += 1
    k += 1



onto = get_ontology("https://raw.githubusercontent.com/san1197/SER531-Project---Group-19/main/categories.owl").load()
namespace = onto.get_namespace("https://raw.githubusercontent.com/san1197/SER531-Project---Group-19/main/categories.owl")
IncType = onto.search(iri = "*Income")
ExpType = onto.search(iri = "*Expense")

# To add N-Triples
g = Graph()


for sub, pred, obj in spo:
	sub_url = URIRef(sub)

	#Mapping predicate to OWL classes
	if pred == 'groceries':
		pred_url = URIRef('Grocery')
	elif pred == 'merchandise':
		pred_url = URIRef('Clothing')
	elif pred == 'transfer':
		pred_url = URIRef('Income')
	elif pred == 'travel':
		pred_url = URIRef('TravelInsurance')
	else:
		pred_url = URIRef('Health')
	
	obj_url = Literal(obj)
	g.add((sub_url, pred_url, obj_url))


# To derive insights using OWL
totalIncome = 0
totalExpense = 0
maxExpense = 0
maxExpenseOn = ''
users = []
dictionary = {}
listofDic = []
count = 1




for s,p,o in g:
	if str(s) not in users:
		users.append(str(s))


for i in range(len(users)):
	totalIncome = 0
	totalExpense = 0
	maxExpense = 0
	maxExpenseOn = ''
	username = ''
	for s,p,o in g:
		if(str(s) == users[i]):
			username = str(s)
			appendstar = "*"
			appendstar += str(p)
			typeNS = onto.search(iri = appendstar)
			if(IncType[0] in list(typeNS[0].ancestors())):
				totalIncome += float(o)
			elif(ExpType[0] in list(typeNS[0].ancestors())):
				totalExpense += float(o)
				maxExpense = max(maxExpense,float(o))
				maxExpenseOn = str(p)		
	print("\n")
	print("User:",username)
	print("Total Income:", totalIncome)
	print("Total Expense:", totalExpense)
	print("Maximum Expense:",maxExpense,"Spent on",maxExpenseOn)
		



