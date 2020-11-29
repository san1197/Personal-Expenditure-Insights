import pandas as pd
import random

expenseData = pd.read_csv('dataset/Expenses Data Set.csv', low_memory=False)
expenseData_DF = pd.DataFrame(expenseData)

persons = ['Tom', 'Harry', 'Chris', 'Dave']
spent = ['spent', 'paid', 'gave', 'exhausted']
received = ['received', 'got', 'gained', 'earned']
inputFile = open("input.txt","w")

for index, row in expenseData_DF.iterrows():
    name = random.choice(persons)
    amount = row['Amount']
    category = row['Category']
    sentence = ""
    if amount < 0:
        amount = -amount
        types = random.choice(spent)
        sentence += name
        sentence += " "
        sentence += types
        sentence += " $"
        sentence += str(amount)
        if types == 'spent' or types == 'exhausted':
            sentence += " on "
        else:
            sentence += " for "
        sentence += category

    else:
        types = random.choice(received)
        sentence += name
        sentence += " "
        sentence += types
        sentence += " $"
        sentence += str(amount)
        sentence += " as "
        sentence += category

    n = inputFile.write(sentence)
    n = inputFile.write("\n")

print("\n****** Preprocessing Complete **********")
print("****** Sentences stored in input.txt **********\n")
