import argparse
import re
from computor_types import *

def str_to_num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def match_token(token, env):
    """ use re.fullmatch to map token to object """
    number_re = r'[\-\+]?[0-9]+\.?[0-9]*'
    operator_re = r'(\*\*)|([\=\+\-\*\/\^\%\?])'
    brackets_re = r'[\(\)]'
    complex_re = r'([\-\+]?[0-9]*)([\+\-]?[0-9]*)i'
    var_re = r'[a-zA-Z]+'
    # 1. Operator
    mo = re.fullmatch(operator_re, token)
    if mo:
        return Operator(mo[0])
    # 1.2 Brackets
    mo = re.fullmatch(brackets_re, token)
    if mo:
        return mo[0]
    # 2. Rational number
    mo = re.fullmatch(number_re, token)
    if mo:
        number = str_to_num(mo[0])
        return Rational(number)
    # 2.2 Complex number
    mo = re.fullmatch(complex_re, token)
    if mo:
        print(mo, mo.groups())
        real, img = mo[1], mo[2]
        if not img:
            real = 0
            img = mo[1]
        return Complex(Rational(real), Rational(img))
    # 3. Variable
    mo = re.fullmatch(var_re, token)
    if mo:
        name = mo[0]
        if name.lower() == 'i':
            print("Variable cannot be called i (for obvious reasons)")
            return None
        else:
            var = Variable(name)
            for t in env:
                if var == t:
                    return t
            return var

def eval_expression(expr, env):
    """ Expression is expected to simplify to a single term """
    accum = None
    expect_operator = False
    n = len(expr)
    for i in range(n):
        t = expr[i]
        if type(t) is Variable:
            found = False
            for v in env:
                if t == v:
                    print(f"Var {t} exists in env")
                    t = v
                    found = True
                    break
            if t.v is None:
                raise ValueError(f"Variable {t} doesn't have value associated with it")
            else:
                t = t.v
        
        if type(t) is Operator:
            if accum is None:
                left = expr[i - 1] if i > 0 else None
                if left is None:
                    left = accum
                if type(left) is Variable:
                    left = left.v
            else:
                left = accum
            right = expr[i + 1] if i < (n - 1) else None
            if type(right) is Variable:
                right = right.v
            print(f"left={left}|right={right}|op={t}")
            if t.n_operands == 2 and (left is None or right is None):
                raise ValueError(f"Invalid expression: {expr} (Operator doesn't have enough operands)")
            elif t.n_operands == 1 and left is None:
                raise ValueError(f"Invalid expression: {expr} (Operator doesn't have enough operands)")
            else:
                accum = t.eval(left, right)
                expect_operator = False
        else:
            if accum is None:
                accum = t
                expect_operator = True
            elif expect_operator:
                raise ValueError(f'Invalid expression: {expr}. Expected operator, found term {t} at {i} place instead')
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
    print("Right side:", right_side)
    var = left[0]
    found = False
    for thing in env:
        if thing == var:
            thing.assign(right_side)
            found = True
            print("Found, assigned to it")
            break
    if not found:
        var.assign(right_side)
        print("var now:", var)
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

def infix_to_rpn(expr):
    operators = []  # Stack
    output = []  # Queue
    while expr:
        tk = expr.pop(0)
        if type(tk) in [Rational, Complex, Variable]:  # TODO: Add complex and matrix here
            output.append(tk)
        elif type(tk) is Function:
            operators.append(tk)
        elif type(tk) is Operator:
            while True:
                if len(operators) == 0:
                    break
                head = operators[-1]
                if head == '(':
                    break
                if type(head) is Function:
                    output.append(operators.pop())
                elif type(head) is Operator and head.precedence > tk.precedence:
                    output.append(operators.pop())
                elif type(head) is Operator and head.precedence == tk.precedence and head.associativity == 'left':
                    output.append(operators.pop())
                else:
                    break
            operators.append(tk)
        elif tk == '(':
            operators.append(tk)
        elif tk == ')':
            found_bracket = False
            while True:
                if len(operators) == 0:
                    break
                head = operators[-1]
                if head == '(':
                    found_bracket = True
                    break
                output.append(operators.pop())
            if not found_bracket:
                raise ValueError("Mismatched parentheses")
            assert operators[-1] == '('
            operators.pop()
    while operators:
        op = operators.pop()
        if op in ['(', ')']:
            raise ValueError("Mismatched parentheses")
        output.append(op)
    return output

