from invaders.detector import MatrixDiffFilteringDetector
from invaders.shape import load_shape_from_file


def test_invader1():
    invader = load_shape_from_file("sample_data/invader1.txt")
    space = load_shape_from_file("sample_data/space.txt")

    detector = MatrixDiffFilteringDetector(
        space, invader, detected_invader_min_score=0.82, fill_ratio_max_diff=0.2
    )
    detector.crawl()
    assert len(detector.detected_invaders) == 3
    assert [(di.row, di.col) for di in detector.detected_invaders] == [(1, 74), (12, 85), (13, 60)]


def test_invader2():
    invader = load_shape_from_file("sample_data/invader2.txt")
    space = load_shape_from_file("sample_data/space.txt")

    detector = MatrixDiffFilteringDetector(
        space, invader, detected_invader_min_score=0.82, fill_ratio_max_diff=0.2
    )
    detector.crawl()
    assert len(detector.detected_invaders) == 5
    assert [(di.row, di.col) for di in detector.detected_invaders] == [
        (0, 42),
        (15, 35),
        (28, 16),
        (41, 82),
        (45, 17),
    ]
