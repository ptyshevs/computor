import argparse
import re
import computor_types as ct
from math import sin, cos, tan, tanh

def str_to_num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def squeeze(mat_row):
    if len(mat_row) < 2 or mat_row[0] != '[':
        return mat_row
    cnt_open = 1
    i = 1
    n = len(mat_row)
    while i < n:
        if cnt_open == 0:
            break
        t = mat_row[i]
        if t == '[':
            cnt_open += 1
        elif t == ']':
            cnt_open -= 1
        i += 1
    print(f"Squeeze attempt: i={i} | cnt_open={cnt_open} | n={n}")
    if cnt_open == 0 and i == n:
        return mat_row[1:-1]
    else:
        return mat_row

def row_split(row, char=','):
    """ Split row by comma, but only on the zero level """
    depth = 0
    elems = []
    accum = None
    for c in row:
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
        elif c == char and depth == 0:
            elems.append(accum)
            accum = None
            continue
        if accum is None:
            accum = c
        else:
            accum += c
    if accum is not None:
        elems.append(accum)
    return elems

def parse_matrix(tk, env=None, return_matrix=True):
    """ Starts and ends with [] brackets, potential ct.Matrix """
    if env is None:
        env = []
    tk = tk[1:-1]  # Strip leading and trailing brackets
    rows = row_split(tk, ';')
    if len(rows) == 1:
        v = rows[0]
        v_squeezed = squeeze(v)
        n_squizzes = 0
        while v_squeezed != v:
            n_squizzes += 1
            v = v_squeezed
            v_squeezed = squeeze(v)
        # print("Vector", v, "Squizzes:", n_squizzes)
        vec_elems = row_split(v, ',')
        expr = [evaluate(elem, env) for elem in vec_elems]
        if any((e is None for e in expr)):
            return None
        if return_matrix:
            return ct.Matrix([expr])
        else:
            return expr

    else:
        # ct.Matrix, validate that each rows starts and ends with proper brackets
        valid = True
        for r in rows:
            if len(r) < 2:
                valid = False
                break
            elif r[0] != '[' or r[-1] != ']':
                valid = False
                break
        if not valid:
            print("Invalid ct.Matrix format")
            return None
        else:
            print("Valid multi-row ct.Matrix")
            matrix_rows = []
            row_len = None
            for r in rows:
                res = parse_matrix(r, env=env, return_matrix=False)
                if res is None or len(res) == 0:
                    raise ValueError(f"Invalid ct.Matrix row: {r}")
                if row_len is None:
                    row_len = len(res)
                elif len(res) != row_len:
                    raise ValueError(f'Attempted to create matrix of different column length: {len(res)} != {row_len}')
                matrix_rows.append(res)
            print("ct.Matrix rows:", matrix_rows)
            return ct.Matrix(matrix_rows)
        


def match_token(token, env=None):
    """ use re.fullmatch to map token to object """
    number_re = r'[\-\+]?[0-9]+\.?[0-9]*'
    operator_re = r'(\*\*)|([\=\+\-\*\/\^\%\?])'
    brackets_re = r'[\(\)]'
    complex_re = r'([\-\+]?[0-9]*)([\+\-]?[0-9]*)i'
    matrix_re = r'\[.*\]'
    var_re = r'[a-zA-Z]+'

    if env is None:
        env = []
    # 1. ct.Operator
    mo = re.fullmatch(operator_re, token)
    if mo:
        return ct.Operator(mo[0])
    # 1.2 Brackets
    mo = re.fullmatch(brackets_re, token)
    if mo:
        return mo[0]
    # 2. ct.Rational number
    mo = re.fullmatch(number_re, token)
    if mo:
        number = str_to_num(mo[0])
        return ct.Rational(number)
    # 2.2 ct.Complex number
    mo = re.fullmatch(complex_re, token)
    if mo:
        real, img = mo[1], mo[2]
        if not img:
            real = 0
            img = mo[1]
        if not img:  # i
            img = 1
        return ct.Complex(ct.Rational(real), ct.Rational(img))
    # 3. ct.Variable
    mo = re.fullmatch(var_re, token)
    if mo:
        name = mo[0]
        if name.lower() == 'i':
            print("ct.Variable cannot be called i (for obvious reasons)")
            return None
        else:
            var = ct.Variable(name)
            for t in env:
                if var.name == t.name:
                    return t
            return var
    # 4. ct.Matrix
    mo = re.fullmatch(matrix_re, token)
    if mo:
        mat_repr = mo[0]
        mat = parse_matrix(mat_repr, env)
        print("ct.Matrix REPR:", mat_repr)
        print("ct.Matrix:", mat)
        if mat:
            return mat



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
    print(', '.join(f'({type(v)}) {v}' for v in env))  # Todo: Pretty formatting

