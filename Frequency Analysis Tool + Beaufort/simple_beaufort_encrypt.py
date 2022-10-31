import random

alphabet = ' abcdefghijklmnopqrstuvwxyz'
max_key_len = 26

def do_shift(char, shift):
    new_index = shift - alphabet.index(char)
    if new_index < 0:
        new_index += 27
    return alphabet[new_index]

key_length = random.randint(0, 26)

key = [random.randint(0,26) for _ in range(key_length)]

plain_text = input('Enter PT: ')

ct = ''
i = 0
for c in plain_text:
    ct += do_shift(c, key[i])
    i+=1
    if i >= len(key):
        i = 0
print(ct)
