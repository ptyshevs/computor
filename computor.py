import sys
import argparse
import re
import random

class Term:
    def __init__(self, name='', order=1, coef=1):
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

    i = len(eq) - 1
    simplified = []
    cnt_equals = 0
    while i >= 0:

        cur = eq[i]
        if cur == '=':
            cnt_equals += 1
            if cnt_equals > 1:
                raise ValueError("Too many equal signs")
        left = eq[i - 1] if i > 0 else None
        right = eq[i + 1] if i < len(eq) - 1 else None
        if is_op(cur):
            if is_op(left) or left is None:
                if is_term(right):
                    apply_sign(cur, right)
                    eq.pop(i)
                else:
                    raise ValueError("Invalid equation")
            else:
                if cur == '-':
                    apply_sign(cur, right)
                    cur = '+'
                simplified.insert(0, cur)
        else:
            simplified.insert(0, cur)
        i -= 1
    return simplified

def equation_to_string(eq, add_right_side=True):
    s =  ' + '.join((str(_) for _ in eq))
    if add_right_side:
        s += ' = 0'
    return s

def combine_same_orders(eq):
    combined = []
    left_side = True
    for term in eq:
        if type(term) is str and term == '=':
            left_side = False
            continue
        if type(term) is Term:
            found = False
            for left_term in combined:
                if left_term.order == term.order:
                    sign = 1 if left_side else -1
                    left_term.coef += sign * term.coef
                    found = True
                    break
            if not found:
                sign = 1 if left_side else -1
                term.coef *= sign
                combined.append(term)
    
    non_zero = [term for term in combined if term.coef != 0]
    return sorted(non_zero, key=lambda x: x.order, reverse=True)

def solve_equation(eq):
    """
    For now, equation is in correct form
    """
    order = eq[0].order
    if eq[0].coef == 0:
        return "all real values"
    print(f"{int(order)}-degree polynomial")
    if order == 0:
        return "no solution"  # a != 0, equation of form a = 0
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
    
def check_variables(eq):
    name = None
    for term in eq:
        if type(term) is not Term:
            continue
        if name is None and term.name:
            name = term.name
        if term.name and name != term.name:
            raise ValueError(f"Equation of several variables detected. {name} != {term.name}")

def check_tokens(tokens, regex):
    for tk in tokens:
        res = re.findall(regex, tk)
        if len(res) == 0:
            raise ValueError(f"Invalid token {tk} | {res}")
        print(res)
        v = ''.join([''.join(_[0] if _[0] else _[4:]) for _ in res])
        print(v)
        if v != tk:
            raise ValueError(f"Invalid token: {tk} != {v}")


def check_operators(eq):
    left_side = True
    term_expected = True
    for t in eq:
        if type(t) is Term and term_expected:
            term_expected = False
        elif type(t) is str and not term_expected:
            term_expected = True
        elif type(t) is str and left_side:
            left_side = False
        else:
            raise ValueError("Invalid equation")
    if is_op(eq[-1]) or is_op(eq[0]):
        raise ValueError("Equation should not start and\or end with operator")
        

jokes = ["Q: Why was the student afraid of the y-intercept?\nA: She thought she'd be stung by the b.",
        "Q: Who invented algebra?\nA: A Clever X-pert.",
        "Q: What do you call friends who love math?\nA: algebros",
        "Q: Why wont Goldilocks drink a glass of water with 8 pieces of ice in it?\nA: It's too cubed.",
        "Q: Why is an algebra book always unhappy? A: Because it always has lots of problems.",
        "Q: Why do you rarely find mathematicians spending time at the beach? A: Because they have sine and cosine to get a tan and don't need the sun!"]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('equation')
    parser.add_argument("--joke", '-j', default=False, action='store_true')
    parser.add_argument('--verbose', '-v', default=False, action='store_true')
    args = parser.parse_args()

    if args.joke:
        print(random.choice(jokes))
        exit(0)
    reg = r'(([[0-9]*\.?[0-9]*)\*?([a-zA-Z])\^?([0-9]*))|([0-9]+\.?[0-9]*)|([-=*+])'

    inp = args.equation
    print("input:", inp)
    tokens = [c.lower() for c in inp.split(" ") if c]
    check_tokens(tokens, reg)
    reformat = ''.join(tokens)
    print("correct format:", reformat)
    matched_terms = re.findall(reg, reformat)
    print("Matches:", matched_terms)
    eq = []
    for match in matched_terms:
        term = interpret_match(match)
        eq.append(term)
    
    if args.verbose:
        print("Before simplification:", ' '.join([str(_) for _ in eq]))
    simplified = simplify_operators(eq)
    if args.verbose:
        print("After simplification:", ' '.join([str(_) for _ in simplified]))
    check_variables(simplified)
    check_operators(simplified)
    combined = combine_same_orders(simplified)
    if len(combined) == 0:
        print(f"Solution(s): all real variables")
    else:
        if args.verbose:
            print("Combined sides:", ' '.join([str(_) for _ in combined]), "= 0")
        print(f"Reduced form: {equation_to_string(combined)}")
        if len(combined) == 0 or len(combined) > 3 or combined[0].order > 2:
            raise ValueError(f"Polynomials of degree > {len(combined)} are not supported: {equation_to_string(combined)}")
        solution = solve_equation(combined)
        print(f"Solution(s): {solution}")
