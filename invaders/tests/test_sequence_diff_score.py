from invaders import scores
from invaders.shapes import Shape

invader_txt = """
--o-----o--
---o---o---
--ooooooo--
-oo-ooo-oo-
ooooooooooo
o-ooooooo-o
o-o-----o-o
---oo-oo---
"""


def test_identical_100():
    invader = Shape.load_from_str(invader_txt)
    assert scores.SequenceDiffScoreEngine(invader, invader).calculate().score == 1.0


def test_different_2_chars():
    similar_invader_txt = "\n".join(
        (
            "-----------",
            "---o---o---",
            "--ooooooo--",
            "-oo-ooo-oo-",
            "ooooooooooo",
            "o-ooooooo-o",
            "o-o-----o-o",
            "---oo-oo---",
        )
    )

    invader1 = Shape.load_from_str(invader_txt)
    invader2 = Shape.load_from_str(similar_invader_txt)
    score_val = scores.SequenceDiffScoreEngine(space=invader2, invader=invader1).calculate().score
    assert round(score_val, 2) == round((8 * 11 - 2) / (8 * 11), 2)


def test_top_edge():
    invader_top_edge_txt = "\n".join(
        (
            "-oo-ooo-oo-",
            "ooooooooooo",
            "o-ooooooo-o",
            "o-o-----o-o",
            "---oo-oo---",
            "-----------",
            "-----------",
            "-----------",
        )
    )

    invader = Shape.load_from_str(invader_txt)
    space = Shape.load_from_str(invader_top_edge_txt)
    assert scores.SequenceDiffScoreEngine(space, invader, row=-3, col=0).calculate().score == 1.0


def test_bottom_edge():
    invader_bottom_edge_txt = "\n".join(
        (
            "-----------",
            "-----------",
            "-----------",
            "--o-----o--",
            "---o---o---",
            "--ooooooo--",
            "-oo-ooo-oo-",
            "ooooooooooo",
        )
    )

    invader = Shape.load_from_str(invader_txt)
    space = Shape.load_from_str(invader_bottom_edge_txt)
    assert scores.SequenceDiffScoreEngine(space, invader, row=3, col=0).calculate().score == 1.0
