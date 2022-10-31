import random
import time
import freqAnalysis
import copy

alphabet = ' abcdefghijklmnopqrstuvwxyz'
max_key_length = 26
METHODS = ["v","b"] #different poly-alpha functions

'''Load the two dictionaries and strip end of line characters'''
def get_dictionaries(d_one = 'dictionary_1.txt', d_two='dictionary_2.txt'):
    d_one = open(d_one, 'r').readlines()
    d_two = open(d_two, 'r').readlines()
    
    for index,text in enumerate(d_one):
        d_one[index] = text.strip('\n\r')
    
    for index,text in enumerate(d_two):
        d_two[index] = text.strip('\n\r')
    
    return d_one, d_two

'''Calculate the shifts between two equal length strings'''
def compare_shifts(string_one, string_two, method):
    prev_diff = calc_shift(string_one[0],string_two[0],method)
    
    try:
        for i in range(len(string_one)):
            difference = calc_shift(string_one[i], string_two[i], method)
            if difference != prev_diff:
                return False
            prev_diff = difference
    except:
        print('[!] String length difference in calculate_shifts')

    return True

'''Calculate the amount x must be shifted by to reach y'''
def calc_shift(x,y, method):
    if method == "v":
        diff = alphabet.index(x) - alphabet.index(y)
        if diff < 0:
            diff = 27+diff
        return diff
    elif method == "b":
        diff = alphabet.index(x) + alphabet.index(y)
        if diff >= 27:
            diff -= 27
        return diff
    
'''Shift a character by shift places'''
def do_shift(char, shift, method):
    if method == "v":
        new_index = alphabet.index(char) + shift
        if new_index >=27:
            new_index -= 27
        return alphabet[new_index]
    elif method == "b":
        new_index = shift - alphabet.index(char)
        if new_index < 0:
            new_index += 27
        return alphabet[new_index]

'''Given a list of indexes, return the characters at those indexes'''
def get_chars_at_indexes(indexes, text):
    return [text[i] for i in indexes]

'''Get every i_th character e.g. Get every 5th character
'''
def get_all_i_th_chars(text, i, start=0):
    ret = ''
    x = start
    while x < len(text):
        ret = ret+text[x]
        x+=i 
    return ret

'''Build the key based off the known plain text'''
def build_key(cipher_text, plain_text, length, method):
    key = []
    for i in range(length):
        key.append(calc_shift(plain_text[i], cipher_text[i], method))
    return key

'''Decrypt a text with the key'''
def decrypt(cipher_text, key, method = "v"):
    ret = ''
    i = 0
    for c in cipher_text:
        ret += do_shift(c, key[i], method)
        i+=1
        if i >= len(key):
            i = 0
    return ret

def brute_key_len(cipher_text, plain_text, method = "v"):
    possible_lengths = []
    for key_len in range(1, max_key_length):
        cipher_chars = get_all_i_th_chars(cipher_text, key_len)
        plain_chars = get_all_i_th_chars(plain_text, key_len)

        if compare_shifts(plain_chars, cipher_chars, method):
            #print(f'Possible key length {shifts[0]}')
            possible_lengths.append(key_len)
    
    return possible_lengths

def test_one(cipher_text, dictionary):
    for d in dictionary:
        #test for possible polyalphabetic ciphers
        for method in METHODS:
            possible_key_lengths = brute_key_len(cipher_text, d, method)
            if len(possible_key_lengths) > 0:
                for key_len in possible_key_lengths:
                    key = build_key(cipher_text, d, key_len, method)
                    if decrypt(cipher_text, key, method) == d:
                        return d
                

        
    return False

def find_repeat_sequences(cipher_text, length = 3):
    ret = []
    for i in range(len(cipher_text) - length):
        sequence = cipher_text[i:i+length]
        for j in range(i+1, len(cipher_text)-length):
            if cipher_text[j:j+length] == sequence:
                ret.append(sequence)
    
    return list(set(ret))

def find_gaps_between_repeats(cipher_text, repeated_sequences, length=3):
    gaps = []
    for sequence in repeated_sequences:
        mark = None
        for i in range(len(cipher_text)-length):
            if cipher_text[i:i+length] == sequence:
                if mark:
                    gaps.append(i-mark)
                mark = i
    return gaps
    
def analyze_gaps(gaps):
    mod_zero = {}
    for i in range(1, max_key_length+1):
        mod_zero[i] = 0
        for gap in gaps:
            if gap % i == 0:
                mod_zero[i] += 1
    
    #Sort potential key lengths based on most number of mod 0 hits
    length_candidates = [key for key,val in sorted(mod_zero.items(), key = lambda item: item[1], reverse=True)]
    return length_candidates
    
def candidate_freq_analysis(key_len, cipher_text):
    groups = []
    key = []
    for i in range(key_len):
        new_group = get_all_i_th_chars(cipher_text, key_len, i)
        groups.append(new_group)
        
    test_key = []
    for group in groups:
        scores = []
        for subkey in range(0,28):
            pt_candidate = decrypt(group, [subkey])
            score = freqAnalysis.englishFreqMatchScore(pt_candidate.upper())
            scores.append((score, subkey))
        scores = sorted(scores, key = lambda item: item[0], reverse=True)
        best = scores[0][0]
        subkeys = [score[1] for score in scores if score[0] == best]
        test_key.append(subkeys)

    all_keys = [[k] for k in test_key[0]]

    for i in test_key[1:]:
        placeholder = []
        for subkey in i:
            for ak in all_keys:
                tmp = copy.deepcopy(ak)
                tmp.append(subkey)
                placeholder.append(tmp)
        all_keys = placeholder
    
    best_score = 0
    pt = ''

    for key in all_keys:
        pt_candidate = decrypt(cipher_text, key)
        score = freqAnalysis.englishFreqMatchScore(pt_candidate.upper())
        if score > best_score:
            best_score = score
            pt = pt_candidate
   
    return (best_score, pt)
    
                
            
def test_two(cipher_text):
    repeated_sequences = find_repeat_sequences(cipher_text)
    gaps = find_gaps_between_repeats(cipher_text, repeated_sequences)
    key_length_candidates = analyze_gaps(gaps)
    
    all_scores = []
    for key_len_candidate in key_length_candidates:
        all_scores.append(candidate_freq_analysis(key_len_candidate, cipher_text))
    
    best = sorted(all_scores, key = lambda item: item[0], reverse = True)[0]
    return best

def find_pt(cipher_text, dictionary):
    if d := test_one(cipher_text, dictionary):
        print(f'My guess for the plaintext is: {d}')
        return
    else:
        score, pt = test_two(cipher_text)
        print(f'My guess for the plaintext is: {d}')
        return
    
start = time.time()
dictionary_one, dictionary_two = get_dictionaries()

cipher_text = input('Input your ciphertext: ')
find_pt(cipher_text, dictionary_one)
