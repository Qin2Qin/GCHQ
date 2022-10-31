def fisherYatesShuffle(K,rand):
    if K > len(rand):
        raise Exception("Not enough random numbers.")
    
    L = [i for i in range(K)]
    
    out = []
    
    for i in range(K):

        r = rand[i]

        out.append(L.pop( r % (K-i) ))

    return out

def fisherYatesShuffleExample():
    from RNG.LCG import LCG
    from itertools import islice, product
    
    suits = ["\u2663", "\u2665", "\u2660", "\u2666"]
    ranks = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
    deck = []
    for i,j in product(suits,ranks):
        deck.append("".join([j,i]))

    print("Deck of Cards in Standard Order")

    for i,card in enumerate(deck,1):
        print(card,end = " ")
        if i % 13 == 0:
            print()
 
    R = [i for i in islice(LCG(555,1000,73,123),52)]
    print("\nPseudo-Random Numbers")
    print(R)
    
    shuf = fisherYatesShuffle(52,R)
    print("\nFisher-Yates Positions")    
    print(shuf)
    print(len(shuf))

    print("\nShuffled Deck")
    shufdeck = [deck[i] for i in shuf]
    for i,card in enumerate(shufdeck,1):
        print(card,end = " ")
        if i % 13 == 0:
            print()
    print()

#fisherYatesShuffleExample()