def evaluate_rpn(rpn, env):
    eval_stack = []
    while rpn:
        val = rpn.pop(0)
        if type(val) is Variable:
            found = False
            for t in env:
                if val == t:
                    val = t
                    found = True
                    break
            if not found and val.v is not None:
                env.append(val)
        if type(val) in [Rational, Complex, Variable]:
            eval_stack.append(val)
        elif type(val) is Operator:
            n_op = val.n_operands
            if not eval_stack:
                raise ValueError(f"Not enough operands to perform calculation | operator {val}")
            op = eval_stack.pop()
            if n_op == 1:
                eval_stack.append(val.eval(op))
            else:
                if not eval_stack:
                    if val in ['+', '-']:
                        print(f"Unary {val}")
                        eval_stack.append(val.eval(op))
                    else:
                        raise ValueError(f"Not enough operands to perform calculation | operator {val}, op1 {op}")
                else:
                    op2 = eval_stack.pop()
                    print(f"OP={op}|OP2={op2}")
                    if val != '=':
                        if type(op) is Variable:
                            if op.v is None:
                                raise ValueError(f"Unassigned variable {op}")
                            op = op.v
                        if type(op2) is Variable:
                            if op2.v is None:
                                raise ValueError(f"Unassigned variable {op2}")
                            op2 = op2.v
                    else:
                        if type(op) is Variable:
                            op = op.v
                        if op2 not in env:
                            env.append(op2)
                    eval_stack.append(val.eval(op, op2))
        elif type(val) is Function:
            if not eval_stack:
                raise ValueError(f"Not enough operands to perform calculation | operator {val}")
            eval_stack.append(val.eval(eval_stack.pop()))
        else:
            raise NotImplementedError(val, type(val))
    if len(eval_stack) != 1:
        raise ValueError("Expression doesn't evaluate to a single value")
    print("EVAL STACK:", eval_stack)
    res = eval_stack[0]
    if type(res) is Variable:
        return res.v
    return res

def expand_tokens(tokens):
    split_re = r'([\*\^\/\(\)\-\+\%\=\?])'
    exp = []
    for tk in tokens:
        expanded = [c for c in re.split(split_re, tk) if c]
        n = len(expanded)
        accum = None
        for i in range(n):
            t = expanded[i]
            if accum is None:
                accum = t
            else:
                accum += t
            if t in list('+-'):
                prev = expanded[i-1] if i > 0 else None
                if prev and prev in '0123456789':
                    exp.append(accum)
                    accum = None
            else:
                exp.append(accum)
                accum = None
        if accum is not None:
            exp.append(accum)
    return exp

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
            continue
        elif line_args['env']:
            show_env(env)
            continue

        tokens = [c for c in inp.split(" ") if c]
        print("Tokens:", tokens)
        # Convert tokens to expression. One token can actually contain many statements that need to be separated: "-x^2+3x"
        exp_tokens = expand_tokens(tokens)
        print("Expanded tokens:", exp_tokens)
        success = True
        expr = []
        for tk in exp_tokens:
            obj = match_token(tk, env)
            if obj is None:
                print(f"Unrecognized token: {tk}")
                success = False
                break
            expr.append(obj)
        if not success:
            continue

        print("Input:", inp, "|Expression:", expr)
        # At this point all tokens are interpreted and expanded, so we can
        # proceed with preparing it into form that is suitable for calculation
        rpn = infix_to_rpn(expr)
        print("RPN:", rpn)
        try:
            result = evaluate_rpn(rpn, env)
            print("Result:", result)
        except ValueError as e:
            print(e)
