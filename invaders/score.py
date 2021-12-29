import dataclasses

import numpy as np


MINIMAL_EDGE_SHAPE_SIZE_RATIO = 0.5


@dataclasses.dataclass
class DetectedInvader:
    score: float
    x: int
    y: int
    size_x: int
    size_y: int


def similarity_score(space: np.ndarray, shape: np.ndarray, x: int = 0, y: int = 0) -> DetectedInvader:
    size_x = min(shape.shape[0], space.shape[0] - x, shape.shape[0] + x)
    size_y = min(shape.shape[1], space.shape[1] - y, shape.shape[1] + y)

    edge_shape_size_ratio = size_x / shape.shape[0] * size_y / shape.shape[1]

    if edge_shape_size_ratio < MINIMAL_EDGE_SHAPE_SIZE_RATIO:
        score = 0.0
    else:
        space_x = max(x, 0)
        space_y = max(y, 0)

        shape_x = abs(min(x, 0))
        shape_y = abs(min(y, 0))

        subspace = space[space_x:space_x+size_x, space_y:space_y+size_y]
        score = np.sum(
            subspace == shape[shape_x:shape_x+size_x, shape_y:shape_y+size_y]
        ) / (size_x * size_y)

    return DetectedInvader(x=x, y=y, size_x=size_x, size_y=size_y, score=score)
