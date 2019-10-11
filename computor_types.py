import sys

class Term:
    def __init__(self):
        pass

class Rational(Term):
    def __init__(self, p, q=1):
        if q == 0:
            raise ValueError(f"Failed to create rational number: division by zero: {p}/{q}")
        if p == 0:
            q = 1
        try:
            p = int(str(p))
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
        else:
            raise NotImplementedError()

    def __sub__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()

        if self.q != o.q:
            common_q = self.q * o.q
            left_p = self.p * o.q
            right_p = o.p * self.q
            return Rational(left_p - right_p, common_q)
        else:
            return Rational(self.p - o.p, self.q)
    
    def __mul__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return Rational(self.p * o.p, self.q * o.q)

    def __div__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return self * Rational(o.q, o.p)
    
    def __truediv__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return self * Rational(o.q, o.p)

class Complex(Term):
    def __init__(self, re, img=0):
        self.re = re
        self.img = img
    
    def __repr__(self):
        s = str(self.re)
        if self.img != 0:
            s += f'+{self.img}i'
        return s

class Matrix(Term):
    def __init__(self, A):
        self.v = [[c for c in r] for r in A]

class Function(Term):
    def __init__(self, f):
        self.f = f

class Operator(Term):
    def __init__(self, op):
        self.op = op
        self.available_operators = '+-*/%^?'.split() + ["**"]
        self.n_operands = 2 if op in self.available_operators else 1
    
    def __repr__(self):
        return self.op
    
    def __eq__(self, o):
        return str(self) == str(o)
    
    def eval(self, l, r=None):
        if self.n_operands == 2 and r is not None:
            raise ValueError("{self} doesn't support second operator")
        if self.op == '+':
            return l + r
        elif self.op == '-':
            return l - r
        elif self.op == '*':
            return l * r
        elif self.op == '/':
            return l / r
        elif self.op == '%':
            return l % r
        elif self.op == '^':
            return l ** r
        elif self.op == '**':
            return l @ r
        elif self.op == '?':
            return l
        elif self.op == '~':  # TODO: Maybe implement this one
            return -l

class Variable(Term):
    def __init__(self, name, v=None):
        self.name = name
        self.v = v
    
    def assign(self, v):
        self.v = v
    
    def __repr__(self):
        s = str(self.name)
        if self.v:
            s += f'={self.v}'
        return s
    
    def __eq__(self, o):
        if type(o) is Variable:
            return str(self.name) == str(o.name)
        else:
            return str(self) == str(o)

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