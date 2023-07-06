from abc import ABC, abstractmethod
import numpy as np


class Puzzle(ABC):
    
    EXPANSIONS = ()
    MOVE_INDICES = {}
    BACKTRACKS = ()
    TRANSPOSABLES = ()

    @classmethod
    @abstractmethod
    def init(cls) -> None: pass

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

    @classmethod
    @abstractmethod
    def move(cls, position: np.ndarray, move_index: int) -> list[int]: pass

    @classmethod
    def adjacents(cls, position: np.ndarray, allowed_moves: list[int]) -> list[int]:
        return [cls.move(position, move) for move in allowed_moves]


class Cube(Puzzle):     

    EDGES = ()
    NEW_EDGES = ()

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
    

class Cube3(Cube):
    
    @classmethod
    def init(cls) -> None:
        cls.EXPANSIONS = tuple([(move // 3, move % 3 + 1) for move in range(cls.ADJACENT_COUNT)])

        cls.MOVE_INDICES = {}
        for face in range(6):
            for amount in (1, 2, 3):
                cls.MOVE_INDICES[(face, amount)] = 3 * face + amount - 1
        
        cls.BACKTRACKS = []
        for move_index in range(cls.ADJACENT_COUNT):
            face, _ = cls.EXPANSIONS[move_index]
            backs = [cls.MOVE_INDICES[(face, amount)] for amount in (1, 2, 3)]
            cls.BACKTRACKS.append(tuple(backs))
        cls.BACKTRACKS = tuple(cls.BACKTRACKS)

        cls.TRANSPOSABLES = []
        for move_index in range(cls.ADJACENT_COUNT):
            face, _ = cls.EXPANSIONS[move_index]
            opposite_face = {0:5, 1:3, 2:4, 3:1, 4:2, 5:0}[face]
            trans = [cls.MOVE_INDICES[(opposite_face, amount)] for amount in (1, 2, 3)]
            cls.TRANSPOSABLES.append(tuple(trans))
        cls.TRANSPOSABLES = tuple(cls.TRANSPOSABLES)

        cls.EDGES = []
        cls.NEW_EDGES = []
        for move_index in range(cls.ADJACENT_COUNT):
            face, amount = cls.EXPANSIONS[move_index]
            edges = ((8, 9, 10, 32, 33, 34, 24, 25, 26, 16, 17, 18),
                     (4, 5, 6, 18, 19, 20, 40, 41, 42, 38, 39, 32),
                     (6, 7, 0, 26, 27, 28, 46, 47, 40, 14, 15, 8),
                     (0, 1, 2, 34, 35, 36, 44, 45, 46, 22, 23, 16),
                     (2, 3, 4, 10, 11, 12, 42, 43, 44, 30, 31, 24),
                     (12, 13, 14, 20, 21, 22, 28, 29, 30, 36, 37, 38))
            cls.EDGES.append(edges[face])
            cls.NEW_EDGES.append(tuple(roll(cls.EDGES[move_index], -3 * amount)))
        cls.EDGES = tuple(cls.EDGES)
        cls.NEW_EDGES = tuple(cls.NEW_EDGES)

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

    @classmethod
    def move(cls, position: np.ndarray, move_index: int) -> list[int]:
        position = list(position)
        new_pos = position.copy()
        face, amount = cls.EXPANSIONS[move_index]

        # Move the appropriate face
        new_pos[8*face : 8*face+8] = roll(position[8*face : 8*face+8], 2*amount)

        # Move the appropriate edges
        edges = cls.EDGES[move_index]
        new_edges = cls.NEW_EDGES[move_index]
        for edge, new_edge in zip(edges, new_edges):
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