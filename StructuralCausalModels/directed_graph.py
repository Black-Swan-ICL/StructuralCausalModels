import numpy as np

from StructuralCausalModels.graph import Graph
from StructuralCausalModels.graph_via_adjacency_matrix import \
    InvalidAdjacencyMatrix


class DirectedGraph(Graph):
    """A class to represent directed graphs.

    A DirectedGraph object is a representation of a directed graph. It is
    defined by the adjacency matrix of the graph ; validation will be performed
    to check that the graph defined is directed. An exception will be raised
    otherwise.

    Parameters
    ----------
    adjacency_matrix : array_like
        The adjacency matrix of the graph.
    name : str, optional
        The name of the object created (default is '').

    Raises
    ------
    InvalidAdjacencyMatrix
        If the adjacency matrix does not define a directed graph.
    """

    def __init__(self, adjacency_matrix, name=''):

        if not DirectedGraph.validate_directed_graph_adjacency_matrix(
                adjacency_matrix):
            msg = 'Adjacency matrix provided not valid for a directed graph.'
            raise InvalidAdjacencyMatrix(msg)

        super().__init__(name=name,
                         adjacency_matrix=adjacency_matrix)

    @staticmethod
    def validate_directed_graph_adjacency_matrix(matrix):
        """
        Checks that a matrix is a valid adjacency matrix for a directed graph.

        Parameters
        ----------
        matrix : array_like
            The matrix to check.

        Returns
        -------
        bool
            Whether the matrix to check is a valid adjacency matrix for a
            directed graph.
        """
        if not Graph.validate_binary_matrix(matrix):
            return False

        # Check that there are no self-loops
        no_self_loops = np.asarray([matrix[i, i] == 0 for i in
                                    range(matrix.shape[0])])
        if not np.all(no_self_loops):
            return False

        # Check that there are no undirected edges
        for i in range(matrix.shape[0]):
            for j in range(i):
                if matrix[i, j] == 1 and matrix[j, i] == 1:
                    return False

        return True
