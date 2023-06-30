import numpy as np
import math


def generate_bfs(puzzle, size):
    actual_size = math.ceil(size / 18) * 18 + 1
    cache = np.zeros((actual_size, puzzle.POS_SIZE + 1), dtype=np.int8)

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


def save_cache(puzzle, cache_name, cache):
    np.save(f'puzzles/{puzzle.NAME}/{cache_name}', cache)


def load_cache(puzzle, cache_name):
    return np.load(f'puzzles/{puzzle.NAME}/{cache_name}.npy')