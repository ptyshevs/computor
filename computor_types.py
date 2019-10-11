import sys
from Term import *
from Rational import *
from Operator import *
from Variable import *

class Complex(Term):
    def __init__(self, re, img=0):
        self.re = re
        self.img = img
    
    def __repr__(self):
        s = str(self.re)
        if s == '0':
            s = ''
        if self.img != 0:
            if s:
                s += '+' if self.img >= Rational(0) else '-'
            s += f'{abs(self.img)}i'
        return s

class Matrix(Term):
    def __init__(self, A):
        self.v = [[c for c in r] for r in A]

class Function(Term):
    def __init__(self, f):
        self.f = f
