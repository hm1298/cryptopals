def xor(s1, s2):
	"""
	Takes as input two strings of ASCII characters. Returns the hexadecimal
	output of the bytecode of s1 xor the bytecode of s2.
	"""
	return hex(int(text_to_bits(s1), 2) ^ int(text_to_bits(s2), 2))[2:].zfill(2 * len(s1))

def text_to_bits(text):
	"""
	Takes as input a string of ASCII characters. Returns a string of bits
	representing their bytecode.
	"""
	return bin(int.from_bytes(text.encode(), 'big'))[2:]

def xor_encrypt(s, key):
	"""
	Takes as input two strings. Returns a string of alphanumeric characters
	0-9, a-f only representing the hexadecimal output of xor encrypting s
	with repeating key key.
	"""
	if len(s) < len(key):
		key = key[:len(s)]
	s2 = key * (len(s) // len(key)) + key[:(len(s) % len(key))]
	assert(len(s) == len(s2))
	return xor(s, s2)

assert(xor_encrypt("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal", "ICE") == "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")