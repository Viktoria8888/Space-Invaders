import numpy as np
from sympy import *
import random


"""There seems to be a mix of languages here.
The code and the program are presented in English,
while the problem statements and occasionally the solutions are in Polish.
I have decided against translating everything into English.
This work is intended to serve as preparation for an algebra exam,
which will be conducted in Polish. An entire translation
could potentially lead to confusion.

Numpy and sympy modules are extensively used in data science and machine learning
Actually, thanks to those modules Python became so popular and frequently used in these domains
That is why in the code below I will be using those 2 modules to help me to solve some linear algebra problems
from the first part of the algebra exam
I used ChatGpt to guide me through numpy methods and math algorithms that
would be the most efficient to solve the problem
This time all the comments to the code were written by myself :) """
class UpgradedMatrix:
    def __init__(self, matrix):
        self.matrix = np.array(matrix, dtype=float)
        self.matrix_letters = np.array(matrix, dtype='object')#<-

        self.sympy_matrix = Matrix(self.matrix_letters)
        if self.matrix.shape[0] == self.matrix.shape[1]:
            self.determinant = self.sympy_matrix.det()

    def is_invertible(self):
        # A matrix is invertible iff its determinant is not zero
        return simplify(self.determinant) != 0

    def when_invertible(self, param):
        equation = Eq(self.determinant, 0)
        solution = solve(equation, param)
        return solution

    # Gram-Schmidt elimination
    def orthogonalization(self):
        self.matrix[0] = self.matrix[0] / np.linalg.norm(self.matrix[0])
        n = self.matrix.shape[0]
        for i in range(1, n):
            orthogonal_sum = sum(np.dot(self.matrix[i], self.matrix[j]) * self.matrix[j] for j in range(i))
            self.matrix[i] -= orthogonal_sum
            if np.dot(self.matrix[i], self.matrix[i]) > 1e-10:  # Check for non-zero vector
                self.matrix[i] = self.matrix[i] / np.linalg.norm(self.matrix[i])
            else:
                return i # index of the linearly dependent vector
                # Although I don't take into the account that
                # there are more linearly dependent vectors

        return self.matrix

    # If vectors are linearly independent
    # A common way to check it is by using Gaussian Elimination and verifying
    # if the rank of the matrix created by those #vectors is equal to the rank
    # of the matrix after Gaussian Elimination.
    # T he rank of a matrix is the maximum number of linearly independent rows (columns).
    # I will use numpy.linalg.matrix_rank() to compute the rank
    # This method uses Singular Value Decomposition to compute the matrix rank.

    def if_linearly_independent(self):
        rank = np.linalg.matrix_rank(self.matrix)
        return rank==len(self.matrix)

    def return_lin_dependent(self):
        func_call = self.orthogonalization()
        if type(func_call) == int:
            return func_call
        else:
            return False #if the set is linearly independent

    # To expand into the basis first we have to remove the independent vectors
    # We can do it by orthogonalization to see what vectors end up as a zero vector.
    # This function will not be used to show the solution to the user,
    # because of the results are not quite readible.
    def expand_into_basis(self):
        # Remove any linearly dependent vectors
        if not self.if_linearly_independent():
            i = self.return_lin_dependent()
            self.matrix = np.delete(self.matrix, i, axis=0)


        n = self.matrix.shape[1]
        # Current number of basis vectors
        m = self.matrix.shape[0]

        # add necessary standard basis vectors
        for i in range(n):
            e = np.zeros((1, n))
            e[0][i] = 1
            # Check if the new vector e is linearly independent of the existing vectors
            if np.linalg.matrix_rank(np.vstack((self.matrix, e))) > np.linalg.matrix_rank(self.matrix):
                self.matrix = np.vstack((self.matrix, e))

        return self.matrix

    # if the given matrix is positive definite
    # We have to check first if it's symmetric, or A^T = T
    def is_symmetric(self):
        return np.array_equal(self.matrix, self.matrix.T)
    # There are two common ways to check if the matrix is posite definite
    # 1) Sylvester's criterion (all the determinants of minors are > 0)
    # 2) Cholevsky's decomposition
    # 3) All the eigenvalues are positive
    # Use the third approach because Cholesky method doesn't take into account if
    # the matrix is semi-definite (or when one of the determinants of a minor is equal to 0)
    def if_positive_definite(self):
        if self.is_symmetric():
            eigenvalues = np.linalg.eigvalsh(self.matrix)
            return np.all(eigenvalues > 0)
        return False


def solve_4():
    x = symbols('x')
    m = UpgradedMatrix([[1,x,1,x],
                [1,1,1,1],
                [0,0,x,1],
                [1,0,0,1]])
    solution_real = m.when_invertible(x)
    return set(map (lambda x: x %2, solution_real))




def solve_5(): # Will show the picture with the solution, because the result numbers
    vectors_in_problem = [[4,4,-2,0],[1,4,1,0], [5,-4,-7,1]]
    s4 = UpgradedMatrix(vectors_in_problem)
    return s4.orthogonalization().tolist()



