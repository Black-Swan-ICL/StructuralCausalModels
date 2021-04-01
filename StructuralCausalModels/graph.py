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

        return GraphViaAdjacencyLists(name=self.name,
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

        return GraphViaAdjacencyMatrix(name=self.name,
                                       adjacency_matrix=adjacency_matrix)

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


class Graph:

    def __init__(self, adjacency_matrix, name=''):
        matrix_based = GraphViaAdjacencyMatrix(
            adjacency_matrix=adjacency_matrix,
            name=name
        )
        list_based = matrix_based.to_adjacency_list_representation()
        self.adjacency_matrix_representation = matrix_based
        self.adjacency_list_representation = list_based

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
        matrix_based = GraphViaAdjacencyMatrix(
            adjacency_matrix=new_adjacency_matrix,
            name=self.name
        )
        list_based = matrix_based.to_adjacency_list_representation()
        self.adjacency_matrix_representation = matrix_based
        self.adjacency_list_representation = list_based
