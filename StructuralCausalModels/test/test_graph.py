# TODO reorganise and document
import pytest
import numpy as np

from StructuralCausalModels.graph import Graph, EdgeType, \
    ImpossibleEdgeConfiguration


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


@pytest.mark.parametrize(
    "m_ij, m_ji, expected_typed_edge",
    [
        (0, 0, EdgeType.NONE),
        (1, 0, EdgeType.FORWARD),
        (1, 1, EdgeType.UNDIRECTED),
        (0, 1, EdgeType.BACKWARD)
    ]
)
def test_compute_edge_types(m_ij, m_ji, expected_typed_edge):

    actual_typed_edge = Graph.compute_edge_type(m_ij=m_ij,
                                                m_ji=m_ji)

    assert actual_typed_edge == expected_typed_edge


def test_crash_compute_edge_types():

    with pytest.raises(ImpossibleEdgeConfiguration):

        Graph.compute_edge_type(-1, 1)


@pytest.mark.parametrize(
    "adjacency_matrix, expected_typed_edges",
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
def test_adjacency_matrix_to_edges(adjacency_matrix, expected_typed_edges):

    actual_edge_types = Graph.adjacency_matrix_to_edges(adjacency_matrix)

    assert actual_edge_types == expected_typed_edges


# TODO test further ?
@pytest.mark.parametrize(
    "edges, expected_adjacency_lists",
    [
        (
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
                },
                [[1, 2, 3],
                 [2],
                 [],
                 [1, 2]]
        ),
    ]

)
def test_edges_to_adjacency_lists(edges, expected_adjacency_lists):

    actual_adjacency_lists = Graph.edges_to_adjacency_lists(edges)

    assert actual_adjacency_lists == expected_adjacency_lists


@pytest.mark.parametrize(
    "edges, expected_adjacency_matrix",
    [
        (
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
                },
                np.asarray([
                    [0, 1, 1, 1],
                    [0, 0, 1, 0],
                    [0, 0, 0, 0],
                    [0, 1, 1, 0]
                ])
        ),
        (
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
                },
                np.asarray([
                    [0, 1, 1, 1],
                    [1, 0, 1, 1],
                    [0, 0, 0, 1],
                    [0, 0, 1, 0]
                ])
        ),
    ]
)
def test_edges_to_adjacency_matrix(edges, expected_adjacency_matrix):

    actual_adjacency_matrix = Graph.edges_to_adjacency_matrix(edges)

    assert np.all(actual_adjacency_matrix == expected_adjacency_matrix)


# TODO test further ?
@pytest.mark.parametrize(
    "adjacency_lists, expected_typed_edges",
    [
        (
                [[1, 2, 3],
                 [2],
                 [],
                 [1, 2]],
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
    ]
)
def test_adjacency_list_to_edges(adjacency_lists, expected_typed_edges):

    actual_typed_edges = Graph.adjacency_lists_to_edges(adjacency_lists)

    assert actual_typed_edges == expected_typed_edges
