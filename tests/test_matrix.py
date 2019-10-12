from computor_types import *
from computorv2 import evaluate

def test1():
    assert str(evaluate('[2^3]')) == '[8]'
    assert str(evaluate('[2^(-3)]')) == '[1/8]'