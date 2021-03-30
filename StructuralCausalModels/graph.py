import numpy as np


class InvalidAdjacencyMatrix(Exception):
    pass


class Graph:

    def __init__(self, name, adjacency_matrix):

        if not Graph.validate_binary_matrix(adjacency_matrix):
            msg = 'Adjacency matrix provided not valid.'
            raise InvalidAdjacencyMatrix(msg)

        self.name = name
        self.adjacency_matrix = adjacency_matrix

    @staticmethod
    def validate_binary_matrix(matrix):
        """
        Checks that a matrix is an adjacency matrix (i.e. a square matrix containing
        only 0's and 1's).

        Parameters
        ----------
        matrix : array_like
            The matrix to check.

        Returns
        -------
        bool
            Whether the matrix is a valid adjacency matrix.
        """
        if len(matrix.shape) != 2:
            return False

        if matrix.shape[0] != matrix.shape[1]:
            return False

        if not np.all(np.logical_or(matrix == 1, matrix == 0)):
            return False

        return True
# def validate_binary_matrix(matrix):
#     """
#     Checks that a matrix is an adjacency matrix (i.e. a square matrix containing
#     only 0's and 1's).
#
#     Parameters
#     ----------
#     matrix : array_like
#         The matrix to check.
#
#     Returns
#     -------
#     bool
#         Whether the matrix is a valid adjacency matrix.
#     """
#     if len(matrix.shape) != 2:
#
#         return False
#
#     if matrix.shape[0] != matrix.shape[1]:
#
#         return False
#
#     if not np.all(np.logical_or(matrix == 1, matrix == 0)):
#
#         return False
#
#     return True