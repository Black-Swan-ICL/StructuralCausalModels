import copy
import numpy as np


class InvalidAdjacencyMatrix(Exception):
    pass


# TODO to string method
class Graph:
    """
    Implements a graph structure using an adjacency matrix representation.
    """

    def __init__(self, adjacency_matrix, name=''):

        if not Graph.validate_binary_matrix(adjacency_matrix):
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

    # TODO test
    # TODO document
    def to_adjacency_list_representation(self):

        nb_vertices = self.adjacency_matrix.shape[0]

        # Build the adjacency lists
        adjacency_lists = []
        for i in range(nb_vertices):
            adjacency_lists.append(
                np.where(self.adjacency_matrix[i, :] != 0)[0].tolist()
            )

        return AlternativeGraph(name=self.name,
                                nb_vertices=nb_vertices,
                                adjacency_lists=adjacency_lists)


# TODO to string method
# TODO validate inputs e.g. as many vertices as nb elts in adjacency_lists
class AlternativeGraph:
    """
    Implements a graph structure representing an adjacency list representation.
    """

    def __init__(self, nb_vertices, adjacency_lists, name=''):
        self.name = name
        self.nb_vertices = nb_vertices
        self.adjacency_lists = adjacency_lists
        self.indegrees = []
        for i in range(self.nb_vertices):
            count = sum([int(i in adj_l) for adj_l in self.adjacency_lists])
            self.indegrees.append(count)

    # TODO test
    # TODO document
    def to_adjacency_matrix_representation(self):

        # Build the adjacency matrix
        adjacency_matrix = np.zeros((self.nb_vertices, self.nb_vertices))
        for i in range(self.nb_vertices):
            adjacency_matrix[i, self.adjacency_lists[i]] = 1

        return Graph(name=self.name,
                     adjacency_matrix=adjacency_matrix)

    # TODO test
    # TODO document
    def kahn_algorithm_topological_sorting(self):
        """
        Iterative method
        """
        queue = np.where(np.asarray(self.indegrees) == 0)[0].tolist()
        topological_ordering = []
        indegrees = copy.deepcopy(self.indegrees)

        while queue:

            current_node = queue.pop(0)
            topological_ordering.append(current_node)

            for neighbour in self.adjacency_lists[current_node]:
                indegrees[neighbour] -= 1
                if indegrees[neighbour] == 0:
                    queue.append(neighbour)

        return topological_ordering

    # TODO test
    # TODO document
    def dfs_topological_sorting(self):
        """
        Recursive method.
        """
        def rec_func(current_vertex, visited_vertices, stack):

            visited_vertices[current_vertex] = True

            for neighbour in self.adjacency_lists[current_vertex]:
                if not visited_vertices[neighbour]:
                    rec_func(current_vertex=neighbour,
                             visited_vertices=visited_vertices,
                             stack=stack)

            stack.append(current_vertex)

        visited_vertices = [False] * self.nb_vertices
        stack = []

        for i in range(self.nb_vertices):
            if not visited_vertices[i]:
                rec_func(current_vertex=i,
                         visited_vertices=visited_vertices,
                         stack=stack)

        topological_ordering = stack[::-1]

        return topological_ordering

    # TODO implement
    # TODO document
    # TODO test
    def compute_all_topological_ordering(self):

        return []


if __name__ == '__main__':

    # mymat = np.asarray([
    #     [0, 1, 1, 1],
    #     [0, 0, 1, 0],
    #     [0, 0, 0, 0],
    #     [0, 1, 1, 0]
    # ])
    mymat = np.asarray([
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0]
    ])

    test_graph = Graph(name='test', adjacency_matrix=mymat)

    transformed = test_graph.to_adjacency_list_representation()
    print(transformed.nb_vertices)
    print(transformed.adjacency_lists)
    print(transformed.indegrees)
    print(f"Causal order : {transformed.dfs_topological_sorting()}")
    print(f"Kahn : {transformed.kahn_algorithm_topological_sorting()}")

    retransformed = transformed.to_adjacency_matrix_representation()
    print(retransformed.adjacency_matrix)