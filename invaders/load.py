import numpy as np


def load_array_from_file(filename):
    with open(f'sample_data/{filename}') as f:
        txt = f.read()
    return load_array_from_str(txt)


def load_array_from_str(txt):
    return np.array([[c == "o" for c in line] for line in txt.strip().split('\n')])


def join_array(arr):
    return "\n".join("".join("o" if val else "-" for val in line) for line in arr)
