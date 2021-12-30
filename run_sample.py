from invaders.detector import PreFilteringDiffDetector
from invaders.shape import load_shape_from_file

_invader1 = None
_invader2 = None
_space = None


def run_once(print_result=True):
    global _space
    global _invader1
    global _invader2

    if _invader1 is None:
        _invader1 = load_shape_from_file("sample_data/invader1.txt")
    if _invader2 is None:
        _invader2 = load_shape_from_file("sample_data/invader2.txt")

    if _space is None:
        _space = load_shape_from_file("sample_data/space.txt")

    detected_invaders = [
        *PreFilteringDiffDetector(_space, _invader1).crawl(),
        *PreFilteringDiffDetector(_space, _invader2).crawl(),
    ]

    if print_result:
        print("\n".join(str(detected_invader) for detected_invader in detected_invaders))
        print(f"Total results: {len(detected_invaders)}")


if __name__ == "__main__":
    run_once()
