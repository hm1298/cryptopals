def hamming_distance(b1, b2):
    """
    Takes as input two strings b1 and b2 of equal length, each containing
    only 1s and 0s. Returns the Hamming Distance betwen them, interpreted
    as bitstrings.
    """
    return len(list(filter(lambda x: x == '1', list(xor(b1, b2)))))

def xor(b1, b2):
    """
    Takes as input two strings b1 and b2 of equal length, each containing
    only 1s and 0s. Returns b1 ^ b2, interpreted as bitstrings.
    """
    answer = ""
    for i in range(len(b1)):
        x, y = b1[i], b2[i]
        assert(x in "01" and y in "01")
        if x == y:
            answer += "0"
        else:
            answer += "1"
    assert(len(answer) == len(b2))
    return answer

def xor_encrypt(b, k):
    """
    Takes as input string b, containing only 1s and 0s, and integer k,
    0 <= k <= 255. Returns b single-key xor encrypted with key k. Pads
    b with 0s on the left if length is not a multiple of 8.
    """
    b = "0" * (len(b) % 8) + b
    key = bin(k)[2:].zfill(8) * ((len(b)) // 8)
    return xor(b, key)

def base64_to_bitstring(b64_str):
    """
    Takes as input a string of base64 characters. Returns a string of 1s
    and 0s, equivalent to the binary representation of b64_str interpreted
    as an integer. Trims padding.
    """
    digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    answer = ""
    padding = False
    for c in b64_str:
        if c in digits:
            assert(padding == False) #assumes only non-base64 characters appear at end
            answer += bin(digits.index(c))[2:].zfill(6)
        else:
            padding = True
            answer += "000000"
    bitlength = len(answer) #trims padding
    assert(bitlength == 6 * len(b64_str))
    if padding == True:
        assert(answer[-8:] == "00000000")
        while answer[-8:] == "00000000":
            answer = answer[:-8]
    elif bitlength % 8 != 0:
        q, r = divmod(bitlength, 8)
        print(answer)
        print(len(answer))
        assert(answer[q * 8:] == "0" * r)
        answer = answer[:q * 8]
    assert(len(answer) % 8 == 0)
    return answer

def text_to_bitstring(text):
    """
    Takes as input a string. Returns a string of 1s and 0s, equivalent
    to the utf-8 byte encoding of input string.
    """
    return bin(int.from_bytes(text.encode(), 'big'))[2:].zfill(8 * len(text))

assert(hamming_distance(text_to_bitstring("this is a test"), text_to_bitstring("wokka wokka!!!")) == 37)

def solve():
    """
    Opens and decodes the encrypted file.
    """
    f = open("6.txt", "r")
    arr = f.read().split("\n")
    f.close()
    b64_text = "".join(arr)
    ciphertext = base64_to_bitstring(b64_text)
    #ksize = find_keysize(ciphertext)[0]
    ksize = 29
    blocks = [] #creates ksize amount of blocks, each to be decrypted
    for i in range(ksize):
        blocks.append("")
        for j in range(len(ciphertext) // ksize):
            num = 8 * (ksize * j + i)
            if num < len(ciphertext):
                blocks[i] += (ciphertext[num: num+8])
    assert(len(ciphertext) == sum(list(map(lambda x: len(x), blocks))))
    assert(ciphertext[: 8*ksize] == "".join(list(map(lambda x: x[:8], blocks))))
    arr = []
    for b in blocks:
        arr.append(decrypt(b))
    ans = ""
    for i in range(len(arr[0][0])):
        for j in range(ksize):
            if i < len(arr[j][0]):
                ans += arr[j][0][i]
    print(ans)
    print("".join(list(map(lambda x: chr(x[1]), arr))))

def find_keysize(b):
    """
    Takes as input string b, containing only 1s and 0s. Returns the 3 most
    plausible keysizes for a Vigenere encryption.
    """
    performance = [[i, 0] for i in range(41)]
    for i in range(100): #this is an iteration to get a better average
        for k in range(2, 41): #this is the base code
            performance[k][1] += avg_4way(b[8*i:], k) / k
    ans = performance[2:]
    ans.sort(key=lambda x: x[1])
    return [ans[0][0], ans[1][0], ans[2][0]]

def avg_4way(b, k):
    """
    Returns float. Helper function for find_keysize(-).
    """
    b1, b2, b3, b4 = b[:8*k], b[8*k: 16*k], b[16*k: 24*k], b[24*k: 32*k]
    return (hamming_distance(b1, b2) + hamming_distance(b1, b3) + hamming_distance(b1, b4) \
    + hamming_distance(b2, b3) + hamming_distance(b2, b4) + hamming_distance(b3, b4)) / 6

def decrypt(b):
    """
    Takes as input string b, containing only 1s and 0s. Returns the most
    likely decryption along with the key value.
    """
    assert(len(b) % 8 == 0)
    tuples = []
    for i in range(256):
        attempt = xor_encrypt(b, i)
        if len(attempt) != 0:
            val = chi_squared_check(attempt)
            tuples.append((i, val))
    tuples.sort(key=lambda x: x[1])
    k = choose_less_capital(b, tuples[0][0], tuples[1][0])
    plaintext = int(xor_encrypt(b, k), 2).to_bytes(len(b) // 8, 'big').decode('utf-8', 'ignore')
    return (plaintext, k)

def chi_squared_check(b):
    """
    Takes as input bitstring b and returns a float representing the
    likelihood that the string corresponding to b is plaintext.
    """
    expected_frequencies = {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, \
    'd': 0.04253, 'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094, \
    'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025, 'm': 0.02406, \
    'n': 0.06749, 'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987, \
    's': 0.06327, 't': 0.09056, 'u': 0.02758, 'v': 0.00978, 'w': 0.0236, \
    'x': 0.0015, 'y': 0.01974, 'z': 0.00074}
    actual_occurrences = freq_dist(b)
    N = sum_dict(actual_occurrences)
    if N < 0.6 * len(b) // 8:
        return 999999
    chi2 = 0
    arr = []
    for key in expected_frequencies:
        arr.append((actual_occurrences[key] - N * expected_frequencies[key]) ** 2 / (N * expected_frequencies[key]))
    arr.sort()
    chi2 = sum(arr[:24])
    return chi2    

def freq_dist(b):
    """
    Takes as input bitstring b and returns a dictionary containing the
    frequencies of (non-case-sensitive) letters in the string represented
    by b.
    """
    d = {}
    for c in "abcdefghijklmnopqrstuvwxyz":
        d[c] = 0
    assert(len(b) % 8 == 0)
    for i in range(len(b) // 8):
        o = int(b[8*i: 8*i+8], 2)
        if 97 <= o and o < 123:
            d[chr(o)] += 1
        if 65 <= o and o < 91:
            d[chr(o + 32)] += 1
    return d

def sum_dict(d):
    """
    Returns the sum of the values in dictionary d.
    """
    total = 0
    for k in d:
        total += d[k]
    return total

def choose_less_capital(b, k1, k2):
    """
    This is a bit messy. Could use some cleaning up. Helper function for 
    chi_squared_check(-).
    """
    b1, b2 = xor_encrypt(b, k1), xor_encrypt(b, k2)
    total1, total2 = 0, 0
    for i in range(len(b) // 8):
        o1 = int(b1[8*i: 8*i+8], 2)
        o2 = int(b2[8*i: 8*i+8], 2)
        if 65 <= o1 and o1 < 91:
            total1 += 1
        if 65 <= o2 and o2 < 91:
            total2 += 1
    if total1 <= total2:
        return k1
    return k2

assert(decrypt(base64_to_bitstring('Gzc3MzE2P3gVG38reDQxMz14OXgoNy02PHg3Png6OTs3Ng=='))[0] == "Cooking MC's like a pound of bacon")

solve()











