# These tests are extremely simple and are used to confirm that decoding works
# properly.

import sys
sys.path.append("C:\\Users\\Alexander\\Documents\\GitHub\\ClassicCrypto")

# Some stuff we need for testing
from Ciphers.UtilityFunctions import decodetest, preptext, playfairPrep

# Load up the text to use
textfile = open('C:\\Users\\Alexander\\Documents\\GitHub\\ClassicCrypto\\SampleText\\text1.txt', 'r')
ptext = preptext(textfile.readline())
print()

# Import the various ciphers

# Monoalphabetic substitution
from Ciphers.Simple import affine, caesar, substitution

# Variation on the Playfair Cipher
from Ciphers.Playfair import playfair, twoSquare, fourSquare

# Rotor machines
from Ciphers.RotorMachine import enigma, SIGABA, M209

# Variations on the polybius square
from Ciphers.Polybius import polybiusSquare, ADFGX, ADFGVX, bifid, trifid

# Transposition ciphers
from Ciphers.Transposition import AMSCO, columnarTransport, doubleColumnarTransport, \
                                  railfence, turningGrille, turningGrilleExtended, \
                                  disruptedTransposition

# Variation on the Vigenere cipher
from Ciphers.Vigenere import vigenere, multiVigenere, trithemius, beaufort, \
                             multiBeaufort, autokey, affineVigenere, recursiveKey
                             

# The quagmire family of ciphers
from Ciphers import quagmire1, quagmire2, quagmire3, quagmire4

# Mutating alphabet ciphers
from Ciphers import chaocipher, hutton

# Everything else
from Ciphers import cipherDisk, nomenclator, straddlingCheckerboard, hillCipher, nihilist, \
                    VIC


decodetest(caesar,ptext,1)
decodetest(affine, ptext,[3,4])
decodetest(substitution, ptext,"IOWNAXYLOPHONE",)

decodetest(vigenere, ptext,"THISISABOUTFARMING")
decodetest(beaufort, ptext,"SUGARCANE")
decodetest(multiVigenere, ptext,["THIS","IS","ABOUT","FARMING"])
decodetest(multiBeaufort,ptext,["THIS","IS","ABOUT","FARMING"])
decodetest(autokey, ptext,"FARMING")
decodetest(affineVigenere, ptext,["SUGAR","CANE"])
decodetest(recursiveKey, ptext, "ZEBRAS")
decodetest(trithemius, ptext,"")

decodetest(polybiusSquare, ptext,"ZEBRAS")
decodetest(nihilist, ptext,["NIHILIST","CIPHER"])
decodetest(ADFGX, ptext.replace("J","I"),["ZEBRAS","GIGANTIC"])
decodetest(ADFGVX, ptext,["17ZEBRAS529","GIGANTIC"],)
decodetest(bifid, ptext,"GIANTUNICORNS")
decodetest(trifid, ptext,"GIANTUNICORNS")

decodetest(quagmire1, ptext,["FLYING","ZEBRA"])
decodetest(quagmire2, ptext,["FLYING","ZEBRA"])
decodetest(quagmire3, ptext,["FLYING","ZEBRA"])
decodetest(quagmire4, ptext,["FLYING","ZEBRA","CAVALRY"])

decodetest(chaocipher, ptext,["",""])
decodetest(hutton, ptext,["JUPTIER","FEDROA"])

decodetest(cipherDisk, ptext,"M0A8G7I4C3A2L6F4UNTI5MEL1AND",)

decodetest(playfair, playfairPrep(ptext),"ILIKEANTELOPES")
decodetest(fourSquare, ptext,["4SQUARE2","10CODE7"],mode="EX")
decodetest(twoSquare, ptext,["4SQUARE2","10CODE7"])

rotors =    ["V","III","II"]
reflector = "B"
positions = ["H","L","B"]
plugs =     ["AB","CD","EF","GH"]
rings =     ["A","A","A"]
keySettings = [rotors,reflector,positions,plugs,rings]
decodetest(enigma, ptext,keySettings)

cipher =     ["IV","X","VII","III","II"]
control =    ["IX","V","I","VI","VIII"]
index =      ["II","IV","V","I","III"]
indicator =  "HUPYU"
controlPos = "JBKPO"
indexPos =   "02384"
keySettings = [cipher,control,index,indicator,controlPos,indexPos]
SIGtext = ptext
SIGtext = SIGtext.replace("Z","X")
decodetest(SIGABA, SIGtext,keySettings)

pins = ["++-+---++-+-++----++-++---",
        "+--++-+--+++--+--++-+-+--",
        "++----++-+-+++---++++-+",
        "--+-++-++---++-+--+++",
        "-+-+++-++---++-+--+",
        "++-+---+--+--++-+"]
lugs = [[3,6], [0,6], [1,6], [1,5], [4,5], [0,4], [0,4],
        [0,4], [0,4], [2,0], [2,0], [2,0], [2,0], [2,0],
        [2,0], [2,0], [2,0], [2,0], [2,0], [2,5], [2,5],
        [0,5], [0,5], [0,5], [0,5], [0,5], [0,5]]
decodetest(M209, ptext,["TABLEA",pins,lugs])

key = [[ 4, 15, 23,  5], 
       [12,  6,  2,  9], 
       [ 8,  5, 24,  4], 
       [21, 25, 19, 16]]
decodetest(hillCipher, ptext,key)

decodetest(straddlingCheckerboard, ptext,["CIPHER",[5,7]])

decodetest(nomenclator, ptext,5766645)

decodetest(columnarTransport, ptext,"TABLES",)
decodetest(doubleColumnarTransport, ptext,["GIGANTIC","TABLES"],)
decodetest(railfence, ptext,5)
decodetest(AMSCO, ptext,"GIGANTIC")

grille = [35, 4, 23, 9, 14, 5, 
          12, 32, 24, 20, 15, 11,
          33, 10, 27, 31, 16, 29, 
          34, 1, 13, 18, 0, 28, 
          6, 2, 7, 21, 17, 30, 
          25, 19, 22, 26, 8, 3]
decodetest(turningGrille, ptext[:144],grille, N=6)
decodetest(turningGrilleExtended, ptext,grille, N=6)


decodetest(disruptedTransposition,ptext[:289],"GIANTZEBRACAVALRY")

decodetest(VIC,ptext[:180],["77651","74177","IDREAMOFJEANNIEWITHT",12])