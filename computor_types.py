import sys
from Term import *
from Operator import *
from Variable import *
import computorv2

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
        if type(o) is Complex:
            return Complex(self.re + o.re, self.img + o.img)
        elif type(o) is Rational:
            return Complex(self.re + o, self.img)
        else:
            raise NotImplementedError(f'Add {self} ({type(self)}) to {o} ({type(o)})')
    
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

    def __truediv__(self, o):
        print("Division starts here")
        if type(o) is Rational:
            o = Complex(o)
        if type(o) is Complex:
            a, b = self.re, self.img
            c, d = o.re, o.img
            
            denom = c * c + d * d
            return Complex((a * c + b * d) / denom, (b * c - a * d) / denom)
        else:
            raise NotImplementedError("Division of complex numbers")

    def __neg__(self):
        return Complex(-self.re, -self.img)
    
    def __pos__(self):
        return Complex(self.re, self.img)
    
    def conj(self):
        return Complex(self.re, -self.img)
    
    def norm(self):
        ss = (self.re ** Rational(2) + self.img ** Rational(2))
        return Rational(ss ** Rational(.5))

class Rational(Term):
    def __init__(self, p, q=1):
        if q == 0:
            raise ValueError(f"Failed to create rational number: division by zero: {p}/{q}")
        if p == 0:
            q = 1
        try:
            strp = str(p)
            if type(p) is float:
                if 'e' in strp:  # Very big integer
                    p = int(p)
                else:
                    p = int(strp)
            elif type(p) is not int:
                p = int(strp)
            if type(q) is float:
                q = int(q)
            elif type(q) is not int:
                q = int(str(q))
        except ValueError:
            if q != 1:
                raise ValueError(f'Failed to create Rational: p is float and q is not 1: {p}/{q}')
            ps = str(p)
            dot = ps.index('.')
            order = len(ps) - 1 - dot
            p = int(ps[:dot] + ps[dot + 1:])
            q = 10 ** order

        self.p, self.q = self._simplify(p, q)
        # Sign resolution
        p_sign = 1 if self.p >= 0 else -1
        q_sign = 1 if self.q >= 0 else -1
        if p_sign == -1 and q_sign == -1:
            p_sign, q_sign = 1, 1
        elif q_sign == -1:
            p_sign, q_sign = -1, 1

        self.p = p_sign * abs(self.p)
        self.q = q_sign * abs(self.q)

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
            raise NotImplementedError(f"{self} + {o} is not implemented")

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
            raise NotImplementedError(f'{self} - {o} is not implemented')
    
    def __mul__(self, o):
        if type(o) is Rational:
            return Rational(self.p * o.p, self.q * o.q)
        elif type(o) is Complex:
            return Complex(self) * o
        else:
            raise NotImplementedError(f'{self} * {o} is not implemented')
    
    def __truediv__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError(f'{self} / {o} is not implemented')
        return self * Rational(o.q, o.p)
    
    def __pow__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError(f"{self} ^ {o} is not implemented")
        return Rational(self.v ** o.v)
    
    def __mod__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError(f'{self} % {o} is not implemented')
        return Rational(self.v % o.v)
    
    def __ge__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError(f'{self} >= {o} is not implemented')
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
        self.n_rows = len(self.v)
        self.n_cols = len(self.v[0]) if len(self.v) > 0 else 0
        self.shape = (self.n_rows, self.n_cols)
    
    def __repr__(self):
        return '\n'.join((str(_) for _ in self.v))
    
    def __add__(self, o):
        if type(o) is Matrix:
            self._validate_shape(o, 'add')
            return Matrix([[cl + cr for cl, cr in zip(rl, rr)] for rl, rr in zip(self.v, o.v)])
        else:
            raise NotImplementedError()
    
    def __sub__(self, o):
        if type(o) is Matrix:
            self._validate_shape(o, 'sub')
            return Matrix([[cl - cr for cl, cr in zip(rl, rr)] for rl, rr in zip(self.v, o.v)])
        else:
            raise NotImplementedError()
    
    def __mul__(self, o):
        if type(o) is Matrix:
            self._validate_shape(o, 'mul')
            return Matrix([[cl * cr for cl, cr in zip(rl, rr)] for rl, rr in zip(self.v, o.v)])
        elif type(o) in [Rational, Complex]:
            return Matrix([[c * o for c in r] for r in self.v])
        else:
            raise NotImplementedError()
    
    def __truediv__(self, o):
        if type(o) is Matrix:
            self._validate_shape(o, 'div')
            return Matrix([[cl / cr for cl, cr in zip(rl, rr)] for rl, rr in zip(self.v, o.v)])
        elif type(o) in [Rational, Complex]:
            return Matrix([[c / o for c in r] for r in self.v])
        else:
            raise NotImplementedError()
    
    def __neg__(self):
        return Matrix([[-c for c in r] for r in self.v])
    
    def __pos__(self):
        return Matrix([[+c for c in r] for r in self.v])
    
    def __abs__(self):
        return Matrix([[abs(c) for c in r] for r in self.v])
    
    def _validate_shape(self, o, op):
        if self.shape != o.shape:
            raise ValueError(f"Dimensions mismatch ({op}): {self.shape} != {o.shape}")

class Function(Term):
    def __init__(self, name, arg_name, body, env, f=None):
        self.name = name
        self.arg_name = arg_name
        self.f = f
        self.body = body
        self.sub_body = ' '.join((c if c != arg_name else f'%_{arg_name}_%' for c in body))
        self.env = env

    def apply(self, o):
        if type(o) is Variable:
            o = o.dereference()
        if self.f is not None:
            if type(o) is Rational:
                return Rational(self.f(o.v))
            else:
                raise NotImplementedError(f"{self.name}({self.arg_name}) is not implemented for {o}")
        res = computorv2.evaluate(' '.join((c if c != self.arg_name else str(o) for c in self.body)), self.env)
        print(f"applying {self.name}({self.arg_name}) on {o}: {res}")
        return res
    
    def __repr__(self):
        return f'{self.name}({self.arg_name})={self.body}'
    
    def __str__(self):
        return f'{self.name}'


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