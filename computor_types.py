import sys
from Term import *
from Rational import *


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
    available_operators = list('+-*/%^?') + ["**"]
    precedence_map = {'+': 2, '-': 2, '%': 2, '*': 3, '/': 3, '**': 3, '^': 4, '?': 4}

    def __init__(self, op):
        self.op = op
        if op not in self.available_operators:
            raise ValueError(f"Bad operator: {op}")
        self.n_operands = 1 if op in list('?~') else 2

        self.precedence = self.precedence_map[op]

    def __repr__(self):
        return self.op
    
    def __eq__(self, o):
        return str(self) == str(o)
    
    def eval(self, l, r=None):
        if self.n_operands == 1 and r is not None:
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