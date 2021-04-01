import copy
import numpy as np


class InvalidAdjacencyMatrix(Exception):
    pass


class Graph:
    """
    Implements a graph structure using an adjacency matrix representation.
    """

    # TODO test
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
    def to_adjacency_list_representation(self):
        """
        Returns an AlternativeGraph object which is equivalent to the Graph
        object.

        Returns
        -------
        AlternativeGraph
            The equivalent adjacency list based representation of the graph.
        """
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

    def __str__(self):
        """
        Returns a user-friendly string representation of the object.

        Returns
        -------
        str
            A user-friendly string representation of the object.
        """
        s = f"Graph '{self.name}', adjacency matrix:\n{self.adjacency_matrix}"

        return s

    # TODO test that with eval can reconstitute the object
    def __repr__(self):
        """
        Returns a string representation of the object from which it can be
        rebuilt.

        Returns
        -------
        str
            A string representation of the object from which it can be rebuilt.
        """
        s = f"Graph(name={repr(self.name)}, adjacency_matrix=np.asarray("
        s += f"{np.array2string(self.adjacency_matrix, separator=',')}))"

        return s

    def __eq__(self, other):
        """
        Checks whether the object is equal to another Graph object. Two Graph
        objects are equal if they have the same adjacency matrix and the same
        names.

        Parameters
        ----------
        other : Graph
            The other Graph object.

        Returns
        -------
        bool
            Whether the two Graph objects are equal.
        """
        if not np.all(self.adjacency_matrix == other.adjacency_matrix):
            return False

        if self.name != other.name:
            return False

        return True


class InvalidAdjacencyLists(Exception):
    pass


# TODO implement a method to find all the topological orderings ?
class AlternativeGraph:
    """
    Implements a graph structure representing an adjacency list representation.
    """

    # TODO test
    def __init__(self, nb_vertices, adjacency_lists, name=''):

        if not len(adjacency_lists) == nb_vertices:
            msg = 'There should be as many adjacency lists as vertices !'
            raise InvalidAdjacencyLists(msg)

        self.name = name
        self.nb_vertices = nb_vertices
        self.adjacency_lists = adjacency_lists
        self.indegrees = []
        for i in range(self.nb_vertices):
            count = sum([int(i in adj_l) for adj_l in self.adjacency_lists])
            self.indegrees.append(count)

    # TODO test
    def to_adjacency_matrix_representation(self):
        """
        Returns a Graph object which is equivalent to the AlternativeGraph
        object.

        Returns
        -------
        Graph
            The equivalent adjacency matrix based representation of the graph.
        """

        # Build the adjacency matrix
        adjacency_matrix = np.zeros((self.nb_vertices, self.nb_vertices))
        for i in range(self.nb_vertices):
            adjacency_matrix[i, self.adjacency_lists[i]] = 1

        return Graph(name=self.name,
                     adjacency_matrix=adjacency_matrix)

    # TODO test
    def kahn_algorithm_topological_ordering(self):
        """
        An implementation of Kahn's algorithm for topological ordering of a
        graph. Note that it does not make sense to use this method if the
        graph is not in fact a DAG !

        Returns
        -------
        list
            A topological ordering of the graph.
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
    def dfs_topological_ordering(self):
        """
        An implementation of the DFS-based (Depth First Search) algorithm for
        topological ordering of a graph. Note that it does not make sense to
        use this method if the graph is not in fact a DAG !

        Returns
        -------
        list
            A topological ordering of the graph.
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
        ValueError
            If the ordering passed is not a valid ordering for the graph.
        """
        if set(ordering) != set(range(self.nb_vertices)):
            msg = "Ordering provided is not a valid ordering for the graph !"
            raise ValueError(msg)

        # Build a "look-up table" of the nodes and their indices
        index_lookup = dict()
        for i in range(self.nb_vertices):
            index_lookup[i] = ordering.index(i)

        # Use the definition of a topological ordering
        for i in range(len(self.adjacency_lists)):
            parent = i
            children = self.adjacency_lists[parent]
            for child in children:
                if index_lookup[child] <= index_lookup[parent]:
                    return False
                else:
                    pass

        return True

    def __str__(self):
        """
        Returns a user-friendly string representation of the object.

        Returns
        -------
        str
            A user-friendly string representation of the object.
        """
        s = f"AlternativeGraph '{self.name}', {self.nb_vertices} vertices, "
        s += f"adjacency lists:\n{self.adjacency_lists}"

        return s

    # TODO test that with eval can reconstitute the object
    def __repr__(self):
        """
        Returns a string representation of the object from which it can be
        rebuilt.

        Returns
        -------
        str
            A string representation of the object from which it can be rebuilt.
        """
        s = f"AlternativeGraph(nb_vertices={repr(self.nb_vertices)}, "
        s += f"adjacency_lists={repr(self.adjacency_lists)}, "
        s += f"name={repr(self.name)})"

        return s

    def __eq__(self, other):
        """
        Checks whether the object is equal to another AlternativeGraph object.
        The two objects are equal if they have the same number of vertices, the
        same adjacency lists and the same names.

        Parameters
        ----------
        other : AlternativeGraph
            The other AlternativeGraph object.

        Returns
        -------
        bool
            Whether the objects are equal.
        """

        if self.nb_vertices != other.nb_vertices:
            return False

        if self.adjacency_lists != other.adjacency_lists:
            return False

        if self.name != other.name:
            return False

        return True


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
    reconstructed = eval(repr(test_graph))

    print(f"Graph reconstruction worked : {test_graph == reconstructed}")

    transformed = test_graph.to_adjacency_list_representation()
    print(transformed.nb_vertices)
    print(transformed.adjacency_lists)
    print(transformed.indegrees)
    print(f"Causal order : {transformed.dfs_topological_ordering()}")
    print(f"Kahn : {transformed.kahn_algorithm_topological_ordering()}")
    print(transformed.check_topological_ordering(transformed.kahn_algorithm_topological_ordering()))

    print('\n\n\n')
    print(transformed)
    reconstructed = eval(repr(transformed))
    print(f"AlternativeGraph reconstruction worked : " +
          f"{transformed == reconstructed}")

    print('\n\n\n')

    retransformed = transformed.to_adjacency_matrix_representation()
    print(retransformed.adjacency_matrix)