def infix_to_rpn(expr):
    operators = []  # Stack
    output = []  # Queue
    print("INFIX TO RPN")
    while expr:
        tk = expr.pop(0)
        print(f'tk={tk}, type={type(tk)}')
        if type(tk) in [ct.Rational, ct.Complex, ct.Variable, ct.Matrix]:
            output.append(tk)
        elif type(tk) is ct.Function:
            print(f"Added {tk} as a func")
            operators.append(tk)
        elif type(tk) is ct.Operator:
            while True:
                if len(operators) == 0:
                    break
                head = operators[-1]
                if head == '(':
                    break
                if type(head) is ct.Function:
                    output.append(operators.pop())
                elif type(head) is ct.Operator and head.precedence > tk.precedence:
                    output.append(operators.pop())
                elif type(head) is ct.Operator and head.precedence == tk.precedence and head.associativity == 'left':
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
        if type(val) is ct.Variable:
            found = False
            for t in env:
                if val == t:
                    if type(t) is ct.Function:
                        env.remove(t)
                        found = False
                    if type(t) is ct.Variable:
                        val = t
                        found = True
                    break
            if not found and val.v is not None:
                env.append(val)
        if type(val) in [ct.Rational, ct.Complex, ct.Variable, ct.Matrix]:
            eval_stack.append(val)
        elif type(val) is ct.Operator:
            n_op = val.n_operands
            if not eval_stack:
                raise ValueError(f"Not enough operands to perform calculation | ct.Operator {val} ({type(val)})")
            op = eval_stack.pop()
            if n_op == 1:
                eval_stack.append(val.eval(op))
            else:
                if not eval_stack:
                    if val in ['+', '-']:
                        # print(f"Unary {val}")
                        if type(op) is ct.Variable:
                            op = op.dereference()
                        eval_stack.append(val.eval(op))
                    else:
                        raise ValueError(f"Not enough operands to perform calculation | ct.Operator {val}, op1 {op}")
                else:
                    op2 = eval_stack.pop()
                    # print(f"OP={op}|OP2={op2}")
                    if val != '=':
                        if type(op) is ct.Variable:
                            op = op.dereference()
                        if type(op2) is ct.Variable:
                            op2 = op2.dereference()
                    else:
                        if type(op) is ct.Variable:
                            op = op.dereference()
                        if op2 not in env:
                            env.append(op2)
                    eval_stack.append(val.eval(op, op2))
        elif type(val) is ct.Function:
            if not eval_stack:
                if rpn:  # ct.Function without ct.Variable, but there is still input
                    raise ValueError(f"Not enough operands to perform calculation | ct.Operator {val}")
                else:   # Only ct.Function
                    eval_stack.append(val)
            else:
                eval_stack.append(val.apply(eval_stack.pop()))
        else:
            raise NotImplementedError(val, type(val))
    if len(eval_stack) != 1:
        raise ValueError("Expression doesn't evaluate to a single value")
    # print("EVAL STACK:", eval_stack)
    res = eval_stack[0]
    if type(res) is ct.Variable:
        return res.v
    if type(res) is ct.Function:
        return res.body
    return res

