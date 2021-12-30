import numpy as np

from invaders import utils


def load_shape_from_file(filename):
    with open(filename) as f:
        txt = f.read()
    return Shape.load_from_str(txt)


class Shape:
    def __init__(self, arr: np.ndarray):
        self.arr = arr

    @classmethod
    def load_from_str(cls, txt):
        return cls(utils.arr_from_str(txt))

    def serialize_to_str(self):
        return utils.arr_to_str(self.arr)

    def __str__(self):
        return self.serialize_to_str()

    # Wrap array interface

    @property
    def rows_num(self):
        return self.arr.shape[0]

    @property
    def cols_num(self):
        return self.arr.shape[1]

    def __getitem__(self, *args, **kwargs):
        return self.arr.__getitem__(*args, **kwargs)

    @property
    def size(self):
        return self.arr.size


class DetectedInvader:
    def __init__(
        self,
        space: Shape,
        invader: Shape,
        score: float,
        row: int,
        col: int,
        rows_num: int,
        cols_num: int,
    ):
        self.space = space
        self.invader = invader
        self.score = score
        self.row = row
        self.col = col
        self.rows_num = rows_num
        self.cols_num = cols_num

    def __str__(self):
        return "\n".join(
            (
                f"DetectedInvader at: {self.row}:{self.col}",
                utils.arr_to_str(
                    self.space[
                        self.row : self.row + self.rows_num, self.col : self.col + self.cols_num
                    ]
                ),
            )
        )
