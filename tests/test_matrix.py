from computor_types import *
from computorv2 import evaluate

def test1():
    assert str(evaluate('[2^3]')) == '[[8]]'
    assert str(evaluate('[2^(-3)]')) == '[[1/8]]'

def test_complex_parsing():
    assert str(evaluate('[[2+3, 3+4] ; [4-4, 5   - 6]]')) == '[[5, 7];[0, -1]]'

def test_init_different_length():
    try:
        evaluate('[[2];[3,4]]')
        assert False
    except ValueError as e:
        assert str(e) == 'Attempted to create matrix of different column length: 2 != 1'
