import itertools

from typing import Type

import numpy as np

from invaders.scores import BaseScoreEngine
from invaders.scores import MatrixDiffScoreEngine
from invaders.scores import SequenceDiffScoreEngine
from invaders.shapes import Shape


class BaseDetector:
    score_engine_cls: Type[BaseScoreEngine]
    detected_invader_min_score: int

    def __init__(self, space: Shape, invader: Shape, detected_invader_min_score=None):
        self.space = space
        self.invader = invader
        self.detected_invaders = []

        if detected_invader_min_score is not None:
            self.detected_invader_min_score = detected_invader_min_score

    def crawl(self):
        """
        Basic, unoptimized crawling implementation.
        """
        for row in self._range_inside_and_outside(self.space.rows_num, self.invader.rows_num):
            for col in self._range_inside_and_outside(self.space.cols_num, self.invader.cols_num):
                self._detect(row, col)
        return self.detected_invaders

    def _detect(self, row, col):
        detected_invader = self.score_engine_cls(self.space, self.invader, row, col).calculate()
        if detected_invader.score >= self.detected_invader_min_score:
            self.detected_invaders.append(detected_invader)

    _edge_depth = 0.5

    def _range_inside(self, space_size, invader_size):
        return range(space_size - invader_size)

    def _range_inside_and_outside(self, space_size, invader_size):
        return range(
            -int(invader_size * self._edge_depth),
            space_size - int(invader_size * self._edge_depth),
        )

    def _range_outside(self, space_size, invader_size):
        return itertools.chain(
            range(-int(invader_size * self._edge_depth), 0),
            range(space_size - invader_size, space_size - int(invader_size * self._edge_depth)),
        )


class FilteringDetector(BaseDetector):
    """
    Detector that uses basic fill count heuristic to execute heavy score calculation
    only for most promising points of space.

    The heuristic is to sum fill count for any point of the space and compare it with fill count
    of the shape: abs(PoS - I) / I.

    If the fill ratio for is above `fill_ratio_max_diff` the point is ignored.
    """

    fill_ratio_max_diff = 0.3

    def __init__(self, *args, fill_ratio_max_diff=None, **kwargs):
        super().__init__(*args, **kwargs)
        if fill_ratio_max_diff is not None:
            self.fill_ratio_max_diff = fill_ratio_max_diff

    def crawl(self):
        fill_map = self._prepare_fill_map()
        invader_fill_count = np.sum(self.invader.arr)

        # Crawl inside the edges relying on fill_map array to exclude obvious cases
        # and call the scoring engine only when a precise assessment is required
        for row in self._range_inside(self.space.rows_num, self.invader.rows_num):
            current_fill_count = np.sum(fill_map[row, : self.invader.cols_num - 1])

            for col in self._range_inside(self.space.cols_num, self.invader.cols_num):
                current_fill_count += fill_map[row, col + self.invader.cols_num]

                if (
                    abs(current_fill_count - invader_fill_count) / invader_fill_count
                    <= self.fill_ratio_max_diff
                ):
                    self._detect(row, col)

                current_fill_count -= fill_map[row, col]

        # Crawl outside the edges using standard brute force method
        for row in self._range_outside(self.space.rows_num, self.invader.rows_num):
            for col in self._range_inside_and_outside(self.space.cols_num, self.invader.cols_num):
                self._detect(row, col)

        for row in self._range_inside(self.space.rows_num, self.invader.rows_num):
            for col in self._range_outside(self.space.cols_num, self.invader.cols_num):
                self._detect(row, col)

        self.detected_invaders.sort(key=lambda i: (i.row, i.col))
        return self.detected_invaders

    def _prepare_fill_map(self):
        """
        Prepare 2d array that for each point (row, col) contains sum of filled points
        within `invader.rows_num` distance.
        """
        arr = np.zeros(
            (self.space.rows_num - self.invader.rows_num + 1, self.space.cols_num), dtype=int
        )
        for row in range(arr.shape[0]):
            arr[row, :] = np.sum(self.space[row : row + self.invader.rows_num, :], axis=0)
        return arr


class MatrixDiffDetector(BaseDetector):
    score_engine_cls = MatrixDiffScoreEngine
    detected_invader_min_score = 0.8


class MatrixDiffFilteringDetector(FilteringDetector):
    score_engine_cls = MatrixDiffScoreEngine
    detected_invader_min_score = 0.8


class SequenceDiffFilteringDetector(FilteringDetector):
    score_engine_cls = SequenceDiffScoreEngine
    detected_invader_min_score = 0.75
