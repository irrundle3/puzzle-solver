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
                removed_moves.extend(puzzle.BACKTRACKS[last_move_idx])
            if prune.value & Pruning.TRANSPOSABLES.value:
                removed_moves.extend(puzzle.TRANSPOSABLES[last_move_idx])
        allowed_moves = [i for i in range(puzzle.ADJACENT_COUNT) if i not in removed_moves]
        num_neighbors = len(allowed_moves)

        adjacents = puzzle.adjacents(curr[:-2], allowed_moves)
        adj = np.full((num_neighbors, puzzle.POSITION_SIZE + 2), curr[-2] + 1, dtype=np.int8)
        adj[:, :puzzle.POSITION_SIZE] = adjacents
        adj[:, -1] = allowed_moves

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