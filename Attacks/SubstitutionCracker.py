# based on http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-simple-substitution-cipher/

from Ciphers.Simple import substitution
from Attacks.TextScoring import quadgramScore
from Attacks.AffineCracker import affineCracker
import random



def substitutionCracker(ctext,rounds=100):
    
    # It is possible that the cipher is something simple like an Caesar or
    # affine cipher. The keyspace for those is small but might be missed by the
    # randomized method used for general substitution.
    # So we start by using the affineCracker functions
    
    A,k = affineCracker(ctext)
    finalScore = quadgramScore(A)
    finalOut = A
    print(finalScore)
    
    # There will be one thousand rounds of attempts to break the cipher
    # The reason we have multiple rounds is because we might get stuck in a 
    # local minima while mutating the results.
    # Occasionally resetting gives coverage of more of the possible search
    # space.
    for x in range(rounds):
        # To start the round we randomize the alphabet to start with
        key = [i for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        random.shuffle(key)
        
        # Our starting score is whatever we got from this
        out = substitution(ctext,"".join(key),decode=True)
        bestscore = quadgramScore(out)
        bestkey = "".join(key)
     
        # Within each round we keep mutating the key until we go a few thousand
        # mutations without improvement.
        ctr = 0
        while ctr < 2000:
            # Count how many mutations since the last improvement
            ctr += 1
            
            # A copy of the key list that we can mutate
            newKey = key[:]
            
            # The mutation is swapping two letters
            A = random.randint(0,25)
            B = random.randint(0,25)
            newKey[A],newKey[B] = newKey[B],newKey[A]
            
            # Try it and see what score we get
            out = substitution(ctext,"".join(newKey),decode=True)
            score = quadgramScore(out)
            
            # If that score is better than before write it down and reset the
            # counter.
            if score > bestscore:
    
                ctr = 0
                key = newKey
                bestkey = newKey
                bestscore = score
    
        # At the end of each round check if it produced a better score than
        # any previous round. If it did then write it down and print some
        # information.
        if bestscore > finalScore:
            finalOut = substitution(ctext,"".join(bestkey),decode=True)
            finalScore = bestscore
            print("\n\nRound {}".format(x+1))
            print("Key Looks Like:")
            print("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            print("".join(bestkey))
            print()
            print(finalOut)
            
            print(finalScore)
            print("\n")
        else:
            print("#",end="")
        
    return finalOut

def substitutionCrackerExample():

    print("""
The keyspace for a substitution cipher is much too large for us to try every
possibility so we will use hill climbing with random restarts to explore only
the most likely options. The idea is that we will try a random key and then
make a small change to it. If that change is an improvement we keep it and try
another change. This will usually fail so after a while we stop and start over
with a new random key.
""")

    ctext = "SOWFBRKAWFCZFSBSCSBQITBKOWLBFXTBKOWLSOXSOXFZWWIBICFWUQLRXINOCIJLWJFQUNWXLFBSZXFBTXAANTQIFBFSFQUFCZFSBSCSBIMWHWLNKAXBISWGSTOXLXTSWLUQLXJBUUWLWISTBKOWLSWGSTOXLXTSWLBSJBUUWLFULQRTXWFXLTBKOWLBISOXSSOWTBKOWLXAKOXZWSBFIQSFBRKANSOWXAKOXZWSFOBUSWJBSBFTQRKAWSWANECRZAWJ"
    #ctext = "SWXPJMSNAHSNLULOSWXBJFHKPHUXNBCJKBJXGSLFKXHSXISXUSNUSWXNBMHUGBLOSWXRXBSNUGNXBRWXKXHYLJSSWKXXPXUSJKNXBHFLNSRHBONKBSNUSKLGJPXGOKLDPWNUHLKBLDXLSWXKCHKSBLOSWXXHBSHUGRWXKXNSOMLJKNBWXBRNSWFKXHSMJIJKNHUPXCHKSNPJMHKMZNUDLNBSHUGKNPWFKLJUGSWXBXHBLUOLKCMHUSNUFNSPLDDXUPXBHYLJSSWXYXFNUUNUFLOHJFJBS"
    #ctext = "HPPWXTLCSCBPQMFJKTFPGLIXTLCPQPNBPFJKTFPC"
    
    print("The Ciphertext Looks Like This:")
    print(ctext)
    
    substitutionCracker(ctext,rounds=20)
    
#substitutionCrackerExample()