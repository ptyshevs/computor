from Term import Term
from Variable import Variable

class Operator(Term):
    available_operators = list('+-*/%^?=') + ["**"]
    precedence_map = {'+': 2, '-': 2, '%': 2, '=': 2, '*': 3, '/': 3, '**': 3, '^': 4, '?': 4}
    assoc_map = {'+': 'left', '-': 'left', '*': 'left', '/': 'left', '%': 'left',
                 '^': 'right', '=': 'right', '**': 'left', '?': 'left'}

    def __init__(self, op):
        self.op = op
        if op not in self.available_operators:
            raise ValueError(f"Bad operator: {op}")
        self.n_operands = 1 if op in list('?~') else 2

        self.precedence = self.precedence_map[op]
        self.associativity = self.assoc_map[op]

    def __repr__(self):
        return self.op
    
    def __eq__(self, o):
        return str(self) == str(o)
    
    def eval(self, l, r=None):
        """
        Order is reversed because of RPN prefix notation
        """
        if self.n_operands == 1 and r is not None:
            raise ValueError("{self} doesn't support second operator")
        if self.op == '+':
            if not r:
                return +l
            else:
                return r + l
        elif self.op == '-':
            if not r:
                return -l
            else:
                return r - l
        elif self.op == '*':
            return r * l
        elif self.op == '/':
            return r / l
        elif self.op == '%':
            return r % l
        elif self.op == '^':
            return r ** l
        elif self.op == '**':
            return r @ l
        elif self.op == '?':
            return l
        elif self.op == '~':  # TODO: Maybe implement this one
            return -l
        elif self.op == '=':
            # print("Assignment:", l, r)
            if type(r) is Variable:
                r.v = l
            else:
                raise NotImplementedError(f"Cannot assign {l} to {r}")
            return r
        else:
            raise NotImplementedError(f"Don't know what to do with {self.op}")