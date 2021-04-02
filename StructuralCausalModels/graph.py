from enum import Enum

import numpy as np


class InvalidAdjacencyMatrix(Exception):
    pass


class GraphViaAdjacencyMatrix:
    """
    Implements a graph structure using an adjacency matrix representation.
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

    # TODO remove
    # def to_adjacency_list_representation(self):
    #     """
    #     Returns an AlternativeGraph object which is equivalent to the Graph
    #     object.
    #
    #     Returns
    #     -------
    #     AlternativeGraph
    #         The equivalent adjacency list based representation of the graph.
    #     """
    #     nb_vertices = self.adjacency_matrix.shape[0]
    #
    #     # Build the adjacency lists
    #     adjacency_lists = []
    #     for i in range(nb_vertices):
    #         adjacency_lists.append(
    #             np.where(self.adjacency_matrix[i, :] != 0)[0].tolist()
    #         )
    #
    #     return GraphViaAdjacencyLists(name=self.name,
    #                                   nb_vertices=nb_vertices,
    #                                   adjacency_lists=adjacency_lists)

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
        Checks whether the object is equal to another Graph object. Two Graph
        objects are equal if they have the same adjacency matrix and the same
        names.

        Parameters
        ----------
        other : GraphViaAdjacencyMatrix
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


