from invaders.detector import PreFilteringDiffDetector
from invaders.shape import load_shape_from_file


def test_invader1():
    invader = load_shape_from_file("sample_data/invader1.txt")
    space = load_shape_from_file("sample_data/space.txt")

    detector = PreFilteringDiffDetector(space, invader)
    detector.crawl()
    assert len(detector.detected_invaders) == 3
    assert [(di.row, di.col) for di in detector.detected_invaders] == [(1, 74), (12, 85), (13, 60)]


def test_invader2():
    invader = load_shape_from_file("sample_data/invader2.txt")
    space = load_shape_from_file("sample_data/space.txt")

    detector = PreFilteringDiffDetector(space, invader)
    detector.crawl()
    assert len(detector.detected_invaders) == 4
    assert [(di.row, di.col) for di in detector.detected_invaders] == [
        (0, 42),
        (15, 35),
        (28, 16),
        (41, 82),
    ]