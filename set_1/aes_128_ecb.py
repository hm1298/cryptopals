"""
In all of the following methods, we take the finite field of order 256 to be
identified with the quotient ring F_2[x] / (x^8 + x^4 + x^3 + x + 1).
"""
from finite_field import *
from base64 import b64decode

def solve():
    key = b'YELLOW SUBMARINE'
    file_in = open("7.txt", "r")
    data_enc = "".join(file_in.read().split('\n'))
    file_in.close()

    ciphertext = b64decode(data_enc)
    word = [[bitify(key[4*i+j]) for j in range(4)] for i in range(4)]
    result, count = "", 0
    q, r = divmod(len(ciphertext), 16)
    while count <= q:
        if count == q and r == 0:
            break
        state = [[bitify(ciphertext[16*count+4*j+i]) for j in range(4)] for i in range(4)]
        state = aes_decrypt(state, word)
        result += "".join(list(map(lambda x: chr(int(x, 2)), [state[i % 4][i // 4] for i in range(16)])))
        count += 1

    print(result)

def hex_aes_enc(plaintext, word):
    """
    Input is assumed to be in string hexadecimal format. Padding is added.
    Key must be proper length.
    """
    key = [[bitify(int(word[2*(4*i+j):2*(4*i+j+1)], 16)) for j in range(4)] for i in range(4)]
    result = []
    q, r = divmod(len(plaintext), 32)
    plaintext += "f" * (32 - r)
    count, result = 0, ""
    while count <= q:
        if count == q and r == 0:
            break
        state = aes_encrypt([[bitify(int(plaintext[32*count+2*(4*j+i):32*count+2*(4*j+i+1)], 16)) for j in range(4)] for i in range(4)], key)
        result += "".join(list(map(lambda x: hex(int(x, 2))[2:].zfill(2), [state[i % 4][i // 4] for i in range(16)])))
        count += 1
    return result

def aes_encrypt(plaintext, word):
    """
    Input is assumed to be in double array binary string format.
    """
    state = plaintext
    key_schedule = KeyExpansion(word)

    AddRoundKey(state, next(key_schedule))

    for i in range(1, 10):
        SubBytes(state)
        ShiftRows(state)
        MixColumns(state)
        AddRoundKey(state, next(key_schedule))

    SubBytes(state)
    ShiftRows(state)
    AddRoundKey(state, next(key_schedule))

    return state

def aes_decrypt(plaintext, word):
    """
    Input is assumed to be in double array binary string format.
    """
    state = plaintext
    key_schedule = KeyExpansion(word)
    keys = [next(key_schedule) for i in range(11)]

    AddRoundKey(state, keys[10])
    InvShiftRows(state)
    InvSubBytes(state)

    for i in range(9, 0, -1):
        AddRoundKey(state, keys[i])
        InvMixColumns(state)
        InvShiftRows(state)
        InvSubBytes(state)

    AddRoundKey(state, keys[0])

    return state

def SubBytes(state):
    """
    Takes as input a double array of strings of bits. Transforms input in place
    with the appropriate nonlinear transformation applied to each string. Each
    string has length 8.
    """
    #assert(type(state) == list and type(state[0]) == list)
    #assert(type(state[0][0]) == str and len(state[0][0]) == 8)
    for i in range(len(state)):
        state[i] = SubWord(state[i])

def InvSubBytes(state):
    """
    """
    for i in range(len(state)):
        for j in range(len(state[i])):
                b = state[i][j]
                b2 = ""
                c = "00000101"
                for k in range(8):
                    if (b[(k-2)%8]=="1") ^ (b[(k-5)%8]=="1") ^ \
                        (b[(k-7)%8]=="1") ^ (c[k]=="1"):
                        b2 += "1"
                    else:
                        b2 += "0"
                state[i][j] = field_inverse(b2)

def ShiftRows(state):
    """
    Takes as input a double array of strings of bits. Transforms input in place
    with each row shifted by a constant amount.
    """
    for i in range(len(state)): #len(state) should be 4
        Nb = len(state[i])
        state[i] = [state[i][(j + i) % Nb] for j in range(Nb)]

def InvShiftRows(state):
    """
    """
    for i in range(len(state)):
        Nb = len(state[i])
        state[i] = [state[i][(j - i) % Nb] for j in range(Nb)]

def MixColumns(state):
    """
    Takes as input a double array of strings of bits. Transforms input in place
    with a transformation applied to each column, taken as one long bitstring.
    """
    b1, b2 = "00000010", "00000011"
    for j in range(len(state[0])):
        s0, s1, s2, s3 = state[0][j], state[1][j], state[2][j], state[3][j]
        state[0][j] = bitify(int(mult_for_f256(b1, s0), 2) ^ int( \
            mult_for_f256(b2, s1), 2) ^ int(s2, 2) ^ int(s3, 2))
        state[1][j] = bitify(int(s0, 2) ^ int(mult_for_f256(b1, s1), 2) ^ \
            int(mult_for_f256(b2, s2), 2) ^ int(s3, 2))
        state[2][j] = bitify(int(s0, 2) ^ int(s1, 2) ^ int(mult_for_f256( \
            b1, s2), 2) ^ int(mult_for_f256(b2, s3), 2))
        state[3][j] = bitify(int(mult_for_f256(b2, s0), 2) ^ int(s1, 2) ^ \
            int(s2, 2) ^ int(mult_for_f256(b1, s3), 2))

def InvMixColumns(state):
    """
    terrible look at that faux-indexing on variable names eugh
    """
    b1, b2, b3, b4 = "00001110", "00001011", "00001101", "00001001"
    for j in range(len(state[0])):
        s0, s1, s2, s3 = state[0][j], state[1][j], state[2][j], state[3][j]
        state[0][j] = bitify(int(mult_for_f256(b1, s0), 2) ^ int( \
            mult_for_f256(b2, s1), 2) ^ int(mult_for_f256(b3, s2), 2) \
            ^ int(mult_for_f256(b4, s3), 2))
        state[1][j] = bitify(int(mult_for_f256(b4, s0), 2) ^ int( \
            mult_for_f256(b1, s1), 2) ^ int(mult_for_f256(b2, s2), 2) \
            ^ int(mult_for_f256(b3, s3), 2))
        state[2][j] = bitify(int(mult_for_f256(b3, s0), 2) ^ int( \
            mult_for_f256(b4, s1), 2) ^ int(mult_for_f256(b1, s2), 2) \
            ^ int(mult_for_f256(b2, s3), 2))
        state[3][j] = bitify(int(mult_for_f256(b2, s0), 2) ^ int( \
            mult_for_f256(b3, s1), 2) ^ int(mult_for_f256(b4, s2), 2) \
            ^ int(mult_for_f256(b1, s3), 2))

def AddRoundKey(state, round_key):
    """
    Takes as input a double array of strings of bits (state) and an iterable
    gen that gives the next words in the key schedule.
    """
    for i in range(len(state)):
        for j in range(len(state[i])):
            state[i][j] = bitify(int(state[i][j], 2) ^ int(round_key[i][j], 2))

def KeyExpansion(key):
    """
    Takes as input a key. Returns a generator for the key schedule.
    """
    def key_schedule():
        state = [line[:] for line in key]
        Rcon = ["00000001", "00000000", "00000000","00000000"]
        while True:
            yield [[state[i][j] for i in range(4)] for j in range(4)]
            rot = RotWord(state[3])
            sub = SubWord(rot)
            state[0] = XorWord(XorWord(Rcon, sub), state[0])
            for i in range(1, 4):
                state[i] = XorWord(state[i-1], state[i])
            Rcon[0] = mult_for_f256(Rcon[0], "00000010")
    return key_schedule()

def SubWord(word):
    """
    Takes as input an array of strings of bits.
    """
    result = []
    for i in range(len(word)): #len(word) should be 4
        b = field_inverse(word[i])
        assert(len(b) == 8)
        b2 = ""
        c = "01100011"
        for k in range(8):
            if (b[k]=="1") ^ (b[(k-4)%8]=="1") ^ (b[(k-5)%8]=="1") ^ \
                (b[(k-6)%8]=="1") ^ (b[(k-7)%8]=="1") ^ (c[k]=="1"):
                b2 += "1"
            else:
                b2 += "0"
        result.append(b2)
    return result

def RotWord(word):
    """
    Takes as input an array of strings of bits.
    """
    result = []
    for i in range(len(word)): #len(word) should be 4
        result.append(word[(i + 1) % len(word)])
    return result

def XorWord(word1, word2):
    """
    Takes as input two arrays of strings of bits.
    """
    result = []
    for i in range(len(word1)): #assumes word1 and word2 have same length
        result.append(bitify(int(word1[i], 2) ^ int(word2[i], 2)))
    return result

def field_inverse(b):
    """
    Takes as input a string of bits of length 8. Returns a string of bits
    of length 8.
    """
    if b == "00000000":
        return b
    tup = eea_for_f256("100011011", b)
    assert(tup[2] == "00000001")
    return tup[1]

def eea_for_f256(a, b):
    """
    Takes as input two strings of bits of length ?. Returns a tuple of
    three strings of bits of length 8.
    """
    if int(b, 2) > int(a, 2):
        (x, y, d) = eea_for_f256(b, a)
        return (y, x, d)

    if int(b, 2) == 0:
        return ("00000001", "00000000", a)

    x1, x2, y1, y2 = 0, 1, 1, 0
    while int(b, 2) > 0:
        q, r = divmod_for_f2_polys(a, b)
        x = x2 ^ int(mult_for_f256(q, bitify(x1)), 2)
        y = y2 ^ int(mult_for_f256(q, bitify(y1)), 2)
        a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y

    return (bitify(x2), bitify(y2), a)

def divmod_for_f2_polys(a, b):
    """
    Takes as input two strings of bits. Returns a tuple of two strings of
    bits.
    """
    x, y, q = int(a, 2), int(b, 2), 0
    while x >= y:
        k = len(bin(x)) - len(bin(y))
        q += 2 ** k
        x = x ^ (y * (2 ** k))
    return bitify(q), bitify(x)


def mult_for_f256(a, b):
    """
    Takes as input two strings of bits of length 8. Returns a tuple of
    three strings of bits of length 8, corresponding to the product of
    a and b in the finite field of order 256.
    """
    if int(b, 2) > int(a, 2):
        return mult_for_f256(b, a)
    ans = 0
    for i in range(8):
        if a[7 - i] == "1":
            ans = ans ^ int(b, 2)
        c = b[0]
        b = b[1:] + "0"
        if c == "1":
            b = bitify(int(b, 2) ^ 27)
    return bitify(ans)

def bitify(n):
    """
    Takes as input an integer n, 0 <= n < 512. Returns a string of bits of
    length 8, corresponding to the binary representation of n.
    """
    assert(n >= 0 and n < 512)
    return bin(n)[2:].zfill(8)

def format(b):
    """
    Takes as input a string of bits. Returns string of input as hexadecimal.
    """
    return hex(int(b, 2))[2:].zfill(2)

def format_state(state):
    """
    Takes as input a double array of strings of bits. Returns output of the
    same type with format() applied to each element of the double array.
    """
    output = []
    for i in range(len(state)):
        output.append([])
        for elt in state[i]:
            output[i].append(format(elt))
    return output

"""
assert(mult_for_f256(bitify(int("57", 16)), bitify(int("13", 16))) == bitify(int("fe", 16)))
assert(divmod_for_f2_polys("100011011", "00001101") == ("00111000", "00000011"))
assert(field_inverse("11100001") == "00001101")
assert(field_inverse("00000001") == "00000001")
#probly doesnt work assert(SubWord(["00010111", "01100111", "11000010", "11010010"]) == ["11110000", "10000101", "00100101", "10110101"])
#broken assert(ShiftRows([[(0, 0), (0, 1), (0, 2), (0, 3)], [(1, 0), (1, 1), (1, 2), (1, 3)], [(2, 0), (2, 1), (2, 2), (2, 3)], [(3, 0), (3, 1), (3, 2), (3, 3)]]) == [[(0, 0), (0, 1), (0, 2), (0, 3)], [(1, 1), (1, 2), (1, 3), (1, 0)], [(2, 2), (2, 3), (2, 0), (2, 1)], [(3, 3), (3, 0), (3, 1), (3, 2)]])
#assert MixColumns


#ended up not using any of this... for now
a, b, c = F256(int("57", 16)), F256(int("13", 16)), F256(int("fe", 16))
X, Y, Z = F2Poly([1, 0, 1, 1]), F2Poly([1, 1, 0, 1, 1, 0, 0, 0, 1]), F2Poly([1, 0, 0, 0, 0, 1, 1, 1])
assert(divmod(X * Z, Y)[1] == F2Poly([1]))
assert(F256(Z.eval_at(2)).inverse() == F256(X.eval_at(2)))
assert(a * b == c)
assert(format("11100001") == "e1" and format("00001011") == "0b")


raw_state = [["32", "88", "31", "e0"], ["43", "5a", "31", "37"], ["f6", "30", "98", "07"], ["a8", "8d", "a2", "34"]]
#raw_state = [["19", "a0", "9a", "e9"], ["3d", "f4", "c6", "f8"], ["e3", "e2", "8d", "48"], ["be", "2b", "2a", "08"]]
state = [list(map(lambda x: bitify(int(x, 16)), line)) for line in raw_state]
raw_key = [["2b", "7e", "15", "16"], ["28", "ae", "d2", "a6"], ["ab", "f7", "15", "88"], ["09", "cf", "4f", "3c"]]
key = [list(map(lambda x: bitify(int(x, 16)), line)) for line in raw_key]

#print(format_state(aes_encrypt(state, key)))
#print(hex_aes_enc("00112233445566778899aabbccddeeff", "000102030405060708090a0b0c0d0e0f"))

raw_state2, raw_key2 = [["00", "11", "22", "33"], ["44", "55", "66", "77"], ["88", "99", "aa", "bb"], ["cc", "dd", "ee", "ff"]], [["00", "01", "02", "03"], ["04", "05", "06", "07"], ["08", "09", "0a", "0b"], ["0c", "0d", "0e", "0f"]]
state2, key2 = [[bitify(int(raw_state2[i][j], 16)) for i in range(4)] for j in range(4)], [list(map(lambda x: bitify(int(x, 16)), line)) for line in raw_key2]
print(format_state(state2))
aes_encrypt(state2, key2)
aes_decrypt(state2, key2)
print(format_state(state2))
"""

solve()