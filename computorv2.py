import argparse
import re

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

def match_token(token):
    """ use re.fullmatch to map token to object """
    found = False

    number_re = r'[0-9]+\.?[0-9]*'
    operator_re = r'[=+-*/^%]'

    # 1. Operator
    mo = re.fullmatch(operator_re, tk)
    if mo:
        expr.append(Operator(mo[0]))
    # 2. Rational number
    mo = re.fullmatch(number_re, tk)
    if mo:
        number = mo[0]
        expr.append(Rational(number))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--quiet', '-q', help="Quite mode: display output only when asked for", default=False, action='store_true')

    args = parser.parse_args()

    env = []
    while True:
        inp = input("> ")
        
        if inp == 'q' or inp == '--quit':
            break

        tokens = [c for c in inp.split(" ") if c]
        print(tokens)
        # Convert tokens to expression. One token can actually contain many statements that need to be separated: "-x^2+3x"
        
        expr = []
        for tk in tokens:
            obj = match_token(tk)
            expr.append(obj)

        print(inp)