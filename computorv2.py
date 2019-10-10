import argparse
import re
from computor_types import *

def str_to_num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def match_token(token):
    """ use re.fullmatch to map token to object """
    number_re = r'[-]?[0-9]+\.?[0-9]*'
    operator_re = r'(\*\*)|([\=\+\-\*\/\^\%\?])'
    var_re = r'[a-zA-Z]+'
    # 1. Operator
    mo = re.fullmatch(operator_re, token)
    if mo:
        return Operator(mo[0])
    # 2. Rational number
    mo = re.fullmatch(number_re, token)
    if mo:
        number = str_to_num(mo[0])
        return Rational(number)
    # 3. Variable
    mo = re.fullmatch(var_re, token)
    if mo:
        name = mo[0]
        if name.lower() == 'i':
            print("Variable cannot be called i (for obvious reasons)")
            return None
        else:
            var = Variable(name)
            return var

def eval_expression(expr, env):
    """ Expression is expected to simplify to a single term """
    accum = None
    expect_operator = False
    n = len(expr)
    for i in range(n):
        t = expr[i]
        if type(t) is Variable:
            if t in env:
                print(f"Var {t} exists in env")
                t = t.v
            elif t.v is None:
                raise ValueError(f"Variable {t} doesn't have value associated with it")
        
        elif type(t) is Operator:
            left = expr[i - 1] if i > 0 else None
            if left is None:
                left = accum
            right = expr[i + 1] if i < (n - 1) else None
            
            if t.n_operands == 2 and (left is None or right is None):
                raise ValueError(f"Invalid expression: {expr} (Operator doesn't have enough operands)")
            elif t.n_operands == 1 and left is None:
                raise ValueError(f"Invalid expression: {expr} (Operator doesn't have enough operands)")
            else:
                accum = t.eval(left, right)
        else:
            if accum is None:
                accum = t
                expect_operator = True
            elif expect_operator:
                raise ValueError(f'Invalid expression: {expr}. Expected operator, found term instead')
            else:
                expect_operator = True
    return accum


def eval_statement(expr, env):
    left = []
    right = []
    left_side = True
    cnt_equals = 0
    for t in expr:
        if t == '=':
            left_side = False
            cnt_equals += 1
            if cnt_equals > 1:
                return "Too many assignment values"
        else:
            if left_side:
                left.append(t)
            else:
                right.append(t)
    if len(left) != 1 or type(left[0]) is not Variable:
        return "Left side of assignment should be variable"
    if len(right) == 0:
        return "Right side of assignment cannot be empty"

    right_side = eval_expression(right, env)
    var = left[0]
    found = False
    for thing in env:
        if thing == var:
            thing.assign(right_side)
            found = True
            break
    if not found:
        var.assign(right_side)
        env.append(var)
    return right_side

def parse_keywords(inp):
    cli_args = {'quit': False, 'history': False, 'env': False}
    if inp in ['q', '--quit']:
        cli_args['quit'] = True
    elif inp == 'env':
        cli_args['env'] = True
    elif inp == 'history':
        cli_args['history'] = True
    return cli_args

def show_history(history):
    print(history)  # TODO: Pretty formatting

def show_env(env):
    print(env)  # Todo: Pretty formatting

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--quiet', '-q', help="Quite mode: display output only when asked for", default=False, action='store_true')

    args = parser.parse_args()

    env = []
    history = []
    running = True
    while True:
        inp = input("> ")
        
        line_args = parse_keywords(inp)
        if line_args['quit']:
            break
        elif line_args['history']:
            show_history(history)
        elif line_args['env']:
            show_env(env)

        tokens = [c for c in inp.split(" ") if c]
        # print(tokens)
        # Convert tokens to expression. One token can actually contain many statements that need to be separated: "-x^2+3x"
        
        expr = []
        for tk in tokens:
            obj = match_token(tk)
            expr.append(obj)

        print("Input:", inp, "|Expression:", expr)
        # Expression can either be an assignment statement or expression evaluation
        if '=' in expr:
            res = eval_statement(expr, env)
            print(res)
        else:
            print(eval_expression(expr, env))