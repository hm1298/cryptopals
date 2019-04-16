class F2Poly:
    def __init__(self, arr):
        self.coeffs = [arr[i] % 2 for i in range(len(arr))]
        self.trim()

    def __str__(self):
        text = ""
        for i in range(len(self)-1, -1, -1):
            if self.coeffs[i] == 0:
                continue
            if i == 0:
                term = "1"
            if i == 1:
                term = "x"
            if i > 1:
                term = "x^" + str(i)
            text += " + " + term
        if len(text) == 0:
            text = "0"
        else:
            text = text[3:]
        return text

    def __add__(self, other):
        arr = []
        n = min(len(self), len(other))
        for i in range(n):
            arr.append(self.coeffs[i] ^ other.coeffs[i])
        arr += self.coeffs[n:] + other.coeffs[n:]
        return F2Poly(arr)

    def __sub__(self, other):
        return self + other

    def __neg__(self):
        return self

    def __eq__(self, other):
        return self.coeffs == other.coeffs

    def __mul__(self, other):
        result = F2Poly([])
        for i in range(len(other)):
            if other.coeffs[i] == 1:
                result += self.mult_by_x(i)
        return result

    def __divmod__(self, other):
        r, q = F2Poly(self.coeffs), F2Poly([])
        if len(other) == 0:
            raise ZeroDivisionError
        while len(r) >= len(other):
            k = len(r) - len(other)
            q_partial = F2Poly([1]).mult_by_x(k)
            r = r - other * q_partial
            q += q_partial
        return q, r

    def __len__(self):
        self.trim()
        return len(self.coeffs)

    def deg(self):
        return max(0, len(self) - 1)

    def trim(self):
        arr = self.coeffs
        for i in range(len(arr), 0, -1):
            if arr[i - 1] != 0:
                arr = arr[:i]
                break
            if i == 1:
                arr = []
        self.coeffs = arr

    def mult_by_x(self, exp=1):
        return F2Poly(([0] * exp) + self.coeffs)

    #could use __call__ instead if later I decide I prefer that functionality
    def eval_at(self, n):
        result = 0
        for k in range(len(self)):
            result += self.coeffs[k] * (n ** k)
        return result


class F256:
    def __init__(self, n):
        self.value = n
        self.reduce()

    def __str__(self):
        return bin(self.value)[2:].zfill(8)

    def __add__(self, other):
        return F256(self.value ^ other.value)

    def __sub__(self, other):
        return self + other

    def __mul__(self, other):
        a, b = self.value, other.value
        ans = 0
        while a != 0:
            if a % 2 == 1:
                ans = ans ^ b
            a = a // 2
            b = b * 2
            if b > 255:
                b = b ^ 283
        return F256(ans)

    def __div__(self, other):
        return self * self.inverse()

    def __neg__(self):
        return self

    def __eq__(self, other):
        return self.value == other.value

    def inverse(self):
        tup = extended_euclidean(F2Poly([1,1,0,1,1,0,0,0,1]), self.to_poly())
        return F256(tup[1].eval_at(2))

    def to_poly(self):
        return F2Poly(self.to_list()[::-1])

    def to_list(self):
        return list(map(lambda x: int(x), list(str(self))))

    def reduce(self):
        n = self.value
        while n > 255:
            k = 2 ** (n.bit_length() - 1)
            n = n ^ (283 * (k // 256))
        self.value = n

def extended_euclidean(a, b):
    """
    """
    if len(b) > len(a):
        (x, y, d) = eea_for_f256(b, a)
        return (y, x, d)

    x1, x2, y1, y2 = F2Poly([0]), F2Poly([1]), F2Poly([1]), F2Poly([0])
    while len(b) > 0:
        q, r = divmod(a, b)
        x = x2 - q * x1
        y = y2  - q * y1
        a, b, x2, x1, y2, y1 = b, r, x1, x, y1, y

    return x2, y2, a


a, b, c = F256(int("57", 16)), F256(int("13", 16)), F256(int("fe", 16))
X, Y, Z = F2Poly([1, 0, 1, 1]), F2Poly([1, 1, 0, 1, 1, 0, 0, 0, 1]), F2Poly([1, 0, 0, 0, 0, 1, 1, 1])
assert(divmod(X * Z, Y)[1] == F2Poly([1]))
assert(F256(Z.eval_at(2)).inverse() == F256(X.eval_at(2)))
assert(a * b == c)
