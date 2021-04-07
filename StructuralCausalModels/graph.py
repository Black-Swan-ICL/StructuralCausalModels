import numpy as np

from StructuralCausalModels.graph_via_adjacency_lists import \
    GraphViaAdjacencyLists
from StructuralCausalModels.graph_via_adjacency_matrix import \
    GraphViaAdjacencyMatrix
from StructuralCausalModels.graph_via_edges import EdgeType, GraphViaEdges, \
    ImpossibleEdgeConfiguration


class Graph:
    """A class to represent graphs.

    A Graph object is a representation of the graph. The graph may be very
    general : it does not have to be directed, or acyclic for instance. It
    is arguably easiest to think of a graph in terms of its adjacency matrix
    which is why this implementation is 'adjacency matrix'-driven. Other
    representations can be more convenient depending on context, which is
    why these representations are automatically generated upon construction
    and stored as attributes of the Graph object.

    Parameters
    ----------
    adjacency_matrix : array_like
        The adjacency matrix of the graph.
    name : str, optional
        The name of the object created (default is '').

    Attributes
    ----------
    adjacency_matrix_representation : GraphViaAdjacencyMatrix
        The representation of the graph based on the adjacency matrix.
    adjacency_list_representation : GraphViaAdjacencyLists
        The representation of the graph based on the adjacency lists.
    edge_representation : GraphViaEdges
        The adjacency of the graph based on the typed (undirected, forward etc.)
        edges.
    """

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
        """Validates that a matrix is a proper adjacency matrix.

        A proper adjacency matrix contains only 0's and 1's.

        Parameters
        ----------
        matrix : array_like
            The matrix to validate.

        Returns
        -------
        bool
            Whether the matrix is a valid adjacency matrix.
        """

        return GraphViaAdjacencyMatrix.validate_binary_matrix(matrix)

    @property
    def adjacency_matrix(self):
        """array_like: the adjacency matrix of the graph."""
        return self.adjacency_matrix_representation.adjacency_matrix

    @property
    def name(self):
        """str: the name of the graph."""
        return self.adjacency_matrix_representation.name

    @adjacency_matrix.setter
    def adjacency_matrix(self, new_adjacency_matrix):
        """Sets adjacency matrix of a graph to a new value.

        When changing the adjacency matrix of the graph, the different graph
        representations are automatically re-generated to maintain consistency.

        Parameters
        ----------
        new_adjacency_matrix : array_like
            The new adjacency matrix of the graph.
        """

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

    def structural_hamming_distance(self,
                                    other,
                                    penalty_edge_mismatch_func=None):
        """Computes the Structural Hamming Distance between two graphs.

        By default, the Structural Hamming Distance (SHD) is equal to the number
        of edges in the graphs that are not of the same type. A different
        weighted scheme for penalty computation may be provided (we may want to
        penalise the presence of an edge in the opposite direction more than the
        absence of an edge, for example).

        Parameters
        ----------
        other : Graph
            The graph to compare.
        penalty_edge_mismatch_func : callable, optional
            The edge mismatch penalty scheme (default is None in which case a
            built-in function is used).

        Returns
        -------
        float
            The Structural Hamming Distance (SHD), in its default form or under
            a user-provided edge mismatch penalty scheme.

        Raises
        ------
        GraphsCannotBeCompared
            Raised if the graphs do not have the same vertex set.
        """

        res = self.edge_representation.structural_hamming_distance(
            other=other.edge_representation,
            penalty_edge_mismatch_func=penalty_edge_mismatch_func
        )

        return res

    @staticmethod
    def adjacency_matrix_to_adjacency_lists(adjacency_matrix):
        """Converts an adjacency matrix to the corresponding adjacency lists.

        Parameters
        ----------
        adjacency_matrix : array_like
            The adjacency matrix.

        Returns
        -------
        list
            The adjacency lists.
        """

        nb_vertices = adjacency_matrix.shape[0]

        # Build the adjacency lists
        adjacency_lists = []
        for i in range(nb_vertices):
            adjacency_lists.append(
                np.where(adjacency_matrix[i, :] != 0)[0].tolist()
            )

        return adjacency_lists

    @staticmethod
    def adjacency_lists_to_adjacency_matrix(adjacency_lists):
        """Converts adjacency lists to the corresponding adjacency matrix.

        Parameters
        ----------
        adjacency_lists : list
            The adjacency lists.

        Returns
        -------
        array_like
            The adjacency matrix.
        """
        nb_vertices = len(adjacency_lists)
        # Build the adjacency matrix
        adjacency_matrix = np.zeros((nb_vertices, nb_vertices))
        for i in range(nb_vertices):
            adjacency_matrix[i, adjacency_lists[i]] = 1

        return adjacency_matrix

    @staticmethod
    def compute_edge_type(m_ij, m_ji):
        """Determines the type of the edge between two vertices.

        Determines the type of the edge between :math:`X_i` and :math:`X_j`
        based on the values of :math:`M_{i,j}` and :math:`M_{j,i}` where
        :math:`M` is the adjacency matrix of the graph.

        Parameters
        ----------
        m_ij : int
            The element in the adjacency matrix at the intersection of the i-th
            row and the j-th column.
        m_ji : int
            The element in the adjacency matrix at the intersection of the j-th
            row and the i-th column.

        Returns
        -------
        EdgeType
            The typed edge between :math:`X_i` and :math:`X_j` in the graph.
        """

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

    @staticmethod
    def adjacency_matrix_to_edges(adjacency_matrix):
        """Converts adjacency matrix to the corresponding typed edges.

        Parameters
        ----------
        adjacency_matrix : array_like
            The adjacency matrix.

        Returns
        -------
        dict
            The typed edges.

            The keys are tuples (i, j) ; they indicates the edge is between
            :math:`X_i` and :math:`X_j` in the graph. The values are
            EdgeType objects which indicate what type of edge is between
            :math:`X_i` and :math:`X_j` in the graph.
        """

        edges = dict()

        m = adjacency_matrix.shape[0]
        for i in range(m):
            for j in range(i, m):
                edges[(i, j)] = Graph.compute_edge_type(
                    m_ij=adjacency_matrix[i, j],
                    m_ji=adjacency_matrix[j, i])

        return edges

    @staticmethod
    def edges_to_adjacency_lists(edges):
        """Converts the typed edges to the corresponding adjacency lists.

        Parameters
        ----------
        edges : dict
            The typed edges.

            The keys are tuples (i, j) ; they indicates the edge is between
            :math:`X_i` and :math:`X_j` in the graph. The values are
            EdgeType objects which indicate what type of edge is between
            :math:`X_i` and :math:`X_j` in the graph.

        Returns
        -------
        list
            The adjacency lists.
        """

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

    @staticmethod
    def edges_to_adjacency_matrix(edges):
        """Converts the typed edges to the corresponding adjacency matrix.

        Parameters
        ----------
        edges : dict
            The typed edges.

            The keys are tuples (i, j) ; they indicates the edge is between
            :math:`X_i` and :math:`X_j` in the graph. The values are
            EdgeType objects which indicate what type of edge is between
            :math:`X_i` and :math:`X_j` in the graph.

        Returns
        -------
        array_like
            The adjacency matrix.
        """
        adjacency_lists = Graph.edges_to_adjacency_lists(edges=edges)
        adjacency_matrix = Graph.adjacency_lists_to_adjacency_matrix(
            adjacency_lists=adjacency_lists
        )

        return adjacency_matrix

    @staticmethod
    def adjacency_lists_to_edges(adjacency_lists):
        """Converts adjacency lists to the corresponding typed edges..

        Parameters
        ----------
        adjacency_lists : list
            The adjacency lists.

        Returns
        -------
        dict
            The typed edges.

            The keys are tuples (i, j) ; they indicates the edge is between
            :math:`X_i` and :math:`X_j` in the graph. The values are
            EdgeType objects which indicate what type of edge is between
            :math:`X_i` and :math:`X_j` in the graph.
        """
        adjacency_matrix = Graph.adjacency_lists_to_adjacency_matrix(
            adjacency_lists=adjacency_lists
        )
        edges = Graph.adjacency_matrix_to_edges(
            adjacency_matrix=adjacency_matrix
        )

        return edges
