import numpy as np

from StructuralCausalModels.graph import InvalidAdjacencyMatrix
from StructuralCausalModels.directed_graph import DirectedGraph


class TopologicalOrderingMethodNotImplemented(Exception):

    pass


class DirectedAcyclicGraph(DirectedGraph):

    def __init__(self, adjacency_matrix, name=''):

        if not DirectedAcyclicGraph.validate_dag_adjacency_matrix(
                adjacency_matrix):
            msg = 'Adjacency matrix provided not valid for a DAG.'
            raise InvalidAdjacencyMatrix(msg)

        super().__init__(name=name,
                         adjacency_matrix=adjacency_matrix)

    def kahn_algorithm(self):

        graph_for_sorting = self.to_adjacency_list_representation()

        return graph_for_sorting.kahn_algorithm_topological_ordering()

    def depth_first_search(self):

        graph_for_sorting = self.to_adjacency_list_representation()

        return graph_for_sorting.dfs_topological_ordering()

    def compute_causal_order(self, method):

        if method == 'kahn':

            return self.kahn_algorithm()

        elif method == 'dfs':

            return self.depth_first_search()

        else:

            msg = "Method must be one of 'kahn' for Kahn's algorithm, or 'dfs' "
            msg += "for a depth-first search algorithm !"
            raise TopologicalOrderingMethodNotImplemented(msg)

    @staticmethod
    def validate_dag_adjacency_matrix(matrix, atol=1e-6):
        """
        Checks that a matrix is a valid adjacency matrix for a directed acyclic
        graph. Uses the characterisation of acyclicity established by D. Wei, T.
        Gao and Y. Yu in "DAGs with No Fears : A Closer Look at Continuous
        Optimization for Learning Bayesian Networks" (2020) : a directed graph
        is acyclic if and only if its adjacency matrix is nilpotent.

        Parameters
        ----------
        matrix : array_like
            The matrix to check.
        atol : float
            The absolute tolerance used to check that the eigenvalues are all
            equal to 0.

        Returns
        -------
        bool
            Whether the matrix to check is a valid adjacency matrix for a
            directed acyclic graph.
        """
        if not DirectedGraph.validate_directed_graph_adjacency_matrix(matrix):
            return False

        eigenvalues = np.linalg.eigvals(matrix)
        comparand = np.zeros_like(eigenvalues)

        return np.allclose(eigenvalues, comparand, atol=atol)
