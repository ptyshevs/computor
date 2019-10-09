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
    if n[5]:  # Operator
        return n[5]
    if not n[0]:
        return Term(coef=float(n[4]), order=0)
    n = n[1:]
    n[0] = float(n[0]) if n[0] else 1
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
            solved = False
    
            left_op = eq[i - 1] if i > 0 else None
            right_op = eq[i + 1] if i < (len(eq) - 1) else None
            left_operator = is_op(left_op)
            right_operator = is_op(right_op)

            if (left_operator and right_operator) or right_op is None:
                raise ValueError("Parsing error: operators are invalid")

            if cur_operator and (type(left_op) in [None, str]) and type(right_op) is Term:
                apply_sign(cur_operator, right_op)
                solved = True

            if is_term(left_op) and is_term(right_op):
                if cur_term == '-':
                    apply_sign(cur_term, right_op)
                    simplified.append("+")
                else:
                    simplified.append(cur_term)
                solved = True

            if not solved and cur_operator and left_operator:
                print(cur_term)
                raise ValueError("Too many operators")

        else:
            simplified.append(cur_term)
        i += 1
    return simplified

def equation_to_string(eq, add_right_side=True):
    s =  ' + '.join((str(_) for _ in eq))
    if add_right_side:
        s += ' = 0'
    return s

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

def solve_equation(eq):
    """
    For now, equation is in correct form
    """
    order = eq[0].order
    if order == 0:
        if eq[0].coef == 0:
            return "all real values"
        else:
            return "no solution"
    elif order == 1:
        if len(eq) == 2:
            solution = -eq[1].coef / eq[0].coef
            return solution
        else:
            return 0

    elif order == 2:
        n_coefs = len(eq)
        a = eq[0].coef
        if n_coefs >= 2:
            b = eq[1].coef
        else:
            b = 0
        if n_coefs == 3:
            c = eq[2].coef
        else:
            c = 0
        
        d = b ** 2 - 4 * a * c
        print("Discriminant:", d)
        if d > 0:
            print("Two distinct real solutions")
        elif d == 0:
            print("Two same real solutions")
        else:
            print("No real solutions :(")
        x1 = (-b - d ** .5) / (2 * a)
        x2 = (-b + d ** .5) / (2 * a)
        return x1, x2
    else:
        raise ValueError(f"Polynomials of degree {order} are not supported")
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('equation')
    args = parser.parse_args()

    inp = args.equation
    print("input:", inp)
    reformat = ''.join((c.lower() for c in inp.split(" ") if c))
    print("correct format:", reformat)
    reg = r'(([0-9]*\.?[0-9]*)\*?([a-zA-Z]+)\^?([0-9]*))|([0-9]+\.?[0-9]*)|([-=+])'
    matched_terms = re.findall(reg, reformat)
    print("Matches:", matched_terms)
    eq = []
    for match in matched_terms:
        term = interpret_match(match)
        eq.append(term)
    
    print("Before simplification:", ' '.join([str(_) for _ in eq]))
    simplified = simplify_operators(eq)
    print("After simplification:", ' '.join([str(_) for _ in simplified]))
    left_side = combine_same_orders(simplified)
    print("Combined sides:", ' '.join([str(_) for _ in left_side]), "= 0")
    if len(left_side) == 0 or len(left_side) > 3 or left_side[0].order > 2:
        raise ValueError(f"Polynomials of degree > {len(left_side)} are not supported: {equation_to_string(left_side)}")
    solution = solve_equation(left_side)
    print(f"{equation_to_string(left_side)}")
    print(f"Solution: {solution}")