def expand_tokens(tokens):
    split_re = r'([\*\^\/\(\)\-\+\%\=\?\[\]])'
    exp = []
    expanded = [c for c in re.split(split_re, tokens) if c]
    n = len(expanded)
    accum = None
    i = 0
    while i < n:
        t = expanded[i]
        if accum is None:
            accum = t
        else:
            accum += t
        if t == '[':
            # print("Start collecting ct.Matrix")
            n_open = 1
            while True:
                i += 1
                if n_open <= 0 or i >= n:
                    break
                t = expanded[i]
                if t == '[':
                    n_open += 1
                elif t == ']':
                    n_open -= 1 
                accum += t
            if accum:
                exp.append(accum)
                accum = None
            continue

        if t in list('+-'):
            unary = True
            # print("Checking if +- is unary")
            prev = expanded[i-1] if i > 0 else None
            # print("prev:", prev)
            if prev and len(prev) > 1:
                prev = prev[-1]
            if prev and (prev in '0123456789)' or prev not in '+-*/%^=?('):
                unary = False
            else:
                next = expanded[i+1] if i < (n-1) else None
                # print("next:", next)
                if next and len(next) > 1:
                    next = next[0]
                if next and next not in '0123456789':
                    unary = False

            if not unary:
                exp.append(accum)
                accum = None
        else:
            exp.append(accum)
            accum = None
        i += 1
    if accum is not None:
        exp.append(accum)
    return exp

def tokens_to_expr(tokens, env):
    expr = []
    for tk in tokens:
        obj = match_token(tk, env)
        if obj is None:
            print(f"Unrecognized token: {tk}")
            expr = []
            break
        expr.append(obj)
    return expr


def combine_functions(tokens, env):
    n = len(tokens)
    for i in range(n):
        if type(tokens[i]) is ct.Function and i + 1 < n and tokens[i + 1] != '(':
            tokens[i] = ct.Variable(tokens[i].name)
    if len(tokens) < 6:
        return tokens
    if ct.Operator('=') not in tokens:
        return tokens
    print("Start working on ct.Function")
    func_name, lp, var, rp, assign, *expr = tokens
    print("EXPR:", expr)
    if type(func_name) not in [ct.Function, ct.Variable]:
        return tokens
    if lp != '(' or rp != ')' or assign != ct.Operator('='):
        return tokens
    if str(func_name) == str(var):
        raise ValueError("Function name and argument should not be the same")
    body = []
    for _ in expr:
        if type(_) in [ct.Variable, ct.Function]:
            if _.name == str(func_name):
                raise ValueError("Recursion is prohibited. Nice try")
            else:
                body.append(_.name)
        else:
            body.append(str(_))
    
    func_body = ' '.join(body)
    if 'name' in dir(func_name):
        func_name = func_name.name
    f = ct.Function(str(func_name), str(var), func_body, env)
    
    print(f"Func_name: {func_name} ({type(func_name)})")
    for i in range(len(env)):
        if str(env[i]) == func_name or (type(env[i]) in [ct.Function, ct.Variable] and env[i].name == func_name):
            env.remove(env[i])
            break
    
    env.append(f)

    return [f]

def evaluate(inp, env=None, return_rpn=False):
    """ 
    Evaluation pipeline
    """
    if env is None:
        env = []
    result = None
    # Remove all spaces
    tokens = ''.join([c for c in inp.split(" ") if c])
    print("Tokens:", tokens)
    # Convert tokens to expression. One token can actually contain many statements that need to be separated: "-x^2+3x"
    exp_tokens = expand_tokens(tokens)
    print("Expanded tokens:", exp_tokens)

    expr = tokens_to_expr(exp_tokens, env)
    expr = combine_functions(expr, env)
    if not expr:
        return None

    print("Expression:", [(c, type(c)) for c in expr])
    # At this point all tokens are interpreted and expanded, so we can
    # proceed with preparing it into form that is suitable for calculation
    rpn = infix_to_rpn(expr)
    print("RPN:", rpn)
    if return_rpn:
        return rpn
    try:
        result = evaluate_rpn(rpn, env)
        # print("Result:", result)
    except ValueError as e:
        print(e)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--quiet', '-q', help="Quite mode: display output only when asked for", default=False, action='store_true')

    args = parser.parse_args()

    env = []

    default_functions = [ct.Function('sin', 'x', 'sin(x)', env, f=lambda x: sin(x)), ct.Function('cos', 'x', 'cos(x)', env, f=lambda x: cos(x)),
                        ct.Function('tan', 'x', 'tan(x)', env, f=lambda x: tan(x)), ct.Function('tanh', 'x', 'tanh(x)', env, f=lambda x: tanh(x))]
    env.extend(default_functions)
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

        try:
            result = evaluate(inp, env)
            print(result)
        except Exception as e:
            print(e)
