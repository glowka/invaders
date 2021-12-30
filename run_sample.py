from invaders.detector import DiffDetector
from invaders.detector import PreFilteringDiffDetector
from invaders.shape import load_shape_from_file

_invaders_files = [
    "sample_data/invader1.txt",
    "sample_data/invader2.txt",
]

_invaders = []
_space = None


def run_once(detector_cls, print_result=True):
    # Cache loaded shapes so that this function can be run with %timeit
    global _space
    global _invaders

    if _invaders_files and not _invaders:
        for invader_file in _invaders_files:
            _invaders.append(load_shape_from_file(invader_file))

    if _space is None:
        _space = load_shape_from_file("sample_data/space.txt")

    detected_invaders = []
    for invader in _invaders:
        detected_invaders.extend(
            detector_cls(
                _space, invader, detected_invader_min_score=0.82, fill_ratio_max_diff=0.2
            ).crawl()
        )

    if print_result:
        print("\n".join(str(detected_invader) for detected_invader in detected_invaders))
        print(f"Total results: {len(detected_invaders)}")


if __name__ == "__main__":
    run_once(PreFilteringDiffDetector)
