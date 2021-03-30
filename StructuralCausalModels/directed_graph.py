import numpy as np

from StructuralCausalModels.graph import Graph
from StructuralCausalModels.graph import InvalidAdjacencyMatrix


class DirectedGraph(Graph):

    def __init__(self, name, adjacency_matrix):

        if not DirectedGraph.validate_directed_graph_adjacency_matrix(
                adjacency_matrix):
            msg = 'Adjacency matrix provided not valid for a directed graph.'
            raise InvalidAdjacencyMatrix(msg)

        super().__init__(name, adjacency_matrix)

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
            Whether the matrix to check is a valid adjacency matrix for a directed
            graph.
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
