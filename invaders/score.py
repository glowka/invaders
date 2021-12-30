import numpy as np

from invaders.shape import DetectedInvader
from invaders.shape import Shape


class ScoreEngine:
    def __init__(self, space: Shape, shape: Shape, row: int = 0, col: int = 0):
        assert -shape.rows_num <= row < space.rows_num
        assert -shape.cols_num <= col < space.cols_num

        self.shape = shape
        self.space = space
        self.shape_rows_num, self.shape_row = self._adjust_shape_to_fit_space(
            shape.rows_num, row, space.rows_num
        )
        self.shape_cols_num, self.shape_col = self._adjust_shape_to_fit_space(
            shape.cols_num, col, space.cols_num
        )
        self.space_row = max(row, 0)
        self.space_col = max(col, 0)

    def detect(self) -> "DetectedInvader":
        raise NotImplementedError

    @staticmethod
    def _adjust_shape_to_fit_space(shape_size, space_i, space_size):
        if space_i < 0:
            adjusted_shape_size = shape_size + space_i
            adjusted_shape_i = abs(space_i)
        elif space_i > space_size - shape_size:
            adjusted_shape_size = space_size - space_i
            adjusted_shape_i = 0
        else:
            adjusted_shape_size = shape_size
            adjusted_shape_i = 0
        return adjusted_shape_size, adjusted_shape_i


class DiffScoreEngine(ScoreEngine):
    minimal_edge_shape_size_ratio = 0.5

    def detect(self):
        edge_shape_size_ratio = (
            self.shape_rows_num / self.shape.rows_num * self.shape_cols_num / self.shape.cols_num
        )

        if edge_shape_size_ratio < self.minimal_edge_shape_size_ratio:
            score = 0.0
        else:
            subspace = self.space[
                self.space_row : self.space_row + self.shape_rows_num,
                self.space_col : self.space_col + self.shape_cols_num,
            ]
            subshape = self.shape[
                self.shape_row : self.shape_row + self.shape_rows_num,
                self.shape_col : self.shape_col + self.shape_cols_num,
            ]
            score = np.sum(subspace == subshape) / (self.shape_rows_num * self.shape_cols_num)

        return DetectedInvader(
            self.space,
            self.shape,
            score,
            row=self.space_row,
            col=self.space_col,
            rows_num=self.shape_rows_num,
            cols_num=self.shape_cols_num,
        )
