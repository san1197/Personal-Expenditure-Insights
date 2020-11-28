import sys, random

if __name__ == '__main__':
    f = open("triples.txt", "r")
    lines = f.readlines()
    spent = ['spent', 'paid', 'gave', 'exhausted']
    received = ['received', 'got', 'gained', 'earned']
    summarizeFile = open("summarization.txt", "w")
    for l in lines:
        l.strip(" ")
        x = l.split(',')
        subject = x[0]
        predicate = x[1]
        object = x[2].strip()
        activity = random.choice([random.choice(spent),random.choice(received)])
        if activity == 'exhausted' or activity == 'spent':
            sentence = subject + " " + activity + " $" + object + " on " + predicate
        else:
            sentence = subject + " " + activity + " $" + object + " for " + predicate
        summarizeFile.write(sentence + "\n")
    print("\n****** Summarization Complete **********")
    print("\n****** Sentences stored in summarization.txt **********\n")
