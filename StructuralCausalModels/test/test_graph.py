import pytest
import numpy as np

from StructuralCausalModels.graph import GraphViaAdjacencyMatrix, \
    GraphViaAdjacencyLists, Graph, EdgeType


_adjacency_matrix = np.asarray([
    [0, 1, 1, 1],
    [0, 0, 1, 0],
    [0, 0, 0, 0],
    [0, 1, 1, 0]
])
_adjacency_lists = [
    [1, 2, 3],
    [2],
    [],
    [1, 2]
]


@pytest.fixture
def via_matrix_example():

    example = GraphViaAdjacencyMatrix(adjacency_matrix=_adjacency_matrix,
                                      name='')

    return example


@pytest.fixture
def via_list_example():

    example = GraphViaAdjacencyLists(adjacency_lists=_adjacency_lists,
                                     nb_vertices=4,
                                     name='')

    return example


@pytest.mark.parametrize(
    "matrix,expected",
    [
        (np.asarray([]), False),
        (np.asarray([1, 0, 1]), False),
        (np.asarray([[1, 0, 1], [1, 0, 0]]), False),
        (np.asarray([[1, 1], [1, 1]]), True),
        (np.asarray([[0, 0, 0], [0, 0, 0], [0, 0, 0]]), True),
        (np.asarray([[1, 0, 0], [1, 2, 1], [1, 0, 1]]), False),
    ]
)
def test_validate_adjacency_matrix(matrix, expected):

    assert Graph.validate_binary_matrix(matrix) == expected


# TODO test further ?
@pytest.mark.parametrize(
    "adjacency_matrix, expected_adjacency_lists",
    [
        (_adjacency_matrix, _adjacency_lists),
    ]
)
def test_adjacency_matrix_to_adjacency_lists(adjacency_matrix,
                                             expected_adjacency_lists):

    actual_adjacency_lists = Graph.adjacency_matrix_to_adjacency_lists(
        adjacency_matrix=adjacency_matrix
    )

    adjacency_lists_equal = []
    for l1, l2 in zip(actual_adjacency_lists, expected_adjacency_lists):
        adjacency_lists_equal.append(set(l1) == set(l2))

    assert all(adjacency_lists_equal)


@pytest.mark.parametrize(
    "adjacency_lists, expected_adjacency_matrix",
    [
        (_adjacency_lists, _adjacency_matrix),
    ]
)
def test_adjacency_lists_to_adjacency_matrix(adjacency_lists,
                                             expected_adjacency_matrix):

    actual_adjacency_matrix = Graph.adjacency_lists_to_adjacency_matrix(
        adjacency_lists=adjacency_lists
    )

    assert np.all(actual_adjacency_matrix == expected_adjacency_matrix)


def test_can_rebuild_graph_via_matrix(via_matrix_example):

    reconstructed = eval(repr(via_matrix_example))

    assert reconstructed == via_matrix_example


def test_can_rebuild_graph_via_list(via_list_example):

    reconstructed = eval(repr(via_list_example))

    assert reconstructed == via_list_example


@pytest.mark.parametrize(
    "adjacency_matrix, expected_edge_types",
    [
        (
            np.asarray([
                [0, 1, 1, 1],
                [0, 0, 1, 0],
                [0, 0, 0, 0],
                [0, 1, 1, 0]
            ]),
            {
                (0, 0): EdgeType.NONE,
                (0, 1): EdgeType.FORWARD,
                (0, 2): EdgeType.FORWARD,
                (0, 3): EdgeType.FORWARD,
                (1, 1): EdgeType.NONE,
                (1, 2): EdgeType.FORWARD,
                (1, 3): EdgeType.BACKWARD,
                (2, 2): EdgeType.NONE,
                (2, 3): EdgeType.BACKWARD,
                (3, 3): EdgeType.NONE
            }
        ),
        (
                np.asarray([
                    [0, 1, 1, 1],
                    [1, 0, 1, 1],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0]
                ]),
                {
                    (0, 0): EdgeType.NONE,
                    (0, 1): EdgeType.UNDIRECTED,
                    (0, 2): EdgeType.FORWARD,
                    (0, 3): EdgeType.FORWARD,
                    (1, 1): EdgeType.NONE,
                    (1, 2): EdgeType.FORWARD,
                    (1, 3): EdgeType.FORWARD,
                    (2, 2): EdgeType.NONE,
                    (2, 3): EdgeType.UNDIRECTED,
                    (3, 3): EdgeType.NONE
                }
        ),

    ]
)
def test_adjacency_matrix_to_edges(adjacency_matrix, expected_edge_types):

    actual_edge_types = Graph.adjacency_matrix_to_edges(adjacency_matrix)

    assert actual_edge_types == expected_edge_types


@pytest.mark.parametrize(
    "edge_1, edge_2, expected_penalty",
    [
        (EdgeType.FORWARD, EdgeType.FORWARD, 0),
        (EdgeType.UNDIRECTED, EdgeType.NONE, 1),
    ]
)
def test_compute_penalty_edge_mismatch(edge_1, edge_2, expected_penalty):

    actual_penalty = Graph.compute_penalty_edge_mismatch(edge_1, edge_2)

    assert actual_penalty == expected_penalty


@pytest.mark.parametrize(
    "adjacency_matrix_1, adjacency_matrix_2, expected_shd",
    [
        (
            np.asarray([
                [0, 1, 1, 1],
                [0, 0, 1, 0],
                [0, 0, 0, 0],
                [0, 1, 1, 0]
            ]),
            np.asarray([
                [0, 1, 1, 1],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [0, 0, 0, 0]
            ]),
            2
        ),
        (
            np.asarray([
                [0, 0, 1, 1],
                [1, 0, 1, 1],
                [0, 0, 0, 1],
                [0, 0, 1, 0]
            ]),
            np.asarray([
                [0, 1, 1, 1],
                [1, 0, 1, 1],
                [0, 0, 0, 1],
                [0, 0, 1, 0]
            ]),
            1
        ),
        (
                np.asarray([
                    [0, 1, 1, 1],
                    [0, 0, 1, 0],
                    [0, 0, 0, 0],
                    [0, 1, 1, 0]
                ]),
                np.asarray([
                    [0, 1, 1, 1],
                    [1, 0, 1, 1],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0]
                ]),
                3
        ),
    ]
)
def test_structural_hamming_distance(adjacency_matrix_1, adjacency_matrix_2,
                                     expected_shd):

    graph_1 = Graph(adjacency_matrix=adjacency_matrix_1)
    graph_2 = Graph(adjacency_matrix=adjacency_matrix_2)

    actual_shd = graph_1.structural_hamming_distance(graph_2)

    assert expected_shd == actual_shd