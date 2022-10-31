from Ciphers.Transposition import columnarTransport
from Ciphers.UtilityFunctions import uniqueRank, groups
from Examples.ExampleTemplate import example



def columnarTransportExample():
    
    print("Example of the columnar transport cipher")

    key = "BIRTHDAY"
    ptext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    rank = uniqueRank(key)
    
    
    print("\nThe Key Is {}".format(key))
    
    print("Each letter of the key is ranked to get")
    print(*rank)

    print("\nThe plaintext is\n{}".format(ptext))
    
    print("\nNow the text is read into the grid by rows. The key is placed above.\n")

    print(" ".join([str(i) for i in rank]))
    for i in groups(ptext,8):
        print(" ".join([e for e in i]))

    print("\nFinally the grid is read off in accordance with column numbers starting with zero, then one, and so on.\n")
    
    ctext, dtext = example(columnarTransport,ptext,key,complete=False)
    print(ctext)
    
columnarTransportExample()
