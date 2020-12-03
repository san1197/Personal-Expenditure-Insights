import sys, random


def normaliseTripplesPattern(inputString):
    str = inputString  # take copy of the input
    strk = str.replace('<http://SER531/Project/Group19/', ' ')  # replace header
    strm = strk.replace('>', ',')  # replace >
    strq = strm.replace('"', '')  # replace quotes
    strz = strq.replace(' ', '')  # replace spaces between the line
    return strz


if __name__ == '__main__':
    f = open("triples.txt", "r")
    lines = f.readlines()
    spent = ['spent', 'paid', 'gave', 'exhausted']
    received = ['received', 'got', 'gained', 'earned']
    debit = ['bills', 'grocery', 'merchandise', 'travel']
    credit = ['transfer', 'tuition', 'deposit', 'donation']
    summarizeFile = open("summarization.txt", "w")
    for l in lines:
        l.strip(" ")
        x = normaliseTripplesPattern(l).split(',')
        subject = x[0]
        predicate = x[1]
        object = x[2].strip()
        if predicate in debit:
            activity = random.choice(spent)
        elif predicate in credit:
            activity = random.choice(received)
        sentence = subject + " " + activity + " $" + object + " on " + predicate
        summarizeFile.write(sentence + "\n")
    print("\n****** Summarization Complete **********\n")
    print("****** Sentences stored in summarization.txt **********\n")
