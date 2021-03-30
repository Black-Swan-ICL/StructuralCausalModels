import numpy as np

from StructuralCausalModels.directed_graph import DirectedGraph
from StructuralCausalModels.graph import InvalidAdjacencyMatrix


class DirectedAcyclicGraph(DirectedGraph):

    def __init__(self, name, adjacency_matrix):

        if not DirectedAcyclicGraph.validate_dag_adjacency_matrix(
                adjacency_matrix):
            msg = 'Adjacency matrix provided not valid for a DAG.'
            raise InvalidAdjacencyMatrix(msg)

        super().__init__(name, adjacency_matrix)

    @staticmethod
    def validate_dag_adjacency_matrix(matrix, atol=1e-6):
        """
        Checks that a matrix is a valid adjacency matrix for a directed acyclic
        graph. Uses the characterisation of acyclicity established by D. Wei, T.
        Gao and Y. Yu in "DAGs with No Fears : A Closer Look at Continuous
        Optimization for Learning Bayesian Networks" (2020) : a directed graph is
        acyclic if and only if its adjacency matrix is nilpotent.

        Parameters
        ----------
        matrix : array_like
            The matrix to check.
        atol : float
            The absolute tolerance used to check that the eigenvalues are all equal
            to 0.

        Returns
        -------
        bool
            Whether the matrix to check is a valid adjacency matrix for a directed
            acyclic graph.
        """
        if not DirectedGraph.validate_directed_graph_adjacency_matrix(matrix):
            return False

        eigenvalues = np.linalg.eigvals(matrix)
        comparand = np.zeros_like(eigenvalues)

        return np.allclose(eigenvalues, comparand, atol=atol)
