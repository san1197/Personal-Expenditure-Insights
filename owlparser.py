from owlready2 import get_ontology
from rdflib import Graph, Literal, RDF, URIRef
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
IncType = onto.search(iri = "*income")
ExpType = onto.search(iri = "*expense")

# To add N-Triples
g = Graph()


for sub, pred, obj in spo:
    sub_url = URIRef(sub)
    pred_url = URIRef(pred)
    obj_url = Literal(obj)
    g.add((sub_url, pred_url, obj_url))

f = open("triples.txt", "w")
for s,p,o in g:
    string = str(s) + "," + str(p) + "," +str(o)
    f.write(string)
    f.write("\n")
f.close()

print("\n****** Triples Generated **********")
print("\n****** Stored in triples.txt **********\n")

# To derive insights using OWL
totalIncome = 0
totalExpense = 0
maxExpense = 0
maxExpenseOn = ''
users = []
dictionary = {}
listofDic = []
count = 1
expenseTypes = []
for s,p,o in g:
    if str(s) not in users:
        users.append(str(s))

types = []
for s,p,o in g:
    if str(p) not in types:
        types.append(str(p))



for s,p,o in g:
    if str(p) not in expenseTypes:
        expenseTypes.append(str(p))

for i in range(len(users)):
        #Adding users
        usertag = "U"
        usertag += str(i)
        user1 = onto.User(usertag,hasName=users[i])


t = 0
for s,p,o in g:
    #Adding transactions
    ss = "*"
    uu = "*"
    ss += str(p)

    typeforEI = onto.search(iri = ss)
    ttag = "T"
    ttag += str(t)
    t += 1

    for i in onto.User.instances():
        if(i.hasName == str(s)):
            userkill = str(i).split(".")
    uu += userkill[1]
    usersearch = onto.search(iri = uu)
    t1 = onto.Transaction(ttag,ofType=typeforEI,ofAmount=str(o),doneBy=usersearch)
onto.save(file = "categorieswithIndividuals.owl")



g1 = Graph()
g1.parse("categorieswithIndividuals.owl")

incomeQuery = g1.query(
    '''
    PREFIX ie: <http://www.semanticweb.org/admin/ontologies/2020/10/category#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT ?p ?a ?name ?log
        WHERE {
            ?p rdf:type ie:User.
            ?p ie:hasName ?name.
            ?t ie:doneBy ?p.
            ?t ie:ofType ?log.
            ?t ie:ofAmount ?a.
            ?log rdfs:subClassOf ie:income.
            }
            ORDER BY ?name''')

totalIncomeList = []
maxIncomeList = []
maxIncomeOnList = []
userlist = []
for i in range(len(users)):
    totalIncome = 0
    maxIncome = 0
    maxIncomeOn = ''
    username = ''
    for r in incomeQuery:
        incomeType = str(r[3]).split("#")
        if(str(r[2]) == users[i]):
            username = r[2]
            totalIncome += float(r[1])
            maxIncome = max(maxIncome,float(r[1]))
            maxIncomeOn = incomeType[1]
    userlist.append(str(username))
    totalIncomeList.append(totalIncome)
    maxIncomeList.append(maxIncome)
    maxIncomeOnList.append(maxIncomeOn)

totalExpenseList = []
maxExpenseList = []
maxExpenseOnList = []
userlist2 = []
expenseQuery = g1.query(
    '''
    PREFIX ie: <http://www.semanticweb.org/admin/ontologies/2020/10/category#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?p ?a ?name ?log
        WHERE {
            ?p rdf:type ie:User.
            ?p ie:hasName ?name.
            ?t ie:doneBy ?p.
            ?t ie:ofType ?log.
            ?t ie:ofAmount ?a.
            ?log rdfs:subClassOf ?parentClass.
            ?parentClass rdfs:subClassOf ie:expense.
            }
            ORDER BY ?name''')

for i in range(len(users)):
    totalExpense = 0
    maxExpense = 0
    maxExpenseOn = ''
    username = ''
    for r in expenseQuery:
        expenseType = str(r[3]).split("#")
        if(str(r[2]) == users[i]):
            username = r[2]
            totalExpense += float(r[1])
            maxExpense = max(maxExpense,float(r[1]))
            maxExpenseOn = expenseType[1]

    userlist2.append(str(username))
    totalExpenseList.append(totalExpense)
    maxExpenseList.append(maxExpense)
    maxExpenseOnList.append(maxExpenseOn)

userExpenseQueryH = g1.query(
    '''
    PREFIX ie: <http://www.semanticweb.org/admin/ontologies/2020/10/category#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?p ?a ?name ?log
        WHERE {
            ?p rdf:type ie:User.
            ?p ie:hasName ?name.
            ?t ie:doneBy ?p.
            ?t ie:ofType ?log.
            ?t ie:ofAmount ?a.
            ?log rdfs:subClassOf ?parentClass.
            ?parentClass rdfs:subClassOf ie:expense.
            FILTER (regex(str(?name),"Harry"))
            }''')

typeAmountListH = []
for k in range(len(types)):
    typeAmount = 0
    for r in userExpenseQueryH:
        expenseType = str(r[3]).split("#")
        if(expenseType[1] in types[k]):
            typeAmount += float(r[1])
    typeAmountListH.append(typeAmount)

