import numpy as np
from enum import Enum

from puzzles import Puzzle


class Repeats(Enum):
    KEEP = 0
    REMOVE = 1
    STOP_INSERT = 2


class Pruning(Enum):
    DISABLED = 0
    BACKTRACKS = 1
    TRANSPOSABLES = 2


def generate_bfs(puzzle: Puzzle, size: int, repeats: Repeats, prune: Pruning):
    cache = np.zeros((size + puzzle.ADJACENT_COUNT, puzzle.POSITION_SIZE + 2), dtype=np.int8)
    cache[0] = np.append(puzzle.GOAL, [0, -1])
    num_cached = 1
    queue_idx = 0

    while num_cached < size:
        curr = cache[queue_idx]
        queue_idx += 1

        removed_moves = []
        last_move_idx = curr[-1]
        if last_move_idx != -1:
            if prune.value & Pruning.BACKTRACKS.value:
                removed_moves.append(puzzle.backtracks(last_move_idx))
            if prune.value & Pruning.TRANSPOSABLES.value:
                removed_moves.append(puzzle.transposables(last_move_idx))
        allowed_moves = np.delete(np.arange(puzzle.ADJACENT_COUNT, dtype=np.int8), removed_moves)
        num_neighbors = len(allowed_moves)

        adj = puzzle.adjacents(curr[:-2], allowed_moves)
        dist = np.full((num_neighbors, 1), curr[-2] + 1)
        prev = np.reshape(allowed_moves, (-1, 1))
        adj = np.append(np.append(adj, dist, axis=1), prev, axis=1)
        
        cache[num_cached : num_cached + num_neighbors] = adj
        num_cached += num_neighbors

    cache = np.delete(cache, np.s_[-(len(cache) - num_cached):], axis=0)

    if repeats.value & Repeats.REMOVE.value:
        cache = _remove_repeats(cache)
        print(cache.shape)

    return cache


def save_cache(puzzle: Puzzle, cache_name: str, cache: np.ndarray) -> None:
    np.save(f'caches/{puzzle.NAME}/{cache_name}', cache)


def load_cache(puzzle: Puzzle, cache_name: str) -> np.ndarray:
    return np.load(f'caches/{puzzle.NAME}/{cache_name}.npy')


def _remove_repeats(cache: np.ndarray) -> np.ndarray:
    _, indices = np.unique(cache[:, :-2], axis=0, return_index=True)
    return cache[np.sort(indices)]