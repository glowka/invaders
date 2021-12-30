from functools import cached_property

import numpy as np

from invaders.shape import DetectedInvader
from invaders.shape import Shape


class ScoreEngine:
    def __init__(self, space: Shape, invader: Shape, row: int = 0, col: int = 0):
        assert -invader.rows_num <= row < space.rows_num
        assert -invader.cols_num <= col < space.cols_num

        self.invader = invader
        self.space = space
        self.invader_rows_num, self.invader_row = self._adjust_invader_to_fit_space(
            invader.rows_num, row, space.rows_num
        )
        self.invader_cols_num, self.invader_col = self._adjust_invader_to_fit_space(
            invader.cols_num, col, space.cols_num
        )
        self.space_row = max(row, 0)
        self.space_col = max(col, 0)

    def detect(self) -> "DetectedInvader":
        raise NotImplementedError

    @staticmethod
    def _adjust_invader_to_fit_space(invader_size, space_i, space_size):
        if space_i < 0:
            adjusted_invader_size = invader_size + space_i
            adjusted_invader_i = abs(space_i)
        elif space_i > space_size - invader_size:
            adjusted_invader_size = space_size - space_i
            adjusted_invader_i = 0
        else:
            adjusted_invader_size = invader_size
            adjusted_invader_i = 0
        return adjusted_invader_size, adjusted_invader_i

    @cached_property
    def subspace(self):
        return self.space[
            self.space_row : self.space_row + self.invader_rows_num,
            self.space_col : self.space_col + self.invader_cols_num,
        ]

    @cached_property
    def subinvader(self):
        return self.invader[
            self.invader_row : self.invader_row + self.invader_rows_num,
            self.invader_col : self.invader_col + self.invader_cols_num,
        ]


class MatrixDiffScoreEngine(ScoreEngine):
    """
    Score based on invader and space arrays diff.
    """

    def detect(self):
        score = np.sum(self.subspace == self.subinvader) / (
            self.invader_rows_num * self.invader_cols_num
        )

        return DetectedInvader(
            self.space,
            self.invader,
            score,
            row=self.space_row,
            col=self.space_col,
            rows_num=self.invader_rows_num,
            cols_num=self.invader_cols_num,
        )
