"""
In all of the following methods, we take the finite field of order 256 to be
identified with the quotient ring F_2[x] / (x^8 + x^4 + x^3 + x + 1).
"""
"""
def aes_encrypt(plaintext, word):
	state = plaintext

	AddRoundKey(state, word[:4])

	for i in range(1, 10):
		SubBytes(state)
		ShiftRows(state)
		MixColumns(state)
		AddRoundKey(state, word[4*i: 4*(i+1)])

	SubBytes(state)
	ShiftRows(state)
	AddRoundKey(state, word[40:44])

	return state
"""

def SubBytes(state):
	"""
	Takes as input a double array of strings of bits. Returns a double array
	of strings of bits with the appropriate nonlinear transformation applied
	to each string. Each string has length 8.
	"""
	assert(type(state) == list and type(state[0]) == list)
	assert(type(state[0][0]) == str and len(state[0][0]) == 8)
	for i in range(len(state)):
		for j in range(len(state[i])):
			b = field_inverse(state[i][j])
			assert(len(b) == 8)
			b2 = ""
			c = "01100011"
			for k in range(8):
				if (b[k]=="1") ^ (b[(k-4)%8]=="1") ^ (b[(k-5)%8]=="1") ^ \
					(b[(k-6)%8]=="1") ^ (b[(k-7)%8]=="1") ^ (c[k]=="1"):
					b2 += "1"
				else:
					b2 += "0"
			state[i][j] = b2
	return state

def ShiftRows(state):
	"""
	Takes as input a double array of strings of bits. Returns a double array
	of strings of bits with each row shifted by a constant amount.
	"""
	for i in range(len(state)): #len(state) should be 4
		Nb = len(state[i])
		state[i] = [state[i][(j + i) % Nb] for j in range(Nb)]
	return state

def MixColumns(state):
	"""
	Takes as input a double array of strings of bits. Returns a double array
	of strings of bits with a transformation applied to each column, taken
	as one long bitstring.
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

def AddRoundKey(state, key):
	"""
	Takes as input a double array of strings of bits (state) and a string
	key.
	"""

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

assert(mult_for_f256(bitify(int("57", 16)), bitify(int("13", 16))) == bitify(int("fe", 16)))
assert(divmod_for_f2_polys("100011011", "00001101") == ("00111000", "00000011"))
assert(field_inverse("11100001") == "00001101")
assert(field_inverse("00000001") == "00000001")
assert(SubBytes([["00010111", "01100111", "11000010", "11010010"]]) == [["11110000", "10000101", "00100101", "10110101"]])
assert(ShiftRows([[(0, 0), (0, 1), (0, 2), (0, 3)], [(1, 0), (1, 1), (1, 2), (1, 3)], [(2, 0), (2, 1), (2, 2), (2, 3)], [(3, 0), (3, 1), (3, 2), (3, 3)]]) == [[(0, 0), (0, 1), (0, 2), (0, 3)], [(1, 1), (1, 2), (1, 3), (1, 0)], [(2, 2), (2, 3), (2, 0), (2, 1)], [(3, 3), (3, 0), (3, 1), (3, 2)]])
#assert MixColumns