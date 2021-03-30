import pytest
import numpy as np

from StructuralCausalModels.directed_graph import DirectedGraph


@pytest.mark.parametrize(
    "matrix,expected",
    [
        (np.asarray([]), False),
        (np.asarray([1, 0, 1]), False),
        (np.asarray([[1, 0, 1], [1, 0, 0]]), False),
        (np.asarray([[1, 1], [1, 1]]), False),
        (np.asarray([[1, 0, 0], [1, 2, 1], [1, 0, 1]]), False),
        (np.asarray([[0, 0, 0], [0, 0, 0], [0, 0, 0]]), True),
        (np.asarray([[1, 0, 0], [0, 0, 0], [0, 0, 0]]), False),
        (np.asarray([[0, 0, 1], [0, 0, 0], [1, 0, 0]]), False),
        (np.asarray([[0, 1, 0], [0, 0, 1], [1, 0, 0]]), True),
    ]
)
def test_validate_directed_graph(matrix, expected):

    assert (DirectedGraph.validate_directed_graph_adjacency_matrix(matrix) ==
            expected)
