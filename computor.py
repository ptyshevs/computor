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
    
    def __str__(self):
        return self.__repr__()

def interpret_match(match):
    n = list(match)
    if n[3]:
        return n[3]
    n[0] = float(n[0])
    if not n[1] and n[2]:
        raise ValueError(f"Invalid term: {match[0]}{match[1]}^{match[2]}")
    if not n[2]:
        n[2] = 1
    if not n[1]:
        n[1] = 'x'
        n[2] = 0
    n[2] = float(n[2])

    return Term(coef=n[0], name=n[1], order=n[2])

def is_op(token):
    return token in ['+', '-']

def is_term(token):
    return type(token) is Term

def apply_sign(operator, term):
    sign = 1 if operator == '+' else -1
    term.coef *= sign

def simplify_operators(eq):
    i = 0
    simplified = []
    cnt_equal_sign = 0
    while True:

        if i == len(eq):
            break

        cur_term = eq[i]
        cur_operator = is_op(cur_term)
        if type(cur_term) is str and cur_term == '=':
            cnt_equal_sign += 1
            if cnt_equal_sign > 1:
                raise ValueError("More equal signs than necessary")
        if is_op(cur_term):
            left_op = eq[i - 1] if i > 0 else None
            right_op = eq[i + 1] if i < (len(eq) - 1) else None
            left_operator = is_op(left_op)
            right_operator = is_op(right_op)

            if (left_operator and right_operator) or right_op is None:
                raise ValueError("Parsing error: operators are invalid")

            if cur_operator and (type(left_op) in [None, str]) and type(right_op) is Term:
                apply_sign(cur_operator, right_op)

            if is_term(left_op) and is_term(right_op):
                if cur_term == '-':
                    apply_sign(cur_term, right_op)
                    simplified.append("+")
                else:
                    simplified.append(cur_term)

            if cur_operator and right_operator:
                raise ValueError("Too many operators")

        else:
            simplified.append(cur_term)
        i += 1
    return simplified

def combine_same_orders(eq):
    left = []
    left_side = True
    for term in eq:
        if type(term) is str and term == '=':
            left_side = False
            continue
        if type(term) is Term:
            found = False
            for left_term in left:
                if left_term.order == term.order:
                    sign = 1 if left_side else -1
                    left_term.coef += sign * term.coef
                    found = True
                    break
            if not found:
                left.append(term)
    return sorted(left, key=lambda x: x.order, reverse=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('equation')
    args = parser.parse_args()

    inp = args.equation
    print("input:", inp)
    reformat = ''.join((c.lower() for c in inp.split(" ") if c))
    print("correct format:", reformat)
    reg = r'([0-9]+\.?[0-9]*)\*?([a-zA-Z]*)\^?([0-9]*)|([-=+])'
    matched_terms = re.findall(reg, reformat)
    # print("Matches:", matched_terms)
    eq = []
    for match in matched_terms:
        term = interpret_match(match)
        eq.append(term)
    
    print("Before simplification:", ' '.join([str(_) for _ in eq]))
    simplified = simplify_operators(eq)
    print("After simplification:", ' '.join([str(_) for _ in simplified]))
    left_side = combine_same_orders(simplified)
    print("Combined sides:", ' '.join([str(_) for _ in left_side]), "= 0")
