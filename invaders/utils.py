import numpy as np


def arr_from_str(txt):
    return np.array([[c == "o" for c in line] for line in txt.strip().split("\n")])


def arr_to_str(arr):
    return "\n".join("".join("o" if val else "-" for val in line) for line in arr)


def geo_mean(iterable):
    a = np.array(iterable)
    return a.prod() ** (1.0 / len(a))
