def hex_to_base64(a):
	"""
	Takes as input string a containing alphanumeric characters 0-9, a-f only.
	Returns the base-64 representation of hexadecimal a.
	"""
	s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
	bitstring = bin(int(a, 16))[2:].zfill(len(a) * 4)
	answer = ""
	while bitstring != "":
		val = bitstring[:6]
		answer += s[int(val, 2)]
		if len(bitstring) < 6:
			break
		bitstring = bitstring[6:]
	while len(answer) % 4 != 0:
		answer += "="
	return answer

assert(hex_to_base64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d") == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t")