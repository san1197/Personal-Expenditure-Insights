from owlready2 import *
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF , XSD

onto = get_ontology("https://raw.githubusercontent.com/san1197/SER531-Project---Group-19/main/categories.owl").load()
namespace = onto.get_namespace("https://raw.githubusercontent.com/san1197/SER531-Project---Group-19/main/categories.owl")
IncType = onto.search(iri = "*Income")
ExpType = onto.search(iri = "*Expense")

# To add N-Triples
g = Graph()
money = Literal("300")
money2 = Literal("50")
money3 = Literal("5000")
money4 = Literal("2300")

h = URIRef("Harry")
k = URIRef("Kaleb")
e = URIRef('Cable')
i = URIRef('Rent')
w = URIRef('Wages')

g.add((h,i,money))
g.add((h,e,money2))
g.add((h,w,money3))
g.add((k,w,money4))
g.add((k,e,money2))


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
				totalIncome += int(o)
			elif(ExpType[0] in list(typeNS[0].ancestors())):
				totalExpense += int(o)
				maxExpense = max(maxExpense,int(o))
				maxExpenseOn = str(p)		
	print("\n")
	print("User:",username)
	print("Total Income:", totalIncome)
	print("Total Expense:", totalExpense)
	print("Maximum Expense:",maxExpense,"Spent on",maxExpenseOn)
		



