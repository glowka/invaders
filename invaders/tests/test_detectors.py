from collections import defaultdict

import numpy as np

from invaders.detectors import BaseDetector
from invaders.detectors import FilteringDetector
from invaders.shapes import Shape

# 6 x 10
invader_txt = """
oooooooooo
o--------o
o--o--o--o
o---oo---o
o--------o
oooooooooo
"""

# 10 x 20
space_text = """
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
--------------------
"""

min_row = -3
min_col = -5
max_row = 10 - 6 + 3
max_col = 20 - 10 + 5


class TestBaseDetector:
    def test_crawling_range(self):
        invader = Shape.load_from_str(invader_txt)
        space = Shape.load_from_str(space_text)
        engine_calls = defaultdict(int)

        class TestDetector(BaseDetector):
            def _detect(self, row, col):
                engine_calls[(row, col)] += 1

        detector = TestDetector(space, invader)
        detector.crawl()

        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                assert engine_calls[(row, col)] == 1, (row, col)
        assert len(engine_calls) == (max_row - min_row) * (max_col - min_col)


class TestFilteringDetector:
    def test_crawling_range__cover_all(self):
        invader = Shape.load_from_str(invader_txt)
        space = Shape.load_from_str(space_text)
        engine_calls = defaultdict(int)

        class TestDetector(FilteringDetector):
            fill_ratio_max_diff = 1.0

            def _detect(self, row, col):
                engine_calls[(row, col)] += 1

        detector = TestDetector(space, invader)
        detector.crawl()

        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                assert engine_calls[(row, col)] == 1, (row, col)
        assert len(engine_calls) == (max_row - min_row) * (max_col - min_col)

    def test_crawling_range__omit_inside_edges(self):
        invader = Shape.load_from_str(invader_txt)
        space = Shape.load_from_str(space_text)
        engine_calls = defaultdict(int)

        class TestDetector(FilteringDetector):
            fill_ratio_max_diff = 0.0

            def _detect(self, row, col):
                engine_calls[(row, col)] += 1

        detector = TestDetector(space, invader)
        detector.crawl()

        for row in range(0, 10 - 6):
            for col in range(0, 20 - 10):
                assert engine_calls[(row, col)] == 0, (row, col)

    def test_prepare_fill_map(self):
        invader = Shape.load_from_str("-o-\n" "---\n")
        space = Shape.load_from_str("ooo\n" "ooo\n" "---\n" "---\n" "---\n")

        detector = FilteringDetector(space, invader)
        fill_map = detector._prepare_fill_map()
        expected_fill_map = np.array(
            [np.full(3, fill_value=2), np.ones(3, dtype=int), *np.zeros((2, 3), dtype=int)]
        )
        assert (fill_map == expected_fill_map).all()
