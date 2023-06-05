
import operator
class SquareMatrix:
    def __init__(self, n):
        self.matrix = [[0 for i in range(n)] for k in range(n)]

    def initialize_with(self, l):
        self.matrix = l

    def print_matrix(self):
        for row in self.matrix:
            for element in row:
                print(f"{element}", end=" ")
            print()

    def multiply_by(self,const, vector):
        return (list(map (lambda n: const*n, vector)))

    def sub_vectors(self,v1,v2):
        return list(map(lambda x,y: (x-y),v1 ,v2))


    def det(self):

        for row_index in range(len(self.matrix) - 1):
            pivot =  row_index
            chosen_row = self.matrix[row_index]
            if chosen_row[pivot] != 0:
                for row_below in range(row_index+ 1, len(self.matrix)):
                    # Dividing the row by the leading coeffitient
                    subtract_from_matrix = self.matrix[row_below]
                    chosen_row = self.multiply_by(subtract_from_matrix[pivot]/chosen_row[pivot], chosen_row)
                    self.matrix[row_below] = self.sub_vectors(subtract_from_matrix, chosen_row)
            else:
                return 0
        # Now we have our matrix in the upper triangle form
        # The determinant is going to be just the product
        # of leading corefficients on the diagonal
        det = 1
        for i in range(len(self.matrix)):
            det *= self.matrix[i][i]
        return det

m1 = SquareMatrix(3)
m1.initialize_with([[1,2, 3],
                    [4,5,6],
                    [7,8,9]])
#m1.print_matrix()
det = m1.det()

print(det)







class Elimination:
    def __init__(self, matrix) -> None:
        self.num_unknowns = len(matrix)
        self.matrix = matrix



