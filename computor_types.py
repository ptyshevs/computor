
class Term:
    def __init__(self):
        pass

class Rational(Term):
    def __init__(self, p, q=1):
        self.p = p
        self.q = q
        if q == 0:
            raise ValueError("Divizion by zero when creating rational number")
        self.v = p / q
    
    def __repr__(self):
        if self.q != 1:
            return f'{self.p}/{self.q}'
        else:
            return f'{self.p}'

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
            s += f'{self.v}'
        return s
    
    def __eq__(self, o):
        if type(o) is Variable:
            return str(self.name) == str(o.name)
        else:
            return str(self) == str(o)
