from computor_types import *
from computorv2 import evaluate

def test_init1():
    assert str(Rational(3)) == '3'

def test_init2():
    assert str(Rational(3, 2)) == '3/2'

def test_init3():
    assert str(Rational(4, 2)) == '2'

def test_init4():
    assert str(Rational(2, 4)) == '1/2'

def test_init5():
    assert str(Rational(.5)) == '1/2'

def test_init6():
    assert str(Rational(6, 12)) == '1/2'

def test_init7():
    assert str(Rational(12, 6)) == '2'

def test_init8():
    assert str(Rational(12, 12)) == '1'

def test_init9():
    assert str(Rational(3.25)) == '13/4'

def test_init10():
    assert str(Rational(0, 25)) == '0'

def test_op1():
    assert str(evaluate('4^-1')) == '1/4'

def test_op2():
    assert str(evaluate('16^2')) == '256'

def test_op3():
    assert str(evaluate('3^(1+1+1)')) == '27'

def test_unary1():
    assert str(evaluate('-3')) == '-3'

def test_unary2():
    assert str(evaluate('-0.25')) == '-1/4'

def test_unary3():
    assert str(evaluate('+1')) == '1'

def test_unary4():
    assert str(evaluate('+3')) == '3'

def test_pow1():
    assert str(evaluate('2^-3')) == '1/8'
    assert str(evaluate('2^(-3)')) == '1/8'
