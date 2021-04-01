import pytest
import numpy as np

from StructuralCausalModels.graph import GraphViaAdjacencyMatrix, \
    GraphViaAdjacencyLists, Graph


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


def test_matrix_to_list_representation_transformation(via_matrix_example,
                                                      via_list_example):

    actual = via_matrix_example.to_adjacency_list_representation()

    assert actual == via_list_example


def test_list_to_matrix_representation_transformation(via_list_example,
                                                      via_matrix_example):

    actual = via_list_example.to_adjacency_matrix_representation()

    assert actual == via_matrix_example


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
                (0, 0): 'no edge',
                (0, 1): '->',
                (0, 2): '->',
                (0, 3): '->',
                (1, 1): 'no edge',
                (1, 2): '->',
                (1, 3): '<-',
                (2, 2): 'no edge',
                (2, 3): '<-',
                (3, 3): 'no edge'
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
                    (0, 0): 'no edge',
                    (0, 1): '--',
                    (0, 2): '->',
                    (0, 3): '->',
                    (1, 1): 'no edge',
                    (1, 2): '->',
                    (1, 3): '->',
                    (2, 2): 'no edge',
                    (2, 3): '--',
                    (3, 3): 'no edge'
                }
        ),

    ]
)
def test_compute_edge_types(adjacency_matrix, expected_edge_types):

    actual_edge_types = Graph.compute_edge_types(adjacency_matrix)

    assert actual_edge_types == expected_edge_types