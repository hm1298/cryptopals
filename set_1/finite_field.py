import math

class F256:
    def __init__(self, n):
        self.value = n

    def __str__(self):
        return bin(self.value)[2:].zfill(8)

    def __add__(self, other):
        return self.value ^ other.value

    def __sub__(self, other):
        return self + other

    def __mul__(self, other):
        a, b = self.value, other.value
        while b > 255:
            k = 2 ** int(math.log(b + 0.5, 2))
            b = b ^ (283 * (k // 256))
        ans = 0
        while a != 0:
            if a % 2 == 1:
                ans = ans ^ b
            a = a // 2
            b = b * 2
            if b > 255:
                b = b ^ 283
        return ans

    def __div__(self, other):
        return self * self.inverse()

    def __neg__(self):
        return self

    def inverse(self):
        if self.value == 0:
            return 0
        return "tbd"