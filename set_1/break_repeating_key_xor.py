import math
from functools import reduce

def solve():
	"""
	"""
	f = open('6.txt', 'r')
	arr = f.read().split('\n')
	f.close()
	base64 = "".join(arr)
	ciphertext = base64_to_hex(base64)
	keysizes = find_keysize(ciphertext) #input is given as hex
	keysize = keysizes[1]
	#decrypt(ciphertext[::keysize])

def xor(s1, s2):
	"""
	Returns the hexadecimal output of s1 xor s2.
	"""
	return hex(int(text_to_bits(s1), 2) ^ int(text_to_bits(s2), 2))[2:].zfill(2 * len(s1))

def text_to_bits(s):
	return bin(int.from_bytes(s.encode(), 'big'))[2:]

def xor_encrypt(s, key):
	"""
	"""
	s2 = key * (len(s) // len(key)) + key[:(len(s) % len(key))]
	assert(len(s) == len(s2))
	return xor(s, s2)

def hamming_distance(s1, s2):
	ones_and_zeroes = bin(int(xor(s1, s2), 16))[2:]
	return reduce((lambda x, y: int(x) + int(y)), list(ones_and_zeroes))

assert(hamming_distance("this is a test", "wokka wokka!!!") == 37)

def find_keysize(h):
	"""
	Takes as input hexadecimal ciphertext. Returns possible keysize.
	"""
	s = bin(int(h, 16))[2:].zfill(4 * len(h))
	arr = []
	for k in range(2, 40):
		s1, s2, s3, s4 = s[:k], s[k: 2*k], s[2*k: 3*k], s[3*k: 4*k]
		avg = (hamming_distance(s1, s2) + hamming_distance(s2, s3) \
			+ hamming_distance(s3, s4)) / 3
		val = avg / k
		arr.append((k, val))
	arr.sort(key=lambda x: x[1])
	print(arr)
	return list(map(lambda x: x[0], arr[:3]))

def hex_to_base64(a):
	"""
	Returns the base-64 representation of hexadecimal a.
	"""
	s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
	backwards = bin(int(a, 16))[2:][::-1]
	answer = ""
	for i in range(0, len(backwards), 6):
		val = int(backwards[i: i + 6][::-1], 2)
		answer += s[val]
	return answer[::-1]

def base64_to_hex(a):
	"""
	Returns the hex representation of base-64 a.
	"""
	s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
	answer = ""
	a = a[::-1]
	for i in range(0, len(a), 2):
		try:
			n = s.index(a[i]) + 64 * s.index(a[i + 1])
			answer = hex(n)[2:].zfill(3) + answer
		except ValueError:
			print("couldn't find " + a[i:i+2])
	return answer

assert(hex_to_base64(base64_to_hex("SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t")) == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t")

def decrypt():
	"""
	Takes as input 
	"""

solve()