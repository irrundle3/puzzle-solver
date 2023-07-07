import time

from puzzles import Cube3
import generator as gen
from generator import Repeats, Pruning


def main():
    t_start = time.time_ns()
    Cube3.init()
    search_cache = gen.generate_bfs(Cube3, Repeats.REMOVE, Pruning.BACKTRACKS, int(1e7))
    print(f"\nGenerated cache in {(time.time_ns() - t_start) / 1e9} seconds:")
    gen.save_cache(Cube3, 'search_cache', search_cache)
    print(search_cache)
    print(f"{search_cache.shape}\n")


if __name__ == '__main__':
    main()