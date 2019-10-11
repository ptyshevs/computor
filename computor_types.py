import sys
from Term import *
from Rational import *
from Operator import *

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