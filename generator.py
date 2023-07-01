import numpy as np
import math


def generate_bfs(puzzle, size, *, unique=False, prevent_backtrace=False):
    actual_size = size + puzzle.ADJ_COUNT
    cache = np.zeros((actual_size, puzzle.POS_SIZE + 2), dtype=np.int8)

    cache[0] = np.append(puzzle.GOAL, [0, -1])
    num_cached = 1
    queue_idx = 0
    
    while num_cached < size:
        curr = cache[queue_idx]
        queue_idx += 1

        adj = puzzle.adjacents(curr[:-2])
        dist = np.full((len(adj), 1), curr[-2] + 1)
        adj = np.append(adj, dist, axis=1)
        mov = np.reshape(np.arange(0, puzzle.ADJ_COUNT, dtype=np.int8), (-1, 1))
        adj = np.append(adj, mov, axis=1)

        if prevent_backtrace:
            last_move = curr[-1]
            if last_move != -1:
                adj = np.delete(adj, puzzle.inverse_move(last_move), axis=0)

        cache[num_cached : num_cached + len(adj)] = adj
        num_cached += len(adj)

    # remove last column
    cache = np.delete(cache, -1, axis=1)

    # remove any ending zero rows
    cache = np.delete(cache, np.s_[-(actual_size - num_cached):], axis=0)

    if unique:
        cache = _remove_repeats(cache)

    return cache


def save_cache(puzzle, cache_name, cache):
    np.save(f'puzzles/{puzzle.NAME}/{cache_name}', cache)


def load_cache(puzzle, cache_name):
    return np.load(f'puzzles/{puzzle.NAME}/{cache_name}.npy')


def _remove_repeats(cache):
    _, indices = np.unique(cache[:, :-1], axis=0, return_index=True)
    return cache[np.sort(indices)]