import numpy as np
from enum import Enum
import random

from puzzles import Puzzle


class Repeats(Enum):
    KEEP = 0
    REMOVE = 1
    STOP_INSERT = 2


class Pruning(Enum):
    DISABLED = 0
    BACKTRACKS = 1
    TRANSPOSABLES = 2


def generate_bfs(puzzle: Puzzle, repeats: Repeats, pruning: Pruning, size: int) -> np.ndarray:
    cache = _init_cache(puzzle, size)
    num_cached = 1
    queue_idx = 0

    while num_cached < size:
        num_cached += _expand_node(puzzle, pruning, cache, num_cached, queue_idx)
        queue_idx += 1

    return _cleanup_cache(repeats, cache, num_cached)

    
def generate_random(puzzle: Puzzle, repeats: Repeats, pruning: Pruning, size: int) -> np.ndarray:
    cache = _init_cache(puzzle, size)
    num_cached = 1

    while num_cached < size:
        num_cached += _expand_node(puzzle, pruning, cache, num_cached, random.randrange(num_cached))

    return _cleanup_cache(repeats, cache, num_cached)


def save_cache(puzzle: Puzzle, cache_name: str, cache: np.ndarray) -> None:
    np.save(f'caches/{puzzle.NAME}/{cache_name}', cache)


def load_cache(puzzle: Puzzle, cache_name: str) -> np.ndarray:
    return np.load(f'caches/{puzzle.NAME}/{cache_name}.npy')


def _init_cache(puzzle: Puzzle, size: int) -> np.ndarray:
    cache = np.zeros((size + puzzle.ADJACENT_COUNT, puzzle.POSITION_SIZE + 2), dtype=np.int8)
    cache[0] = np.append(puzzle.GOAL, [0, -1])
    return cache


def _expand_node(puzzle: Puzzle,
                 pruning: Pruning,
                 cache: np.ndarray,
                 num_cached: int,
                 curr_idx: int,
                 ) -> int:
    # Get current node
    curr = cache[curr_idx]

    # Prune the valid movess
    removed_moves = []
    last_move_idx = curr[-1]
    if last_move_idx != -1:
        if pruning.value & Pruning.BACKTRACKS.value:
            removed_moves.extend(puzzle.BACKTRACKS[last_move_idx])
        if pruning.value & Pruning.TRANSPOSABLES.value:
            removed_moves.extend(puzzle.TRANSPOSABLES[last_move_idx])
    allowed_moves = [i for i in range(puzzle.ADJACENT_COUNT) if i not in removed_moves]
    num_neighbors = len(allowed_moves)

    # Expand the neighbors via the allowed moves
    adjacents = puzzle.adjacents(curr[:-2], allowed_moves)
    adj = np.full((num_neighbors, puzzle.POSITION_SIZE + 2), curr[-2] + 1, dtype=np.int8)
    adj[:, :puzzle.POSITION_SIZE] = adjacents
    adj[:, -1] = allowed_moves

    # Update the cache with expanded neighbors
    cache[num_cached : num_cached + num_neighbors] = adj

    # Return the number of neighbors expanded
    return num_neighbors


def _cleanup_cache(repeats: Repeats, cache: np.ndarray, num_cached: int) -> np.ndarray:
    # Remove any extra rows
    cache = np.delete(cache, np.s_[-(len(cache) - num_cached):], axis=0)

    # Remove repeat nodes if in remove mode
    if repeats.value & Repeats.REMOVE.value:
        _, indices = np.unique(cache[:, :-2], axis=0, return_index=True)
        return cache[np.sort(indices)]
    else:
        return cache