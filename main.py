import numpy as np
import matplotlib.pyplot as plt
import time

import generator
from puzzles.cube3x3 import Cube3x3


def main():
    t_start = time.time_ns()
    search_cache = generator.generate_bfs(Cube3x3, int(1e7))
    t_generated = time.time_ns()
    print(f"\nGenerated cache in {(t_generated - t_start) / 1e9} seconds")
    generator.save_cache(Cube3x3, 'search_cache', search_cache)
    t_saved = time.time_ns()
    print(f"Saved cache in {(t_saved - t_generated) / 1e9} seconds")
    print(f"Cache:\n{search_cache}\n")


if __name__ == '__main__':
    main()