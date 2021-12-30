from invaders.detector import MatrixDiffDetector
from invaders.detector import MatrixDiffFilteringDetector
from invaders.detector import SequenceDiffFilteringDetector
from invaders.shape import load_shape_from_file

_invaders_filenames = [
    "sample_data/invader1.txt",
    "sample_data/invader2.txt",
]
_space_filename = "sample_data/space.txt"


_invaders = []
_space = None


def run_once(detector_cls, print_result=True, detector_params=None):
    # Cache loaded shapes so that this function can be run with %timeit
    global _space
    global _invaders

    if _invaders_filenames and not _invaders:
        for invader_filename in _invaders_filenames:
            _invaders.append(load_shape_from_file(invader_filename))

    if _space is None:
        _space = load_shape_from_file("sample_data/space.txt")

    detected_invaders = []
    for invader in _invaders:
        detected_invaders.extend(detector_cls(_space, invader, **(detector_params or {})).crawl())

    if print_result:
        print("\n".join(str(detected_invader) for detected_invader in detected_invaders))
        print(f"Total results: {len(detected_invaders)}")


def run_once_sequence_diff_filtering_detector(print_result=True):
    run_once(
        SequenceDiffFilteringDetector,
        print_result,
        detector_params={"detected_invader_min_score": 0.8, "fill_ratio_max_diff": 0.2},
    )


def run_once_matrix_diff_filtering_detector(print_result=True):
    run_once(
        MatrixDiffFilteringDetector,
        print_result,
        detector_params={"detected_invader_min_score": 0.82, "fill_ratio_max_diff": 0.2},
    )


def run_once_matrix_diff_slow_detector(print_result=True):
    run_once(MatrixDiffDetector, print_result, detector_params={"detected_invader_min_score": 0.82})


if __name__ == "__main__":
    run_once_sequence_diff_filtering_detector()
