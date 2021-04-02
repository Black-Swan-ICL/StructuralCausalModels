import numpy as np

from StructuralCausalModels.graph_via_adjacency_lists import \
    GraphViaAdjacencyLists
from StructuralCausalModels.graph_via_adjacency_matrix import \
    GraphViaAdjacencyMatrix
from StructuralCausalModels.graph_via_edges import EdgeType, GraphViaEdges, \
    ImpossibleEdgeConfiguration


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
    def structural_hamming_distance(self,
                                    other,
                                    penalty_edge_mismatch_func=None):

        res = self.edge_representation.structural_hamming_distance(
            other=other.edge_representation,
            penalty_edge_mismatch_func=penalty_edge_mismatch_func
        )

        return res

    # TODO document
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
