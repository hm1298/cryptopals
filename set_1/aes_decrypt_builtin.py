from base64 import b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import unpad

key = b'YELLOW SUBMARINE'
file_in = open("7.txt", "r")
data_enc = "".join(file_in.read().split('\n'))
ciphertext = b64decode(data_enc)
file_in.close()

cipher = AES.new(key, AES.MODE_ECB)
data_dec = unpad(cipher.decrypt(ciphertext), AES.block_size)
print(data_dec.decode())
