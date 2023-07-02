import numpy as np
from enum import Enum

from puzzles import Puzzle


class Repeats_Mode(Enum):
    KEEP = 0
    REMOVE = 1
    STOP_INSERT = 2


class Pruning_Mode(Enum):
    DISABLED = 0
    BACKTRACKS = 1
    TRANSPOSABLES = 2


def generate_bfs(puzzle: Puzzle, size: int, repeats: Repeats_Mode, prune: Pruning_Mode):
    actual_size = size + puzzle.ADJACENT_COUNT
    cache = np.zeros((actual_size, puzzle.POSITION_SIZE + 2), dtype=np.int8)

    cache[0] = np.append(puzzle.GOAL, [0, -1])
    num_cached = 1
    queue_idx = 0
    
    while num_cached < size:
        curr = cache[queue_idx]
        queue_idx += 1

        adj = puzzle.adjacents(curr[:-2])
        dist = np.full((len(adj), 1), curr[-2] + 1)
        adj = np.append(adj, dist, axis=1)
        mov = np.reshape(np.arange(0, puzzle.ADJACENT_COUNT, dtype=np.int8), (-1, 1))
        adj = np.append(adj, mov, axis=1)

        if prune.value & Pruning_Mode.BACKTRACKS.value:
            last_move = curr[-1]
            if last_move != -1:
                adj = np.delete(adj, puzzle.backtracks_of(last_move), axis=0)

        cache[num_cached : num_cached + len(adj)] = adj
        num_cached += len(adj)

    # remove last column
    cache = np.delete(cache, -1, axis=1)

    # remove any ending zero rows
    cache = np.delete(cache, np.s_[-(actual_size - num_cached):], axis=0)

    if repeats.value & Repeats_Mode.REMOVE.value:
        cache = _remove_repeats(cache)
        print(cache.shape)

    return cache


def save_cache(puzzle: Puzzle, cache_name: str, cache: np.ndarray) -> None:
    np.save(f'caches/{puzzle.NAME}/{cache_name}', cache)


def load_cache(puzzle: Puzzle, cache_name: str) -> np.ndarray:
    return np.load(f'caches/{puzzle.NAME}/{cache_name}.npy')


def _remove_repeats(cache: np.ndarray) -> np.ndarray:
    _, indices = np.unique(cache[:, :-1], axis=0, return_index=True)
    return cache[np.sort(indices)]