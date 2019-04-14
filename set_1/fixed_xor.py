def hex_xor(s1, s2):
	"""
	Takes as input two strings of equal length, each containing alphanumeric
	characters 0-9, a-f only. Returns the hexadecimal output of s1 xor s2.
	"""
	return hex(int(s1, 16) ^ int(s2, 16))[2:]

assert(hex_xor("1c0111001f010100061a024b53535009181c", "686974207468652062756c6c277320657965") == "746865206b696420646f6e277420706c6179")