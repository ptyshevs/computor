from Term import Term

class Variable(Term):
    def __init__(self, name, v=None):
        self.name = name.lower()
        self.v = v
    
    def assign(self, v):
        self.v = v
    
    def __repr__(self):
        s = str(self.name)
        if self.v:
            s += f'={self.v}'
        return s
    
    def __eq__(self, o):
        if type(o) is Variable:
            return str(self.name) == str(o.name)
        else:
            return str(self) == str(o)

    def __add__(self, o):
        if self.v is None:
            raise ValueError("Unassigned variable addition")
        return self.v + o
    
    def dereference(self):
        # if self.v is None:
            # raise ValueError(f"Attempted to dereference Variable {self}")
        return self.v