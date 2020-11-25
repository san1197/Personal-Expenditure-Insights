import pandas as pd
import random

expenseData = pd.read_csv('dataset/Expenses Data Set.csv', low_memory=False)
expenseData_DF = pd.DataFrame(expenseData)

persons = ['Tom', 'Harry', 'Chris', 'Dave']
spent = ['spent', 'paid', 'gave', 'exhausted']
received = ['received', 'got', 'gained', 'earned']

# He received $300 as a bonus.
# He spent $300 on rent

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
        print(sentence)
    else:
        types = random.choice(received)
        sentence += name
        sentence += " "
        sentence += types
        sentence += " $"
        sentence += str(amount)
        sentence += " as "
        sentence += category
        print(sentence)

    n = inputFile.write(sentence)
    n = inputFile.write("\n")