from invaders import load
from invaders import score


invader1_txt = '''
--o-----o--
---o---o---
--ooooooo--
-oo-ooo-oo-
ooooooooooo
o-ooooooo-o
o-o-----o-o
---oo-oo---
'''

invader2_txt = '''
-----------
---o---o---
--ooooooo--
-oo-ooo-oo-
ooooooooooo
o-ooooooo-o
o-o-----o-o
---oo-oo---
'''

invader_top_edge = '''
-oo-ooo-oo-
ooooooooooo
o-ooooooo-o
o-o-----o-o
---oo-oo---
-----------
-----------
-----------
'''


invader_bottom_edge = '''
-----------
-----------
-----------
--o-----o--
---o---o---
--ooooooo--
-oo-ooo-oo-
ooooooooooo
'''


def test_identical_100():
    invader = load.load_array_from_str(invader1_txt)
    assert score.similarity_score(invader, invader).score == 1.0


def test_different_2_chars():
    invader1 = load.load_array_from_str(invader1_txt)
    invader2 = load.load_array_from_str(invader2_txt)
    assert score.similarity_score(space=invader2, shape=invader1).score == (8*11 - 2) / (8*11)


def test_top_edge():
    invader = load.load_array_from_str(invader1_txt)
    space = load.load_array_from_str(invader_top_edge)
    assert score.similarity_score(space, invader, x=-3, y=0).score == 1.0


def test_bottom_edge():
    invader = load.load_array_from_str(invader1_txt)
    space = load.load_array_from_str(invader_bottom_edge)
    assert score.similarity_score(space, invader, x=3, y=0).score == 1.0


