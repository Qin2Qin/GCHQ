from math import log2,floor
import csv

ngrams1 = open('1grams.csv', 'r')
tot1 = 0
for line in ngrams1:
    L = line.split(",")
    tot1 += int(L[1])
ngrams1.seek(0)

ngrams2 = open('2grams.csv', 'r')
tot2 = 0
for line in ngrams2:
    L = line.split(",")
    tot2 += int(L[1])
ngrams2.seek(0)

ngrams3 = open('3grams.csv', 'r')
tot3 = 0
for line in ngrams3:
    L = line.split(",")
    tot3 += int(L[1])
ngrams3.seek(0)

ngrams4 = open('4grams.csv', 'r')
tot4 = 0
for line in ngrams4:
    L = line.split(",")
    tot4 += int(L[1])
ngrams4.seek(0)

# We use the log probabilities since they are additive

with open('2gramScores.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    
    for line in ngrams2:
        L = line.split(",")
        L[1] = int(L[1])
        # The log probabilities are additive
        logprob = log2((L[1]+1)/tot2)
        # Since Python has no limits on integer size we make storage easier
        # by just storing the first few digits of the log probability
        L.append(floor(logprob*100))
        L.append(logprob)
        writer.writerow(L)
        
with open('3gramScores.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    
    for line in ngrams3:
        L = line.split(",")
        L[1] = int(L[1])
        logprob = log2((L[1]+1)/tot3)
        L.append(floor(logprob*100))
        L.append(logprob)
        writer.writerow(L)

        
with open('4gramScores.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    
    for line in ngrams4:
        L = line.split(",")
        L[1] = int(L[1])
        logprob = log2((L[1]+1)/tot4)
        L.append(floor(logprob*100))
        L.append(logprob)
        writer.writerow(L)
        
with open('1gramScores.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    
    for line in ngrams1:
        L = line.split(",")
        L[1] = int(L[1])
        logprob = log2((L[1]+1)/tot1)
        L.append(floor(logprob*100))
        L.append(logprob)
        writer.writerow(L)