import copy
import numpy as np

from StructuralCausalModels.graph_via_adjacency_matrix import \
    InvalidAdjacencyMatrix
from StructuralCausalModels.directed_graph import DirectedGraph


class TopologicalOrderingMethodNotImplemented(Exception):

    pass


class InvalidOrdering(Exception):

    pass


# TODO add a method to compute all topological orderings ?
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

    # TODO to correct, does not work !
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

        def rec_func(current_vertex, visited_vertices, acc):

            visited_vertices[current_vertex] = True

            for neighbour in list_repr_graph.adjacency_lists[current_vertex]:
                if not visited_vertices[neighbour]:
                    rec_func(current_vertex=neighbour,
                             visited_vertices=visited_vertices,
                             acc=acc)

            acc.append(current_vertex)

        already_visited_vertices = [False] * list_repr_graph.nb_vertices
        stack = []

        for i in range(list_repr_graph.nb_vertices):
            if not already_visited_vertices[i]:
                rec_func(current_vertex=i,
                         visited_vertices=already_visited_vertices,
                         acc=stack)

        topological_ordering = stack[::-1]

        return topological_ordering

    def compute_causal_order(self, method):
        """
        Computes a causal order of the DAG using the method chosen by the user.

        Parameters
        ----------
        method : str
            The method to use to compute the causal order.

        Returns
        -------
        list
            A causal order of the DAG.

        Raises
        ------
        TopologicalOrderingMethodNotImplemented
            If the method chosen by the usr is not implemented.
        """
        if method == 'kahn':

            return self.kahn_algorithm()

        # TODO uncomment when dfs works
        # elif method == 'dfs':
        #
        #     return self.depth_first_search()

        else:

            msg = "Method must be one of 'kahn' for Kahn's algorithm, or 'dfs' "
            msg += "for a depth-first search algorithm !"
            raise TopologicalOrderingMethodNotImplemented(msg)

    def check_topological_ordering(self, ordering):
        """
        Checks whether an ordering is a correct topological ordering for the
        graph.

        Parameters
        ----------
        ordering : list
            The candidate ordering.

        Returns
        -------
        bool
            Whether the ordering is a correct topological ordering for the
            graph.

        Raises
        ------
        InvalidOrdering
            If the ordering passed is not a valid ordering for the graph.
        """
        list_repr_graph = self.adjacency_list_representation

        if set(ordering) != set(range(list_repr_graph.nb_vertices)):
            msg = "Ordering provided is not a valid ordering for the graph !"
            raise InvalidOrdering(msg)

        # Build a "look-up table" of the nodes and their indices
        index_lookup = dict()
        for i in range(list_repr_graph.nb_vertices):
            index_lookup[i] = ordering.index(i)

        # Use the definition of a topological ordering
        for i in range(len(list_repr_graph.adjacency_lists)):
            parent = i
            children = list_repr_graph.adjacency_lists[parent]
            for child in children:
                if index_lookup[child] <= index_lookup[parent]:
                    return False
                else:
                    pass

        return True

    @staticmethod
    def causal_order_to_dag(causal_order):
        """
        Generates the maximally connected DAG that is compatible with the causal
        order provided i.e. for all j such that j > i in the causal order, there
        will be an edge from X_i to X_j in the DAG (i.e. there will be a 1 in
        position [i, j] in the DAG's adjacency matrix).

        Parameters
        ----------
        causal_order : array_like
            The causal order.

        Returns
        -------
        DirectedAcyclicGraph
            The maximally connected DAG compatible with the causal order.
        """
        m = len(causal_order)
        adjacency_matrix = np.zeros((m, m))

        for i in range(m):
            for j in range(i+1, m):
                adjacency_matrix[causal_order[i], causal_order[j]] = 1

        dag = DirectedAcyclicGraph(adjacency_matrix=adjacency_matrix)

        return dag
