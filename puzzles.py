from abc import ABC, abstractmethod
import numpy as np


class Puzzle(ABC):
    
    @classmethod
    @property
    @abstractmethod
    def NAME(cls) -> str: pass

    @classmethod
    @property
    @abstractmethod
    def GOAL(cls) -> np.ndarray: pass

    @classmethod
    @property
    @abstractmethod
    def POSITION_SIZE(cls) -> int: pass

    @classmethod
    @property
    @abstractmethod
    def ADJACENT_COUNT(cls) -> int: pass

    @abstractmethod
    def string(position: np.ndarray) -> str: pass

    @abstractmethod
    def expansion_of(move_index: int) -> tuple[int]: pass

    @abstractmethod
    def move_index_of(expansion: tuple[int]) -> int: pass

    @classmethod
    @abstractmethod
    def backtracks(cls, move_index: int) -> list[int]: pass

    @classmethod
    @abstractmethod
    def transposables(cls, move_index: int) -> list[int]: pass

    @classmethod
    @abstractmethod
    def move(cls, position: np.ndarray, move_index: int) -> list[int]: pass

    @classmethod
    def adjacents(cls, position: np.ndarray, allowed_moves: list[int]) -> list[int]:
        return [cls.move(position, move) for move in allowed_moves]


class Cube(Puzzle):
    
    @classmethod
    @property
    @abstractmethod
    def CUBE_SIZE(cls) -> int: return 0

    @classmethod
    @property
    def NAME(cls) -> str:
        return f'cube{cls.CUBE_SIZE}'

    @classmethod
    @property
    def GOAL(cls) -> np.ndarray:
        movable_per_side = cls.CUBE_SIZE ** 2 - cls.CUBE_SIZE % 2
        return np.sort(np.array(list(range(6)) * movable_per_side, dtype=np.int8))
    
    @classmethod
    @property
    def POSITION_SIZE(cls) -> int:
        movable_per_side = cls.CUBE_SIZE ** 2 - cls.CUBE_SIZE % 2
        return 6 * movable_per_side
    
    @classmethod
    @property
    def ADJACENT_COUNT(cls) -> int:
        return 9 * (cls.CUBE_SIZE - 1)
    
    # TODO: implement expansion_of(), move_index_of(), backtracks(), transposables()


class Cube3(Cube):
    
    @classmethod
    @property
    def CUBE_SIZE(cls) -> int:
        return 3

    def string(position: np.ndarray) -> str:
        repr  = f"        {position[0]} {position[1]} {position[2]}\n"
        repr += f"        {position[7]} 0 {position[3]}\n"
        repr += f"        {position[6]} {position[5]} {position[4]}\n\n"
        repr += f"{position[16]} {position[17]} {position[18]}   "
        repr += f"{position[8]} {position[9]} {position[10]}   "
        repr += f"{position[32]} {position[33]} {position[34]}   "
        repr += f"{position[24]} {position[25]} {position[26]}\n"
        repr += f"{position[23]} 2 {position[19]}   "
        repr += f"{position[15]} 1 {position[11]}   "
        repr += f"{position[39]} 4 {position[35]}   "
        repr += f"{position[31]} 3 {position[27]}\n"
        repr += f"{position[22]} {position[21]} {position[20]}   "
        repr += f"{position[14]} {position[13]} {position[12]}   "
        repr += f"{position[38]} {position[37]} {position[36]}   "
        repr += f"{position[30]} {position[29]} {position[28]}\n\n"
        repr += f"        {position[40]} {position[41]} {position[42]}\n"
        repr += f"        {position[47]} 5 {position[43]}\n"
        repr += f"        {position[46]} {position[45]} {position[44]}\n"
        return repr
    
    def expansion_of(move_index: int) -> tuple[int]:
        face = int(move_index / 3)
        amount = move_index - 3 * face + 1
        return face, amount
    
    def move_index_of(face: int, amount: int) -> int:
        return 3 * face + amount - 1
    
    @classmethod
    def backtracks(cls, move_index: int) -> list[int]:
        face = int(move_index / 3)
        return [cls.move_index_of(face, amount) for amount in (1, 2, 3)]
    
    @classmethod
    def transposables(cls, move_index: int) -> list[int]:
        face = int(move_index / 3)
        face = {0:5, 1:3, 2:4, 3:1, 4:2, 5:0}[face]
        return [cls.move_index_of(face, amount) for amount in (1, 2, 3)]

    @classmethod
    def move(cls, position: np.ndarray, move_index: int) -> list[int]:
        position = list(position)
        face = int(move_index / 3)
        amount = move_index - 3 * face + 1
        new_pos = position.copy()

        # Move the appropriate face
        new_pos[8*face : 8*face+8] = roll(position[8*face : 8*face+8], 2*amount)

        # Move the appropriate edges
        edges = None
        if face == 0:
            edges = [8, 9, 10, 32, 33, 34, 24, 25, 26, 16, 17, 18]
        elif face == 1:
            edges = [4, 5, 6, 18, 19, 20, 40, 41, 42, 38, 39, 32]
        elif face == 2:
            edges = [6, 7, 0, 26, 27, 28, 46, 47, 40, 14, 15, 8]
        elif face == 3:
            edges = [0, 1, 2, 34, 35, 36, 44, 45, 46, 22, 23, 16]
        elif face == 4:
            edges = [2, 3, 4, 10, 11, 12, 42, 43, 44, 30, 31, 24]
        else:
            edges = [12, 13, 14, 20, 21, 22, 28, 29, 30, 36, 37, 38]
        new_edges = roll(edges, -3 * amount)
        for new_edge, edge in zip(new_edges, edges):
            new_pos[new_edge] = position[edge]
        
        return new_pos
    

# 458.2% faster than np.roll()
# Usage speeds up Cube3.adjacents() by 194.7%
def roll(arr: list[int], offset: int) -> list[int]:
    length = len(arr)
    offset %= length
    new_arr = [0] * length
    new_arr[offset:] = arr[:length - offset]
    new_arr[:offset] = arr[length - offset:]
    return new_arr