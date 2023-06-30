import numpy as np


class Cube3x3:

    GOAL = np.array([0, 0, 0, 0, 0, 0, 0, 0,
                     1, 1, 1, 1, 1, 1, 1, 1,
                     2, 2, 2, 2, 2, 2, 2, 2,
                     3, 3, 3, 3, 3, 3, 3, 3,
                     4, 4, 4, 4, 4, 4, 4, 4,
                     5, 5, 5, 5, 5, 5, 5, 5])
    POS_SIZE = 48
    ADJ_COUNT = 18
    
    def cleanstr(position):
        pos_str  = f"        {position[0]} {position[1]} {position[2]}\n"
        pos_str += f"        {position[7]} 0 {position[3]}\n"
        pos_str += f"        {position[6]} {position[5]} {position[4]}\n\n"
        pos_str += f"{position[16]} {position[17]} {position[18]}   "
        pos_str += f"{position[8]} {position[9]} {position[10]}   "
        pos_str += f"{position[32]} {position[33]} {position[34]}   "
        pos_str += f"{position[24]} {position[25]} {position[26]}\n"
        pos_str += f"{position[23]} 2 {position[19]}   "
        pos_str += f"{position[15]} 1 {position[11]}   "
        pos_str += f"{position[39]} 4 {position[35]}   "
        pos_str += f"{position[31]} 3 {position[27]}\n"
        pos_str += f"{position[22]} {position[21]} {position[20]}   "
        pos_str += f"{position[14]} {position[13]} {position[12]}   "
        pos_str += f"{position[38]} {position[37]} {position[36]}   "
        pos_str += f"{position[30]} {position[29]} {position[28]}\n\n"
        pos_str += f"        {position[40]} {position[41]} {position[42]}\n"
        pos_str += f"        {position[47]} 5 {position[43]}\n"
        pos_str += f"        {position[46]} {position[45]} {position[44]}\n"
        return pos_str
    
    def move(position, face, amount):
        new_pos = position.copy()

        # Move appropriate face
        new_pos[8*face : 8*face+8] = np.roll(position[8*face : 8*face+8], 2 * amount)

        # Move appropriate edges
        edges = np.zeros(12)
        if face == 0:
            edges[0:3] = position[8:11]
            edges[3:6] = position[32:35]
            edges[6:9] = position[24:27]
            edges[9:12] = position[16:19]
            edges = np.roll(edges, -3 * amount)
            new_pos[8:11] = edges[0:3]
            new_pos[32:35] = edges[3:6]
            new_pos[24:27] = edges[6:9]
            new_pos[16:19] = edges[9:12]
        elif face == 1:
            edges[0:3] = position[4:7]
            edges[3:6] = position[18:21]
            edges[6:9] = position[40:43]
            edges[9] = position[38]
            edges[10] = position[39]
            edges[11] = position[32]
            edges = np.roll(edges, -3 * amount)
            new_pos[4:7] = edges[0:3]
            new_pos[18:21] = edges[3:6]
            new_pos[40:43] = edges[6:9]
            new_pos[38] = edges[9]
            new_pos[39] = edges[10]
            new_pos[32] = edges[11]
        elif face == 2:
            edges[0] = position[6]
            edges[1] = position[7]
            edges[2] = position[0]
            edges[3:6] = position[26:29]
            edges[6] = position[46]
            edges[7] = position[47]
            edges[8] = position[40]
            edges[9] = position[14]
            edges[10] = position[15]
            edges[11] = position[8]
            edges = np.roll(edges, -3 * amount)
            new_pos[6] = edges[0]
            new_pos[7] = edges[1]
            new_pos[0] = edges[2]
            new_pos[26:29] = edges[3:6]
            new_pos[46] = edges[6]
            new_pos[47] = edges[7]
            new_pos[40] = edges[8]
            new_pos[14] = edges[9]
            new_pos[15] = edges[10]
            new_pos[8] = edges[11]
        elif face == 3:
            edges[0:3] = position[0:3]
            edges[3:6] = position[34:37]
            edges[6:9] = position[44:47]
            edges[9] = position[22]
            edges[10] = position[23]
            edges[11] = position[16]
            edges = np.roll(edges, -3 * amount)
            new_pos[0:3] = edges[0:3]
            new_pos[34:37] = edges[3:6]
            new_pos[44:47] = edges[6:9]
            new_pos[22] = edges[9]
            new_pos[23] = edges[10]
            new_pos[16] = edges[11]
        elif face == 4:
            edges[0:3] = position[2:5]
            edges[3:6] = position[10:13]
            edges[6:9] = position[42:45]
            edges[9] = position[30]
            edges[10] = position[31]
            edges[11] = position[24]
            edges = np.roll(edges, -3 * amount)
            new_pos[2:5] = edges[0:3]
            new_pos[10:13] = edges[3:6]
            new_pos[42:45] = edges[6:9]
            new_pos[30] = edges[9]
            new_pos[31] = edges[10]
            new_pos[24] = edges[11]
        elif face == 5:
            edges[0:3] = position[12:15]
            edges[3:6] = position[20:23]
            edges[6:9] = position[28:31]
            edges[9:12] = position[36:39]
            edges = np.roll(edges, -3 * amount)
            new_pos[12:15] = edges[0:3]
            new_pos[20:23] = edges[3:6]
            new_pos[28:31] = edges[6:9]
            new_pos[36:39] = edges[9:12]
        
        return new_pos
    
    def adjacents(position):
        adj = np.empty((18, len(Cube3x3.GOAL)))
        for face in range(6):
            for amount in range(1, 4):
                adj[3 * face + amount - 1] = Cube3x3.move(position, face, amount)
        return adj