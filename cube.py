import numpy as np

class Cube:

    def __init__(self):
        self.position = np.array([0, 0, 0, 0, 0, 0, 0, 0,
                                  1, 1, 1, 1, 1, 1, 1, 1,
                                  2, 2, 2, 2, 2, 2, 2, 2,
                                  3, 3, 3, 3, 3, 3, 3, 3,
                                  4, 4, 4, 4, 4, 4, 4, 4,
                                  5, 5, 5, 5, 5, 5, 5, 5])
        
    def __init__(self, position):
        self.position = position.copy()

    def __eq__(self, other):
        if not isinstance(other, Cube):
            return False
        return self.position == other.position
    
    def __str__(self):
        pos_str  = f"        {self.position[0]} {self.position[1]} {self.position[2]}\n"
        pos_str += f"        {self.position[7]} 0 {self.position[3]}\n"
        pos_str += f"        {self.position[6]} {self.position[5]} {self.position[4]}\n\n"
        pos_str += f"{self.position[16]} {self.position[17]} {self.position[18]}   "
        pos_str += f"{self.position[8]} {self.position[9]} {self.position[10]}   "
        pos_str += f"{self.position[32]} {self.position[33]} {self.position[34]}   "
        pos_str += f"{self.position[24]} {self.position[25]} {self.position[26]}\n"
        pos_str += f"{self.position[23]} 2 {self.position[19]}   "
        pos_str += f"{self.position[15]} 1 {self.position[11]}   "
        pos_str += f"{self.position[39]} 4 {self.position[35]}   "
        pos_str += f"{self.position[31]} 3 {self.position[27]}\n"
        pos_str += f"{self.position[22]} {self.position[21]} {self.position[20]}   "
        pos_str += f"{self.position[14]} {self.position[13]} {self.position[12]}   "
        pos_str += f"{self.position[38]} {self.position[37]} {self.position[36]}   "
        pos_str += f"{self.position[30]} {self.position[29]} {self.position[28]}\n\n"
        pos_str += f"        {self.position[40]} {self.position[41]} {self.position[42]}\n"
        pos_str += f"        {self.position[47]} 5 {self.position[43]}\n"
        pos_str += f"        {self.position[46]} {self.position[45]} {self.position[44]}"
        return pos_str
        '''
                0 0 0
                0 0 0
                0 0 0

        2 2 2   1 1 1   4 4 4   3 3 3
        2 2 2   1 1 1   4 4 4   3 3 3
        2 2 2   1 1 1   4 4 4   3 3 3
               
                5 5 5
                5 5 5
                5 5 5
        
        '''
    
    def move(self, face, amount):
        new_pos = self.position.copy()

        # Move appropriate face
        new_pos[8*face : 8*face+8] = np.roll(self.position[8*face : 8*face+8], 2 * amount)

        # Move appropriate edges
        edges = np.zeros(12)
        if face == 0:
            edges[0:3] = self.position[8:11]
            edges[3:6] = self.position[16:19]
            edges[6:9] = self.position[24:27]
            edges[9:12] = self.position[32:35]
            edges = np.roll(edges, -3 * amount)
            new_pos[8:11] = edges[0:3]
            new_pos[16:19] = edges[3:6]
            new_pos[24:27] = edges[6:9]
            new_pos[32:35] = edges[9:12]
        elif face == 1:
            edges[0:3] = self.position[4:7]
            edges[3:6] = self.position[18:21]
            edges[6:9] = self.position[40:43]
            edges[9] = self.position[38]
            edges[10] = self.position[39]
            edges[11] = self.position[32]
            edges = np.roll(edges, -3 * amount)
            new_pos[4:7] = edges[0:3]
            new_pos[18:21] = edges[3:6]
            new_pos[40:43] = edges[6:9]
            new_pos[38] = edges[9]
            new_pos[39] = edges[10]
            new_pos[32] = edges[11]
        elif face == 2:
            edges[0] = self.position[6]
            edges[1] = self.position[7]
            edges[2] = self.position[0]
            edges[3:6] = self.position[26:29]
            edges[6] = self.position[46]
            edges[7] = self.position[47]
            edges[8] = self.position[40]
            edges[9] = self.position[14]
            edges[10] = self.position[15]
            edges[11] = self.position[8]
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
            edges[0:3] = self.position[0:3]
            edges[3:6] = self.position[34:37]
            edges[6:9] = self.position[44:47]
            edges[9] = self.position[22]
            edges[10] = self.position[23]
            edges[11] = self.position[16]
            edges = np.roll(edges, -3 * amount)
            new_pos[0:3] = edges[0:3]
            new_pos[34:37] = edges[3:6]
            new_pos[44:47] = edges[6:9]
            new_pos[22] = edges[9]
            new_pos[23] = edges[10]
            new_pos[16] = edges[11]
        elif face == 4:
            edges[0:3] = self.position[2:5]
            edges[3:6] = self.position[10:13]
            edges[6:9] = self.position[42:45]
            edges[9] = self.position[30]
            edges[10] = self.position[31]
            edges[11] = self.position[24]
            edges = np.roll(edges, -3 * amount)
            new_pos[2:5] = edges[0:3]
            new_pos[10:13] = edges[3:6]
            new_pos[42:45] = edges[6:9]
            new_pos[30] = edges[9]
            new_pos[31] = edges[10]
            new_pos[24] = edges[11]
        elif face == 5:
            edges[0:3] = self.position[12:15]
            edges[3:6] = self.position[20:23]
            edges[6:9] = self.position[28:31]
            edges[9:12] = self.position[36:39]
            edges = np.roll(edges, -3 * amount)
            new_pos[12:15] = edges[0:3]
            new_pos[20:23] = edges[3:6]
            new_pos[28:31] = edges[6:9]
            new_pos[36:39] = edges[9:12]
        
        self.position = new_pos
