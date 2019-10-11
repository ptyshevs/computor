import sys
from Term import *
from Operator import *
from Variable import *

class Complex(Term):
    def __init__(self, re, img=0):
        self.re = re
        self.img = img
        if type(img) is int:
            self.img = Rational(img)
    
    def __repr__(self):
        s = str(self.re)
        if s == '0':
            s = ''
        if self.img != 0:
            if s:
                s += '+' if self.img >= Rational(0) else '-'
                s += f'{abs(self.img)}i'
            else:
                s += f'{self.img}i'
        return s
    
    def __add__(self, o):
        if type(o) not in [Complex, Rational]:
            raise NotImplementedError()
        if type(o) is Complex:
            return Complex(self.re + o.re, self.img + o.img)
        else:
            return Complex(self.re + o, self.img)
    
    def __sub__(self, o):
        if type(o) is Rational:
            return Complex(self.re - o, self.img)
        elif type(o) is Complex:
            return Complex(self.re - o.re, self.img - o.img)
        else:
            raise NotImplementedError()
    
    def __mul__(self, o):
        if type(o) is Rational:
            o = Complex(o)
        if type(o) is Complex:
            return Complex(self.re * o.re - self.img * o.img, self.re * o.img + self.img * o.re)
        else:
            raise NotImplementedError()

    def __neg__(self):
        return Complex(-self.re, -self.img)
    
    def __pos__(self):
        return Complex(self.re, self.img)

class Rational(Term):
    def __init__(self, p, q=1):
        if q == 0:
            raise ValueError(f"Failed to create rational number: division by zero: {p}/{q}")
        if p == 0:
            q = 1
        try:
            if type(p) is float:
                p = int(p)
            elif type(p) is not int:
                p = int(str(p))
            
            if type(q) is float:
                q = int(q)
            elif type(q) is not int:
                q = int(str(q))
        except ValueError:
            if q != 1:
                raise ValueError(f'Failed to create Rational: p is float and q is not 1: {p}/{q}')
            print("HERE, type:", type(p))
            ps = str(p)
            dot = ps.index('.')
            order = len(ps) - 1 - dot
            p = int(ps[:dot] + ps[dot + 1:])
            q = 10 ** order

        self.p, self.q = self._simplify(p, q)

        self.v = p / float(q)

    @classmethod
    def gcd(cls, a, b):
        a = abs(a)
        b = abs(b)
        while b != 0:
            t = b
            b = a % b
            a = t
        return a

    @classmethod
    def _simplify(cls, p, q):
        g = cls.gcd(p, q)
        
        return int(p / g), int(q / g)

    def __repr__(self):
        if self.q != 1:
            return f'{self.p}/{self.q}'
        else:
            return f'{self.p}'
    
    def __add__(self, o):
        if type(o) is Rational:
            if self.q != o.q:
                common_q = self.q * o.q
                left_p = self.p * o.q
                right_p = o.p * self.q
                return Rational(left_p + right_p, common_q)
            else:
                return Rational(self.p + o.p, self.q)
        elif type(o) is Complex:
            return Complex(self) + o
        else:
            raise NotImplementedError(f"Rational + {o} ({type(o)})")

    def __sub__(self, o):
        if type(o) is Rational:
            if self.q != o.q:
                common_q = self.q * o.q
                left_p = self.p * o.q
                right_p = o.p * self.q
                return Rational(left_p - right_p, common_q)
            else:
                return Rational(self.p - o.p, self.q)
        elif type(o) is Complex:
            return Complex(self) - o
        else:
            raise NotImplementedError()
    
    def __mul__(self, o):
        if type(o) is Rational:
            return Rational(self.p * o.p, self.q * o.q)
        elif type(o) is Complex:
            return Complex(self) * o
        else:
            raise NotImplementedError()

    def __div__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return self * Rational(o.q, o.p)
    
    def __truediv__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return self * Rational(o.q, o.p)
    
    def __pow__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return Rational(self.v ** o.v)
    
    def __mod__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return Rational(self.v % o.v)
    
    def __ge__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return self.v >= o.v

    def __abs__(self):
        return Rational(abs(self.p), abs(self.q))
    
    def __neg__(self):
        return Rational(-self.p, self.q)
    
    def __pos__(self):
        return Rational(self.p, self.q)


class Matrix(Term):
    def __init__(self, A):
        self.v = [[c for c in r] for r in A]

class Function(Term):
    def __init__(self, f):
        self.f = f


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            p = int(sys.argv[1])
        except ValueError:
            p = float(sys.argv[1])
        
        if len(sys.argv) > 2:
            try:
                q = int(sys.argv[2])
            except ValueError:
                q = float(sys.argv[2])
        else:
            q = 1
        r = Rational(p, q)
    else:
        r = Rational._simplify(5, 25)
    print(r)