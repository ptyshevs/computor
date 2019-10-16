from computorv2 import evaluate

def test1():
    assert str(evaluate('(3+2i)/(4-3i)')) == '6/25+17/25i'
    assert str(evaluate('(4+5i)/(2+6i)')) == '19/20-7/20i'
    assert str(evaluate('-4-5i/-2-6i')) == '-4-7/2i'
    assert str(evaluate('(-6-3i)/(4+6i)')) == '-21/26+6/13i'

def test2():
    assert str(evaluate('[(2-1i)/(-3+6i)]')) == '[[-4/15-1/5i]]'