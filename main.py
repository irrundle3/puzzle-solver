import time

from puzzles import Cube3
import generator as gen
from generator import Repeats_Mode as RMode, Pruning_Mode as PMode


def main():
    t_start = time.time_ns()
    search_cache = gen.generate_bfs(Cube3, int(1e7), RMode.REMOVE, PMode.BACKTRACKS)
    print(f"\nGenerated cache in {(time.time_ns() - t_start) / 1e9} seconds:")
    gen.save_cache(Cube3, 'search_cache', search_cache)
    print(f"{search_cache}\n")


if __name__ == '__main__':
    main()