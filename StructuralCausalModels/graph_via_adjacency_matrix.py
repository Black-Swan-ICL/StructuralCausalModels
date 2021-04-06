import numpy as np


class InvalidAdjacencyMatrix(Exception):
    """Raised if the adjacency matrix does not contain only 0's and 1's.
    """
    pass


class GraphViaAdjacencyMatrix:
    """Implements a graph structure using an adjacency matrix representation.

    Parameters
    ----------
    adjacency_matrix : array_like
        The adjacency matrix of the graph.
    name : str, optional
        The name of the object created (default is '').

    Raises
    ------
    InvalidAdjacencyMatrix
        If the adjacency matrix provided does not contain only 0's and 1's.
    """

    def __init__(self, adjacency_matrix, name=''):

        if not GraphViaAdjacencyMatrix.validate_binary_matrix(adjacency_matrix):
            msg = 'Adjacency matrix provided not valid.'
            raise InvalidAdjacencyMatrix(msg)

        self.name = name
        self.adjacency_matrix = adjacency_matrix

    @staticmethod
    def validate_binary_matrix(matrix):
        """
        Checks that a matrix is an adjacency matrix (i.e. a square matrix
        containing only 0's and 1's).

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

    def __str__(self):
        """
        Returns a user-friendly string representation of the object.

        Returns
        -------
        str
            A user-friendly string representation of the object.
        """
        s = f"GraphViaAdjacencyMatrix '{self.name}', "
        s += f"adjacency matrix:\n{self.adjacency_matrix}"

        return s

    def __repr__(self):
        """
        Returns a string representation of the object from which it can be
        rebuilt.

        Returns
        -------
        str
            A string representation of the object from which it can be rebuilt.
        """
        s = f"GraphViaAdjacencyMatrix(name={repr(self.name)}, "
        s += f"adjacency_matrix=np.asarray("
        s += f"{np.array2string(self.adjacency_matrix, separator=',')}))"

        return s

    def __eq__(self, other):
        """
        Checks whether the object is equal to another GraphViaAdjacencyMatrix
        object. Two GraphViaAdjacencyMatrix objects are equal if they have the
        same adjacency matrix and the same names.

        Parameters
        ----------
        other : GraphViaAdjacencyMatrix
            The other GraphViaAdjacencyMatrix object.

        Returns
        -------
        bool
            Whether the two GraphViaAdjacencyMatrix objects are equal.
        """
        if not np.all(self.adjacency_matrix == other.adjacency_matrix):
            return False

        if self.name != other.name:
            return False

        return True
