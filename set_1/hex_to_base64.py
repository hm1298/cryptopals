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

assert(hex_to_base64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d") == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t")