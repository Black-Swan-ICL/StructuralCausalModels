# TODO reorganise and document
import pytest
import numpy as np

from StructuralCausalModels.dag import DirectedAcyclicGraph


_small_adj_matrix = np.asarray([
    [0, 1, 1, 1],
    [0, 0, 1, 0],
    [0, 0, 0, 0],
    [0, 1, 1, 0]
])
_small_adj_matrix_causal_orders = [[0, 3, 1, 2]]

_large_adj_matrix = np.asarray([
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0]
])
_large_adj_matrix_causal_orders = [[0, 1, 2, 3, 4, 6, 5],
                                   [0, 1, 2, 4, 3, 6, 5],
                                   [0, 2, 1, 3, 4, 6, 5],
                                   [0, 2, 1, 4, 3, 6, 5],
                                   [1, 0, 2, 3, 4, 6, 5],
                                   [1, 0, 2, 4, 3, 6, 5],
                                   [1, 2, 0, 3, 4, 6, 5],
                                   [1, 2, 0, 4, 3, 6, 5],
                                   [2, 0, 1, 3, 4, 6, 5],
                                   [2, 0, 1, 4, 3, 6, 5],
                                   [2, 1, 0, 3, 4, 6, 5],
                                   [2, 1, 0, 4, 3, 6, 5]]

_maximally_connected_large_matrix_causal_order = [0, 1, 2, 3, 4, 6, 5]
_maximally_connected_large_adj_matrix = np.asarray([
    [0, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0]
])


@pytest.mark.parametrize(
    "matrix, expected",
    [
        (np.asarray([]), False),
        (np.asarray([1, 0, 1]), False),
        (np.asarray([[1, 0, 1], [1, 0, 0]]), False),
        (np.asarray([[1, 1], [1, 1]]), False),
        (np.asarray([[1, 0, 0], [1, 2, 1], [1, 0, 1]]), False),
        (np.asarray([[0, 0, 0], [0, 0, 0], [0, 0, 0]]), True),
        (np.asarray([[1, 0, 0], [0, 0, 0], [0, 0, 0]]), False),
        (np.asarray([[0, 0, 1], [0, 0, 0], [1, 0, 0]]), False),
        (np.asarray([[0, 1, 0], [0, 0, 1], [1, 0, 0]]), False),
        (np.asarray([[0, 1, 0], [0, 0, 1], [0, 0, 0]]), True)
    ]
)
def test_validate_directed_acyclic_graph(matrix, expected):

    assert (DirectedAcyclicGraph.validate_dag_adjacency_matrix(matrix) ==
            expected)


@pytest.mark.parametrize(
    "matrix, admissible_orders",
    [
        (_small_adj_matrix, _small_adj_matrix_causal_orders),
        (_large_adj_matrix, _large_adj_matrix_causal_orders),
    ]
)
def test_kahn_algorithm(matrix, admissible_orders):

    dag = DirectedAcyclicGraph(adjacency_matrix=matrix)
    causaL_order = dag.kahn_algorithm()

    assert causaL_order in admissible_orders


# TODO correct the algorithm and check again
# @pytest.mark.parametrize(
#     "matrix, admissible_orders",
#     [
#         (_small_adj_matrix, _small_adj_matrix_causal_orders),
#         (_large_adj_matrix, _large_adj_matrix_causal_orders),
#     ]
# )
# def test_depth_first_search(matrix, admissible_orders):
#
#     dag = DirectedAcyclicGraph(adjacency_matrix=matrix)
#     causaL_order = dag.depth_first_search()
#
#     assert causaL_order in admissible_orders


@pytest.mark.parametrize(
    "matrix, ordering, expected",
    [
        (_small_adj_matrix, _small_adj_matrix_causal_orders[0], True),
        (_small_adj_matrix, [0, 1, 3, 2], False),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[0], True),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[1], True),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[2], True),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[3], True),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[4], True),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[5], True),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[6], True),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[7], True),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[8], True),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[9], True),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[10], True),
        (_large_adj_matrix, _large_adj_matrix_causal_orders[11], True),
    ]
)
def test_check_topological_ordering(matrix, ordering, expected):

    dag = DirectedAcyclicGraph(adjacency_matrix=matrix)

    assert expected == dag.check_topological_ordering(ordering)


@pytest.mark.parametrize(
    "causal_order, expected_adjacency_matrix",
    [
        (_maximally_connected_large_matrix_causal_order,
         _maximally_connected_large_adj_matrix)
    ]
)
def test_causal_order_to_dag(causal_order, expected_adjacency_matrix):

    dag = DirectedAcyclicGraph.causal_order_to_dag(causal_order)
    actual_adjacency_matrix = dag.adjacency_matrix

    assert np.all(actual_adjacency_matrix == expected_adjacency_matrix)