userExpenseQueryD = g1.query(
    '''
    PREFIX ie: <http://www.semanticweb.org/admin/ontologies/2020/10/category#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?p ?a ?name ?log
        WHERE {
            ?p rdf:type ie:User.
            ?p ie:hasName ?name.
            ?t ie:doneBy ?p.
            ?t ie:ofType ?log.
            ?t ie:ofAmount ?a.
            ?log rdfs:subClassOf ?parentClass.
            ?parentClass rdfs:subClassOf ie:expense.
            FILTER (regex(str(?name),"Dave"))
            }''')

typeAmountListD = []
for k in range(len(types)):
    typeAmount = 0
    for r in userExpenseQueryD:
        expenseType = str(r[3]).split("#")
        if(expenseType[1] in types[k]):
            typeAmount += float(r[1])
    typeAmountListD.append(typeAmount)

userExpenseQueryC = g1.query(
    '''
    PREFIX ie: <http://www.semanticweb.org/admin/ontologies/2020/10/category#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?p ?a ?name ?log
        WHERE {
            ?p rdf:type ie:User.
            ?p ie:hasName ?name.
            ?t ie:doneBy ?p.
            ?t ie:ofType ?log.
            ?t ie:ofAmount ?a.
            ?log rdfs:subClassOf ?parentClass.
            ?parentClass rdfs:subClassOf ie:expense.
            FILTER (regex(str(?name),"Chris"))
            }''')

typeAmountListC = []
for k in range(len(types)):
    typeAmount = 0
    for r in userExpenseQueryC:
        expenseType = str(r[3]).split("#")
        if(expenseType[1] in types[k]):
            typeAmount += float(r[1])
    typeAmountListC.append(typeAmount)

userExpenseQueryT = g1.query(
    '''
    PREFIX ie: <http://www.semanticweb.org/admin/ontologies/2020/10/category#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT ?p ?a ?name ?log
        WHERE {
            ?p rdf:type ie:User.
            ?p ie:hasName ?name.
            ?t ie:doneBy ?p.
            ?t ie:ofType ?log.
            ?t ie:ofAmount ?a.
            ?log rdfs:subClassOf ?parentClass.
            ?parentClass rdfs:subClassOf ie:expense.
            FILTER (regex(str(?name),"Tom"))
            }''')

typeAmountListT = []
for k in range(len(types)):
    typeAmount = 0
    for r in userExpenseQueryT:
        expenseType = str(r[3]).split("#")
        if(expenseType[1] in types[k]):
            typeAmount += float(r[1])
    typeAmountListT.append(typeAmount)




import matplotlib.pyplot as plt
plt.style.use('ggplot')

print("Choose from the below visualizations")
print("1. Total Income of all users ")
print("2. Total Expense of all users")
print("3. Specific User Expense Data")
print("4. Exit")

inpNo = int(input())

while(inpNo != 4):
    if(inpNo == 1):
        x = userlist
        energy = totalIncomeList
        x_pos = [i for i, _ in enumerate(x)]
        plt.bar(x_pos, energy, color='green')
        plt.xlabel("Income")
        plt.ylabel("Dollars($)")
        plt.title("Total Income Graph")
        plt.xticks(x_pos, x)
        plt.show()
        inpNo = int(input())
    if(inpNo == 2):
        x = userlist
        energy = totalExpenseList
        x_pos = [i for i, _ in enumerate(x)]
        plt.bar(x_pos, energy, color='green')
        plt.xlabel("Expense")
        plt.ylabel("Dollars($)")
        plt.title("Total Expense Graph")
        plt.xticks(x_pos, x)
        plt.show()
        inpNo = int(input())
    if(inpNo == 3):
        print("Choose user name from the below list:")
        print(users)
        userChoice = str(input())
        if(userChoice == "Harry"):
            typesFinal = []
            typeAmountFinal = []
            for i in range(len(types)):
                if(typeAmountListH[i] != 0):
                    typesFinal.append(types[i])
                    typeAmountFinal.append(typeAmountListH[i])

            labels = typesFinal
            sizes = typeAmountFinal

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes,shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.legend(types)
            plt.title("Expense Distribution for Harry")
            plt.show()
            inpNo = int(input())

        if(userChoice == "Chris"):
            typesFinal = []
            typeAmountFinal = []
            for i in range(len(types)):
                if(typeAmountListC[i] != 0):
                    typesFinal.append(types[i])
                    typeAmountFinal.append(typeAmountListC[i])

            labels = typesFinal
            sizes = typeAmountFinal

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes,shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.legend(types)
            plt.title("Expense Distribution for Chris")
            plt.show()
            inpNo = int(input())

        if(userChoice == "Tom"):
            typesFinal = []
            typeAmountFinal = []
            for i in range(len(types)):
                if(typeAmountListT[i] != 0):
                    typesFinal.append(types[i])
                    typeAmountFinal.append(typeAmountListT[i])

            labels = typesFinal
            sizes = typeAmountFinal

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes,shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.legend(types)
            plt.title("Expense Distribution for Tom")
            plt.show()
            inpNo = int(input())

        if(userChoice == "Dave"):
            typesFinal = []
            typeAmountFinal = []
            for i in range(len(types)):
                if(typeAmountListD[i] != 0):
                    typesFinal.append(types[i])
                    typeAmountFinal.append(typeAmountListD[i])

            labels = typesFinal
            sizes = typeAmountFinal
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes,shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.legend(types)
            plt.title("Expense Distribution for Dave")
            plt.show()
            inpNo = int(input())
