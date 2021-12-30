from invaders import score
from invaders.shape import Shape

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
    assert score.DiffScoreEngine(invader, invader).detect().score == 1.0


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
    assert score.DiffScoreEngine(space=invader2, shape=invader1).detect().score == (8 * 11 - 2) / (
        8 * 11
    )


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
    assert score.DiffScoreEngine(space, invader, row=-3, col=0).detect().score == 1.0


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
    assert score.DiffScoreEngine(space, invader, row=3, col=0).detect().score == 1.0
