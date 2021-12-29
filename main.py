from invaders import load
from invaders import score


def main():
    invader1 = load.load_array_from_file('invader1.txt')
    invader2 = load.load_array_from_file('invader2.txt')
    space = load.load_array_from_file('space.txt')

    results = []
    results.extend(find_invader_with_sums(space, invader1))
    results.extend(find_invader_with_sums(space, invader2))

    print_detected_invaders(space, results)


def main_pure_find():
    invader1 = load.load_array_from_file('invader1.txt')
    invader2 = load.load_array_from_file('invader2.txt')
    space = load.load_array_from_file('space.txt')

    def find():
        find_invader_with_sums(space, invader1)
        find_invader_with_sums(space, invader2)

    return find


def find_invader_with_sums(space, invader):
    import numpy as np
    sums = prepare_sums(space, invader_shape=invader.shape)
    invader_sum = np.sum(invader)
    results = []

    for x in range(0, space.shape[0] - invader.shape[0]):
        xy_sum = np.sum(sums[x, invader.shape[1] - 1])
        for y in range(0, space.shape[1] - invader.shape[1]):
            xy_sum += sums[x, y+invader.shape[1]]
            if abs(xy_sum - invader_sum) / invader.size < 0.2:
                detected_invader = score.similarity_score(space, invader, x, y)
                if detected_invader.score > 0.82:
                    results.append(detected_invader)
            xy_sum -= sums[x, y]
    return results


def prepare_sums(space, invader_shape):
    import numpy as np
    sums = np.array([
        [np.sum(space[x:x+invader_shape[0], y]) for y in range(space.shape[1])]
        for x in range(space.shape[0] - invader_shape[0] + 1)
    ])
    return sums


def find_invader(space, invader):
    results = []
    for x in range(-invader.shape[0], space.shape[0]):
        for y in range(-invader.shape[1], space.shape[1]):
            detected_invader = score.similarity_score(space, invader, x, y)
            if detected_invader.score > 0.82:
                results.append(detected_invader)
    return results


def print_detected_invaders(space, detected_invaders):
    for invader in detected_invaders:
        print('--------')
        print((invader.x, invader.y))
        print(load.join_array(
            space[invader.x:invader.x + invader.size_x, invader.y:invader.y + invader.size_y]
        ))

    print(f'Total results: {len(detected_invaders)}')


if __name__ == "__main__":
    main()
