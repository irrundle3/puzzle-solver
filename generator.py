import numpy as np
import math

from cube import Cube3x3


def generate_cache(puzzle, size):
    actual_size = math.ceil(size / 18) * 18 + 1
    cache = np.zeros((actual_size, puzzle.POS_SIZE + 1), dtype=np.int16)

    cache[0] = np.append(puzzle.GOAL, 0)

    num_cached = 1
    
    while num_cached < size:
        curr = cache[(num_cached - 1) // puzzle.ADJ_COUNT]

        adj = puzzle.adjacents(curr[:-1])
        dist = np.full((puzzle.ADJ_COUNT, 1), curr[-1] + 1)
        adj = np.append(adj, dist, axis=1)

        cache[num_cached : num_cached + puzzle.ADJ_COUNT] = adj
        num_cached += puzzle.ADJ_COUNT

    return cache
