import copy
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

    # TODO test
    def kahn_algorithm(self):
        """
        An implementation of Kahn's algorithm for topological ordering of a
        graph.

        Returns
        -------
        list
            A topological ordering of the graph.
        """
        list_repr_graph = self.adjacency_list_representation
        indegrees = copy.deepcopy(list_repr_graph.indegrees)
        queue = np.where(np.asarray(indegrees) == 0)[0].tolist()
        topological_ordering = []

        while queue:

            current_node = queue.pop(0)
            topological_ordering.append(current_node)

            for neighbour in list_repr_graph.adjacency_lists[current_node]:
                indegrees[neighbour] -= 1
                if indegrees[neighbour] == 0:
                    queue.append(neighbour)

        return topological_ordering

    # TODO remove
    # def kahn_algorithm(self):
    #
    #     graph_for_sorting = self.to_adjacency_list_representation()
    #
    #     return graph_for_sorting.kahn_algorithm_topological_ordering()

    # TODO test
    def depth_first_search(self):
        """
        An implementation of the DFS-based (Depth First Search) algorithm for
        topological ordering of a graph. Note that it does not make sense to
        use this method if the graph is not in fact a DAG !

        Returns
        -------
        list
            A topological ordering of the graph.
        """
        list_repr_graph = self.adjacency_list_representation

        def rec_func(current_vertex, visited_vertices, stack):

            visited_vertices[current_vertex] = True

            for neighbour in list_repr_graph.adjacency_lists[current_vertex]:
                if not visited_vertices[neighbour]:
                    rec_func(current_vertex=neighbour,
                             visited_vertices=visited_vertices,
                             stack=stack)

            stack.append(current_vertex)

        visited_vertices = [False] * list_repr_graph.nb_vertices
        stack = []

        for i in range(list_repr_graph.nb_vertices):
            if not visited_vertices[i]:
                rec_func(current_vertex=i,
                         visited_vertices=visited_vertices,
                         stack=stack)

        topological_ordering = stack[::-1]

        return topological_ordering

    # TODO remove
    # def depth_first_search(self):
    #
    #     graph_for_sorting = self.to_adjacency_list_representation()
    #
    #     return graph_for_sorting.dfs_topological_ordering()

    # TODO document
    def compute_causal_order(self, method):

        if method == 'kahn':

            return self.kahn_algorithm()

        elif method == 'dfs':

            return self.depth_first_search()

        else:

            msg = "Method must be one of 'kahn' for Kahn's algorithm, or 'dfs' "
            msg += "for a depth-first search algorithm !"
            raise TopologicalOrderingMethodNotImplemented(msg)
