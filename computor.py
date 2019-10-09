import sys
import argparse
import re

class Term:
    def __init__(self, name='x', order=1, coef=1):
        self.name = name
        self.order = order
        self.coef = coef
    
    def __repr__(self):
        s = f'{self.coef}'
        if self.order != 0:
            s += f'{self.name}^{self.order}'
        return s

def interpret_match(match):
    n = list(match)
    n[0] = float(n[0])
    if not n[2]:
        n[2] = 1
    if not n[1]:
        n[1] = 'x'
        n[2] = 0
    n[2] = float(n[2])

    return Term(coef=n[0], name=n[1], order=n[2])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('equation')
    args = parser.parse_args()

    inp = args.equation
    print("input:", inp)
    reformat = ''.join((c.lower() for c in inp.split(" ") if c))
    print("correct format:", reformat)
    reg = r'([0-9]+\.?[0-9]*)\*?([a-zA-Z]*)\^?([0-9]*)'
    matched_terms = re.findall(reg, reformat)
    for match in matched_terms:
        term = interpret_match(match)
        print(term)