class GraphViaAdjacencyLists:
    """
    Implements a graph structure representing an adjacency list representation.
    """

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

    # TODO remove
    # def to_adjacency_matrix_representation(self):
    #     """
    #     Returns a Graph object which is equivalent to the AlternativeGraph
    #     object.
    #
    #     Returns
    #     -------
    #     Graph
    #         The equivalent adjacency matrix based representation of the graph.
    #     """
    #
    #     # Build the adjacency matrix
    #     adjacency_matrix = np.zeros((self.nb_vertices, self.nb_vertices))
    #     for i in range(self.nb_vertices):
    #         adjacency_matrix[i, self.adjacency_lists[i]] = 1
    #
    #     return GraphViaAdjacencyMatrix(name=self.name,
    #                                    adjacency_matrix=adjacency_matrix)

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

    def __repr__(self):
        """
        Returns a string representation of the object from which it can be
        rebuilt.

        Returns
        -------
        str
            A string representation of the object from which it can be rebuilt.
        """
        s = f"GraphViaAdjacencyLists(nb_vertices={repr(self.nb_vertices)}, "
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
        other : GraphViaAdjacencyLists
            The other AlternativeGraph object.

        Returns
        -------
        bool
            Whether the objects are equal.
        """

        if self.nb_vertices != other.nb_vertices:
            return False

        if len(self.adjacency_lists) != len(other.adjacency_lists):
            return False
        else:
            for l1, l2 in zip(self.adjacency_lists, other.adjacency_lists):
                if set(l1) != set(l2):
                    return False

        if self.name != other.name:
            return False

        return True


class GraphsCannotBeCompared(Exception):

    pass



class EdgeType(Enum):
    NONE = 'no edge'
    FORWARD = '->'
    BACKWARD = '<-'
    UNDIRECTED = '--'


class ImpossibleEdgeConfiguration(Exception):

    pass


class GraphViaEdges:

    # TODO parameter validation
    def __init__(self, edges, name=''):
        self.edges = edges
        self.name = name

    # TODO __str__ method
    # TODO __repr__ method
    # TODO __eq__ method


class Graph:

    def __init__(self, adjacency_matrix, name=''):
        # Representation of the graph via an adjacency matrix
        matrix_based = GraphViaAdjacencyMatrix(
            adjacency_matrix=adjacency_matrix,
            name=name
        )
        # Representation of the graph via adjacency lists
        adjacency_lists = Graph.adjacency_matrix_to_adjacency_lists(
            adjacency_matrix=adjacency_matrix
        )
        list_based = GraphViaAdjacencyLists(
            nb_vertices=len(adjacency_lists),
            adjacency_lists=adjacency_lists,
            name=name
        )
        # Representation of the graph via edges
        edges = Graph.adjacency_matrix_to_edges(
            adjacency_matrix=adjacency_matrix
        )
        edge_based = GraphViaEdges(edges=edges,
                                   name=name)
        self.adjacency_matrix_representation = matrix_based
        self.adjacency_list_representation = list_based
        self.edge_representation = edge_based

    @staticmethod
    def validate_binary_matrix(matrix):
        return GraphViaAdjacencyMatrix.validate_binary_matrix(matrix)

    @property
    def adjacency_matrix(self):
        return self.adjacency_matrix_representation.adjacency_matrix

    @property
    def name(self):
        return self.adjacency_matrix_representation.name

    @adjacency_matrix.setter
    def adjacency_matrix(self, new_adjacency_matrix):
        # Re-generate the adjacency matrix based representation of the graph
        new_matrix_based = GraphViaAdjacencyMatrix(
            adjacency_matrix=new_adjacency_matrix,
            name=self.name
        )
        # Likewise, regenerate the representation via adjacency lists
        new_adjacency_lists = Graph.adjacency_matrix_to_adjacency_lists(
            adjacency_matrix=new_adjacency_matrix
        )
        new_list_based = GraphViaAdjacencyLists(
            nb_vertices=len(new_adjacency_lists),
            adjacency_lists=new_adjacency_lists,
            name=self.name
        )
        # Likewise, regenerate the representation via edges
        new_edges = Graph.adjacency_matrix_to_edges(
            adjacency_matrix=new_adjacency_matrix
        )
        new_edge_based = GraphViaEdges(edges=new_edges,
                                       name=self.name)
        self.adjacency_matrix_representation = new_matrix_based
        self.adjacency_list_representation = new_list_based
        self.edge_representation = new_edge_based

    # TODO document
    # TODO test
    @staticmethod
    def adjacency_matrix_to_adjacency_lists(adjacency_matrix):

        nb_vertices = adjacency_matrix.shape[0]

        # Build the adjacency lists
        adjacency_lists = []
        for i in range(nb_vertices):
            adjacency_lists.append(
                np.where(adjacency_matrix[i, :] != 0)[0].tolist()
            )

        return adjacency_lists

    # TODO document
    # TODO test
    @staticmethod
    def adjacency_lists_to_adjacency_matrix(adjacency_lists):
        nb_vertices = len(adjacency_lists)
        # Build the adjacency matrix
        adjacency_matrix = np.zeros((nb_vertices, nb_vertices))
        for i in range(nb_vertices):
            adjacency_matrix[i, adjacency_lists[i]] = 1

        return adjacency_matrix

    # TODO test
    # TODO document
    @staticmethod
    def compute_edge_type(m_ij, m_ji):

        if m_ij == 0 and m_ji == 0:

            return EdgeType.NONE

        elif m_ij == 1 and m_ji == 0:

            return EdgeType.FORWARD

        elif m_ij == 0 and m_ji == 1:

            return EdgeType.BACKWARD

        elif m_ij == 1 and m_ji == 1:

            return EdgeType.UNDIRECTED

        else:

            raise ImpossibleEdgeConfiguration

    # TODO document
    # TODO test
    @staticmethod
    def adjacency_matrix_to_edges(adjacency_matrix):

        edges = dict()

        m = adjacency_matrix.shape[0]
        for i in range(m):
            for j in range(i, m):
                edges[(i, j)] = Graph.compute_edge_type(
                    m_ij=adjacency_matrix[i, j],
                    m_ji=adjacency_matrix[j, i])

        return edges

    # TODO document
    # TODO test
    @staticmethod
    def edges_to_adjacency_lists(edges):

        parent_children = dict()

        for key, value in edges.items():

            left_end_node = key[0]
            right_end_node = key[1]
            if left_end_node not in parent_children.keys():
                parent_children[left_end_node] = []
            if right_end_node not in parent_children.keys():
                parent_children[right_end_node] = []

            if value == EdgeType.NONE:
                pass
            elif value == EdgeType.FORWARD:
                parent_children[left_end_node].append(right_end_node)
            elif value == EdgeType.BACKWARD:
                parent_children[right_end_node].append(left_end_node)
            elif value == EdgeType.UNDIRECTED:
                parent_children[left_end_node].append(right_end_node)
                parent_children[right_end_node].append(left_end_node)
            else:
                raise ImpossibleEdgeConfiguration

        adjacency_lists = []
        nb_vertices = len(parent_children.keys())
        for i in range(nb_vertices):
            adjacency_lists.append(parent_children[i])

        return adjacency_lists

    # TODO document
    @staticmethod
    def compute_penalty_edge_mismatch(edge_1, edge_2):

        if edge_1 == edge_2:
            return 0
        elif {edge_1, edge_2} == {EdgeType.NONE, EdgeType.FORWARD}:
            return 1
        elif {edge_1, edge_2} == {EdgeType.NONE, EdgeType.BACKWARD}:
            return 1
        elif {edge_1, edge_2} == {EdgeType.NONE, EdgeType.UNDIRECTED}:
            return 1
        elif {edge_1, edge_2} == {EdgeType.FORWARD, EdgeType.BACKWARD}:
            return 1
        elif {edge_1, edge_2} == {EdgeType.FORWARD, EdgeType.UNDIRECTED}:
            return 1
        elif {edge_1, edge_2} == {EdgeType.BACKWARD, EdgeType.UNDIRECTED}:
            return 1
        else:
            raise ImpossibleEdgeConfiguration

    # TODO document
    def structural_hamming_distance(self,
                                    other,
                                    penalty_edge_mismatch_func=None):

        edges_1 = Graph.adjacency_matrix_to_edges(self.adjacency_matrix)
        edges_2 = Graph.adjacency_matrix_to_edges(other.adjacency_matrix)

        if penalty_edge_mismatch_func is None:
            penalty_edge_mismatch_func = Graph.compute_penalty_edge_mismatch

        if set(edges_1.keys()) != set(edges_2.keys()):
            msg = 'The Structural Hamming Distances cannot be computed : the '
            msg += 'graphs cannot be compared.'
            raise GraphsCannotBeCompared(msg)

        shd = 0

        for key in edges_1.keys():

            shd += penalty_edge_mismatch_func(
                edge_1=edges_1[key],
                edge_2=edges_2[key]
            )

        return shd
