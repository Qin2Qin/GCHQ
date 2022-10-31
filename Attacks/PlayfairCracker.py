# Testing if the simple Hill Climbing method will work on the Playfair cipher

from Ciphers.Playfair import playfair
from TextScoring import quadgramScoreFrac
import random
import math
import numpy as np

def swapLetters(key):
    A,B = random.sample([i for i in range(25)],2)
    key[A],key[B] = key[B],key[A]
    
def swapRows(key):
    A,B = random.sample([0,1,2,3,4],2)
    key[5*A:5*A+5],key[5*B:5*B+5] = key[5*B:5*B+5],key[5*A:5*A+5]

def swapCols(key):
    A,B = random.sample([0,1,2,3,4],2)
    for i in range(5):
        t = key[i*5 + A]
        key[i*5 + A] = key[i*5 + B]
        key[i*5 + B] = t

def rotate(key):
    A = random.randint(1,23)
    for i in range(A):
        key.append(key.pop(0))

def simulatedAnnealing(ctext,T0,stepsize,restarts=50,rounds=10000):

    # There will be one thousand rounds of attempts to break the cipher
    # The reason we have multiple rounds is because we might get stuck in a 
    # local minima while mutating the results.
    # Occasionally resetting gives coverage of more of the possible search
    # space.
    for x in range(restarts):
        # To start the round we randomize the alphabet to start with
        key = [i for i in "ABCDEFGHIKLMNOPQRSTUVWXYZ"]
        random.shuffle(key)
        
        # Our starting score is whatever we got from this
        out = playfair(ctext,"".join(key),decode=True)
        bestscore = quadgramScoreFrac(out)
        bestkey = "".join(key)
     
        bestEverScore = quadgramScoreFrac(out)
        bestEverKey = "".join(key)
        
        # The "temperature" decreases gradually with each round. The higher the
        # temperature the more likely the algorithm is to accept a change.
        for temp in np.arange(T0,stepsize,-stepsize):
            print("!",end="")
            for i in range(rounds):

                # A copy of the key list that we can mutate
                newKey = key[:]
            
                # Choose which kind of mutation to apply
                mutType = random.randint(0,99)
                if mutType < 92:
                    swapLetters(newKey)
                if mutType >= 92 and mutType < 94:
                    swapRows(newKey)
                if mutType >= 94 and mutType < 96:
                    swapCols(newKey)
                if mutType >= 96 and mutType < 98:
                    rotate(newKey)
                if mutType >= 98:
                    newKey.reverse()
    
                tkey = "".join(newKey)
                # Try it and see what score we get
                out = playfair(ctext,tkey,decode=True)
                score = quadgramScoreFrac(out)

                
                # If that score is better we always take the new key
                # If it is worse then there is a chance we will accept it
                # anyway. When the temperature is high, early in the process,
                # it is more likely we will pick a worse score.
                if score > bestscore:
                    key = newKey
                    bestkey = newKey
                    bestscore = score
                else:
                    scorediff = (score - bestscore)

                    pr = math.exp(scorediff/temp)

                    if random.uniform(0,1) > pr:
                        key = newKey
                        bestkey = newKey
                        bestscore = score
    
                # The "best ever score" is kept but not interacted with beyond
                # this. It is our high water mark.
                if score > bestEverScore:
                    bestEverKey = bestkey
                    bestEverScore = bestscore

        print("\n\nRound {}".format(x+1))
        print("Best Key Ever Found:")
        print("".join(bestEverKey))
        print()
        print(playfair(ctext,"".join(bestEverKey),decode=True))
        print("\n")

ptext = "THECULTIVATIONOFTHESUGARCANEISPURSUEDTOGREATEXTENTINTHEISLANDSOFTHEWESTINDIESWHEREABOUTTHREECENTURIESAGOITWASFIRSTINTRODUCEDFROMCHINAORSOMEOTHERPARTSOFTHEEASTANDWHEREITFLOURISHESWITHGREATLUXURIANCEPARTICULARLYINMOISTANDRICHGROUNDTHESEASONFORPLANTINGITCOMMENCESABOUTTHEBEGINNINGOFAUGUST"
ctext = playfair(ptext,"PLAYFAIR")
#ctext = "XZOGQRWVQWNROKCOAELBXZWGEQYLGDRZXYZRQAEKLRHDUMNUXYXSXYEMXEHDGNXZYNTZONYELBEUGYSCOREUSWTZRLRYBYCOLZYLEMWNSXFBUSDBORBZCYLQEDMHQRWVQWAEDPGDPOYHORXZINNYWPXZGROKCOLCCOCYTZUEUIICERLEVHMVQWLNWPRYXHGNMLEKLRHDUYSUCYRAWPUYECRYRYXHGNBLUYSCCOUYOHRYUMNUXYXSXYEMXEHDGN"
simulatedAnnealing(ctext,T0=20,stepsize=.2,restarts=20,rounds=10000)