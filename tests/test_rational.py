from computor_types import *

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