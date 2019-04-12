"""
Cooking MC's like a pound of bacon

>>> for i in range(256):
...     s = int(bytify(i) * 34, 2) ^ int(a, 16)
...     ans = s.to_bytes((s.bit_length() + 7) // 8, 'big').decode()
...     print(ans)
...     if(ans == "Cooking MC's like a pound of bacon"):
...         print(i)
...         break
>>> def bytify(num):
...     bd = bin(num)[2:]
...     bd = "0" * (8 - len(bd)) + bd
...     return bd

throw a try around it

>>>     ans = s.to_bytes((s.bit_length() + 7) // 8, 'big').decode('utf-8', 'surrogatepass')
(doesn't fix the fatal error not sure it changes anything tbh)