import math

def decrypt():
    """
    Returns
    """
    f = open('4.txt', 'r')
    arr = f.read().split('\n')
    base = listify(expected_frequency)
    f.close()
    num_line, smallest_val = 0, 999
    for j in range(len(arr)):
        line = arr[j]
        d, length = {}, 0
        for i in range(0, len(line), 2):
            c = line[i: i + 2]
            if c not in d:
                d[c] = 0
            d[c] += 1
            length += 1
        freqs = list(map(lambda x: x / length, listify(d)))
        val = abs_diff_arrs(freqs, base)
        if val < smallest_val:
            smallest_val = val
            num_line = j
    a = arr[num_line]
    for i in range(256):
        s = int(bytify(i) * (len(a) // 2), 2) ^ int(a, 16)
        attempt = s.to_bytes((s.bit_length() + 7) // 8, 'big').decode('utf-8', 'ignore')
        if len(attempt) != 0:
            val = check(attempt)
            if(check(attempt) < 4):
                print("Line #" + str(num_line) + " xor'ed with " + str(i) + " : " + attempt.strip())

def bytify(num):
    bd = bin(num)[2:]
    bd = "0" * (8 - len(bd)) + bd
    return bd

def listify(d):
    arr = []
    for key in d:
        arr.append(d[key])
    arr.sort(reverse=True)
    return arr

def abs_diff_arrs(a1, a2):
    total = 0
    for i in range(min(len(a1), len(a2))):
        total += math.sqrt(abs(a1[i] - a2[i]))
    return total

expected_frequency = {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, \
'd': 0.04253, 'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094, \
'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025, 'm': 0.02406, \
'n': 0.06749, 'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987, \
's': 0.06327, 't': 0.09056, 'u': 0.02758, 'v': 0.00978, 'w': 0.0236, \
'x': 0.0015, 'y': 0.01974, 'z': 0.00074}
random_frequency = {}
for c in 'abcdefghijklmnopqrstuvwxyz':
    random_frequency[c] = 1 / 26

def letter_frequencies(s):
    """
    Returns a dictionary keyed a-z with values the percent
    of keyed character (upper or lower) in s.
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
    Returns nothing. Scales the values of d to sum to 1.
    """
    total = sum_dict(d)
    if total != 0:
        for k in d:
            d[k] /= total


def sum_dict(d):
    """
    Returns the sum of the values in dictionary d.
    """
    total = 0
    for k in d:
        total += d[k]
    return total

def abs_diff(d1, d2):
    """
    Returns the sum of displacements between two probability
    dictionaries.
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
    """
    d = letter_frequencies(s)
    normalize_frequencies(d)
    return abs_diff(d, expected_frequency)

decrypt()