"""
I still need to come back and fix the output. Need something to distinguish
upper and lower case answers (xor 32 bit flipped). Maybe check ASCII values
present in plaintext, presumed should be nearly all in range(32, 127).
"""

import math

def decrypt(a):
    """
    Takes as input a string of alphanumeric characters 0-9, a-f only. Prints
    a string of plaintext recovered from treating the input as hexidecimal
    bytecode encrypted under a single byte xor of unknown key.
    """
    for i in range(256):
        s = int(bytify(i) * (len(a) // 2), 2) ^ int(a, 16)
        attempt = s.to_bytes((s.bit_length() + 7) // 8, 'big').decode('utf-8', 'ignore')
        if len(attempt) != 0:
            val = check(attempt)
            if(check(attempt) < 4):
                print("#" + str(i) + ": " + attempt)

def bytify(num):
    """
    Takes as input an integer num, 0 <= num < 256. Returns a string of 8
    characters, 0 or 1, the binary representation of num.
    """
    bd = bin(num)[2:]
    bd = "0" * (8 - len(bd)) + bd
    return bd

expected_frequency = {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, \
'd': 0.04253, 'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094, \
'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025, 'm': 0.02406, \
'n': 0.06749, 'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987, \
's': 0.06327, 't': 0.09056, 'u': 0.02758, 'v': 0.00978, 'w': 0.0236, \
'x': 0.0015, 'y': 0.01974, 'z': 0.00074}

def letter_frequencies(s):
    """
    Takes as input a string s. Returns a dictionary keyed a-z, the values of
    which are the percent of characters in s equal to the keyed letter or its
    uppercase version.
    """
    counts = {}
    l = len(s)
    for c in 'abcdefghijklmnopqrstuvwxyz':
        counts[c] = 0
    for c in s:
        if ord(c) < 65 or ord(c) > 122 or (ord(c) < 97 and ord(c) > 90):
            continue
        if c in counts:
            counts[c] += 1
        else:
            counts[chr(ord(c) + 32)] += 1
    for key in counts:
        counts[key] /= l
    return counts

def normalize_frequencies(d):
    """
    Takes as input a dictionary d. Scales the values of d to sum to 1.
    """
    total = sum_dict(d)
    if total != 0:
        for k in d:
            d[k] /= total


def sum_dict(d):
    """
    Takes as input a dictionary d. Returns the sum of the values in d.
    """
    total = 0
    for k in d:
        total += d[k]
    return total

def abs_diff(d1, d2):
    """
    Takes as input two dictionaries d1 and d2. Returns the sum of
    displacements between two probability dictionaries.
    """
    total = 0
    try:
        for k in d1:
            total += math.sqrt(abs(d1[k] - d2[k]))
    except KeyError:
        print("Dictionary keys do not match.")
    return total

def check(s):
    """
    Returns the absolute difference between the string s and
    its expected letter frequencies.

    This is my first attempt at applying cryptanalysis to ciphertext with
    unknown key. As such, it is rather naive and ineffective, although it
    proved sufficient for this challenge.
    """
    d = letter_frequencies(s)
    normalize_frequencies(d)
    return abs_diff(d, expected_frequency)

decrypt("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")