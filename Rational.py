from Term import Term

class Rational(Term):
    def __init__(self, p, q=1):
        if q == 0:
            raise ValueError(f"Failed to create rational number: division by zero: {p}/{q}")
        if p == 0:
            q = 1
        try:
            p = int(str(p))
            q = int(str(q))
        except ValueError:
            if q != 1:
                raise ValueError(f'Failed to create Rational: p is float and q is not 1: {p}/{q}')
            ps = str(p)
            dot = ps.index('.')
            order = len(ps) - 1 - dot
            p = int(ps[:dot] + ps[dot + 1:])
            q = 10 ** order

        self.p, self.q = self._simplify(p, q)

        self.v = p / float(q)

    @classmethod
    def gcd(cls, a, b):
        a = abs(a)
        b = abs(b)
        while b != 0:
            t = b
            b = a % b
            a = t
        return a

    @classmethod
    def _simplify(cls, p, q):
        g = cls.gcd(p, q)
        
        return int(p / g), int(q / g)

    def __repr__(self):
        if self.q != 1:
            return f'{self.p}/{self.q}'
        else:
            return f'{self.p}'
    
    def __add__(self, o):
        if type(o) is Rational:
            if self.q != o.q:
                common_q = self.q * o.q
                left_p = self.p * o.q
                right_p = o.p * self.q
                return Rational(left_p + right_p, common_q)
            else:
                return Rational(self.p + o.p, self.q)
        else:
            raise NotImplementedError()

    def __sub__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()

        if self.q != o.q:
            common_q = self.q * o.q
            left_p = self.p * o.q
            right_p = o.p * self.q
            return Rational(left_p - right_p, common_q)
        else:
            return Rational(self.p - o.p, self.q)
    
    def __mul__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return Rational(self.p * o.p, self.q * o.q)

    def __div__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return self * Rational(o.q, o.p)
    
    def __truediv__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return self * Rational(o.q, o.p)
    
    def __pow__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return Rational(self.v ** o.v)
    
    def __mod__(self, o):
        if type(o) is not Rational:
            raise NotImplementedError()
        return Rational(self.v % o.v)