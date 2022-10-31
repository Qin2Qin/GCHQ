# A simulation of the Engima machine


# Pass a singal through a rotor
def rotor(letter,key,pos,invert=False):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    entry = alpha.index(letter)
    
    if invert == False:
        inner = key[(entry+pos-1)%26]
        outer = (alpha.index(inner)-pos+1)%26
        return alpha[outer]
    if invert == True:
        inner = alpha[(entry+pos-1)%26]
        outer = (key.index(inner)-pos+1)%26
        return alpha[outer]


# The plugboard (Steckerbrett) flips pairs of letters
# Pairs of letters are not allowed to overlap
def plugboard(text,keys):
    
    if keys == []:
        return text
    
    # A very messy bit of code that makes sure only unique pairs of letters
    # are swapped.
    for pos,key in enumerate(keys):
        for let in key:
            for i in range(pos+1,len(keys)):
                if let in keys[i]:
                    raise Exception('pairs of letters cannot overlap')
    
    # Do the swapping
    for key in keys:
        text = text.replace(key[0],"*")
        text = text.replace(key[1],key[0])
        text = text.replace("*",key[1])
    return text


# Should get around to a copy of Enigma at some point
def enigma(text,keys,decode=False):
    
    # Check that theere are exactly five machine settings provided
    if len(keys) != 5:
        raise Exception('the "keys" argument must provide rotors, reflector, rotor positions, plugs, and ring settings')
    
    # Dictionary of rotors and notch positions
    rtrSelect = {"I":   ["EKMFLGDQVZNTOWYHXUSPAIBRCJ",18],
                 "II":  ["AJDKSIRUXBLHWTMCQGZNPYFVOE",6],
                 "III": ["BDFHJLCPRTXVZNYEIWGAKMUSQO",14],
                 "IV":  ["ESOVPZJAYQUIRHXLNFTGKDCMWB",11],
                 "V":   ["VZBRGITYUPSDNHLXAWMJQOFECK",0],}
    
    # Dictionary of reflectors
    refSelect = {"A": "EJMZALYXVBWFCRQUONTSPIKHGD",
                 "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
                 "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",}
    
    # Check the rotors listed to get the wiring and notch positions for them
    rotors = []
    notches = []
    for num in keys[0]:
        rotors.append(rtrSelect[num][0])
        notches.append(rtrSelect[num][1])
    
    # Get the wiring of the reflector
    reflector = refSelect[keys[1]]
    
    # Translate the letters of the rotor positions and ring positions to numbers
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    positions = [alpha.index(i)+1 for i in keys[2]]
    rings = [alpha.index(i) for i in keys[4]]
    
    # Reverse the lists since this is how the Enigma actually ordered the
    # rotors.
    rotors.reverse()
    notches.reverse()
    positions.reverse()
    rings.reverse()
    
    
    # The ring positions just repersent an offset from the rotor positions so
    # we subtract their numerical values.
    for i in range(3):
        positions[i] -= rings[i]
    
    
    # Put the text through the plugboard
    text = plugboard(text,keys[3])
    
    out = []
    
    for letter in text:

        
        T = letter
        
        # Step the first rotor (the fast rotor)
        positions[0] = (positions[0] + 1) % 26
        
        # If it has passed its notch then move the second rotor (middle rotor)
        if positions[0] == notches[0]:
            positions[1] = (positions[1] + 1) % 26
        
            # If the middle rotor has passed its notch then move both the
            # middle rotor and the last rotor (slow rotor)
            # This doublestepping behavior is a serious weakness in the machine
            # as it means the middle rotor effectively skips a position.
            if positions[1] == notches[1]:
                positions[1] = (positions[1] + 1) % 26
                positions[2] = (positions[2] + 1) % 26


        # Pass through the rotors then through the reflector and then back
        # through the rotors in reverse.
        T = rotor(T,rotors[0],positions[0])
        T = rotor(T,rotors[1],positions[1])
        T = rotor(T,rotors[2],positions[2])
        T = rotor(T,reflector,1)
        T = rotor(T,rotors[2],positions[2],True)
        T = rotor(T,rotors[1],positions[1],True)
        T = rotor(T,rotors[0],positions[0],True)
        
        out.append(T)
            
    out = "".join(out)
    
    # Through the plugboard once more    
    out = plugboard(out,keys[3])
    
    return "".join(out)

