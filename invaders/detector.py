from typing import Type

import numpy as np

from invaders.score import DiffScoreEngine
from invaders.score import ScoreEngine
from invaders.shape import Shape


class BaseDetector:
    score_engine_cls: Type[ScoreEngine]
    min_accepted_score: int

    def __init__(self, space: Shape, invader: Shape):
        self.space = space
        self.invader = invader
        self.detected_invaders = []

    def crawl(self):
        """
        Basic, unoptimized crawling implementation.
        """
        for row in range(-self.invader.rows_num, self.space.rows_num):
            for col in range(-self.invader.cols_num, self.space.cols_num):
                self._detect(row, col)
        return self.detected_invaders

    def _detect(self, row, col):
        detected_invader = self.score_engine_cls(self.space, self.invader, row, col).detect()
        if detected_invader.score > self.min_accepted_score:
            self.detected_invaders.append(detected_invader)


class PreFilteringDetector(BaseDetector):
    """
    Detector executing precise score calculation only for lo
    """

    max_fill_diff_ratio = 0.2

    def crawl(self):
        fill_counts = self._prepare_fill_count()
        invader_fill_count = np.sum(self.invader.arr)

        for row in range(0, self.space.rows_num - self.invader.rows_num):
            current_fill_count = np.sum(fill_counts[row, : self.invader.cols_num - 1])

            for col in range(0, self.space.cols_num - self.invader.cols_num):
                current_fill_count += fill_counts[row, col + self.invader.cols_num]

                if (
                    abs(current_fill_count - invader_fill_count) / self.invader.size
                    < self.max_fill_diff_ratio
                ):
                    self._detect(row, col)

                current_fill_count -= fill_counts[row, col]

        return self.detected_invaders

    def _prepare_fill_count(self):
        """
        Prepare 2d array that for each point (row, col) contains sum of filled points
        within `invader.rows_num` distance.
        """
        # Minimize lookup time by using direct references
        invader_rows_num = self.invader.rows_num
        space_rows_num = self.space.rows_num
        space_cols_num = self.space.cols_num
        space_arr = self.space.arr

        return np.array(
            [
                [
                    np.sum(space_arr[row : row + invader_rows_num, col])
                    for col in range(space_cols_num)
                ]
                for row in range(space_rows_num - invader_rows_num + 1)
            ]
        )


class DiffDetector(BaseDetector):
    score_engine_cls = DiffScoreEngine
    min_accepted_score = 0.82


class PreFilteringDiffDetector(PreFilteringDetector):
    score_engine_cls = DiffScoreEngine
    min_accepted_score = 0.82