def solve_6():
    np.set_printoptions(precision=3)
    m1 = UpgradedMatrix([[1,1,0],[0,1,1],[1,1,1],[1,0,1]])
    print(m1.expand_into_basis())
    m2 = UpgradedMatrix([[0,1,2],[1,1,1],[1,1,1]])
    m3 = UpgradedMatrix([[1,0,1,0],[1,2,0,1],[0,2,1,1],[0,0,1,1]])
    #print(m3.if_linearly_independent())
    m4 = UpgradedMatrix([[1,0,1,0],[0,2,0,2],[0,0,2,1]])
    #print(m1.expand_into_basis())


def express_in(basis,vector):
    basis,vector = np.array(basis).T, np.array(vector).T
    res = np.linalg.solve(basis,vector)
    res = np.round(res).astype(int)
    return res

def solve_7():
    B = [[1,2,3],[0,1,2],[0,0,1]]
    v1 = [1,0,0]
    v2 = [0,1,0]
    v3 = [0,0,1]
    v4  = [7,3,2]
    vn = [v1,v2,v3,v4]
    res = {}
    for i in vn:
        # Converting lists to tuples because the keys
        # in dictionary should be immutable
        res[tuple(i)] = express_in(B,i).tolist()
    return res

# S9: Form a change of basis matrix.
# https://math.stackexchange.com/questions/628061/how-to-construct-change-of-basis-matrix


def solve_8():
    b1 = [[1,1,1],[1,1,0],[1,0,0]]
    b2 = [[1,1,1],[1,1,0],[1,0,0]]
    b3 = [[1,1,-1],[1,-1,1],[-1,1,1]]
    def transition_matrix(old_basis,new_basis):
        old_basis = np.array(old_basis).T
        new_basis = np.array(new_basis).T
        change_of_basis_matrix = np.linalg.inv(new_basis) @ old_basis
        return change_of_basis_matrix

#Problem1:
#Podaj bazy obrazu i jądra przekształcenia liniowego FM : R5 → R3 zadanego przez macierz M :
def solve_1():
    def image_basis(matrix):
        # Compute the Reduced Row Echelon Form (RREF) and the pivot columns
        rref, pivot_columns = Matrix(matrix.T).rref()

        # Select pivot columns (non-zerio) from original matrix
        basis = matrix[:, pivot_columns]

        return basis

    def kernel_basis(matrix):
        m = Matrix(matrix)
        basis = m.nullspace()
        nullspace_basis = [list(vector) for vector in basis]
        return nullspace_basis



    A = np.array([[-1, 4, 3], [1, 5, 3], [1, -1, -1],[-1,-2,-1],[2,7,4]]).T
    res = {}
    res["image"] = "{"+', '.join([str(elem) + "^T" for elem in image_basis(A).T]) + "}"
    res["kernel"] = "{"+', '.join([str(elem) + "^T" for elem in kernel_basis(A)]) + "}"
    return res



# Problem2:
# Very common on the exam
# For S = LIN({v1,..vn}) and T = LIN({w1,..wn})
# Find dim(S+T) and dim(S ∩ T)
# We know that LIN(S U T) = LIN(S) + LIN(T) (was proved)
def solve_2(self):
    v_S = Matrix([[3,0,3,3,2,0], [3,1,3,2,3,1]])
    v_T = Matrix([[1,1,1,0,3,1],[0,3,0,-3,-1,3]])
    # dimension of S and T
    dim_S = v_S.rank()
    dim_T = v_T.rank()
    v_S_T = v_S.row_join(v_T)
    dim_S_plus_T = v_S_T.rank()
    # Using formula: dim(S + T) = dim(S) + dim(T) - dim(S ∩ T)
    # dim(S ∩ T) = dim(S) + dim(T) - dim(S + T)
    dim_S_inter_T = dim_S + dim_T - dim_S_plus_T
    return [dim_S_plus_T, dim_S_inter_T]

def solve_3():
    m1 = UpgradedMatrix([[1,2,0],[-2,2,0],[0,0,1]])
    m2 = UpgradedMatrix([[2,2,0],[2,2,0],[0,0,1]])
    m3 = UpgradedMatrix([[6,2,4],[2,1,1],[4,1,5]])
    m4 = UpgradedMatrix([[6,7,3,3],[7,15,7,3],[3,7,11,1],[3,3,1,2]])

    matrices = [m1, m2, m3, m4] # Create a list of matrices
    res = [m.if_positive_definite() for m in matrices] # Check if each matrix is positive definite

    return res


def solve_problem(num):
    if num == 1:
        solve_1() # The output is the dictionaty with strings
    elif num == 2:
        solve_2()
    elif num == 3:
        solve_3()
    elif num == 4:
        solve_4()
    elif num == 5:
        solve_5()
    elif num == 6:
        solve_6()
    elif num == 7:
        solve_7() # Will show the picture
    elif num == 8:
        solve_8()





