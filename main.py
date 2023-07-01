import time

import generator
from puzzles.cube3 import Cube3


def main():
    t_start = time.time_ns()
    search_cache = generator.generate_bfs(Cube3, int(1e7), unique=True, prevent_backtrace=True)
    print(f"\nGenerated cache in {(time.time_ns() - t_start) / 1e9} seconds:")
    generator.save_cache(Cube3, 'search_cache', search_cache)
    print(f"{search_cache}\n")


if __name__ == '__main__':
    main()