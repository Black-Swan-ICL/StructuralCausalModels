# TODO reorganise and document
import pytest
import numpy as np

from StructuralCausalModels.graph_via_adjacency_matrix import \
    GraphViaAdjacencyMatrix


@pytest.fixture
def graph_via_adjacency_matrix_example():

    example = GraphViaAdjacencyMatrix(
        adjacency_matrix=np.asarray([
            [0, 1, 1, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 0],
            [0, 1, 1, 0]
        ]),
        name='')

    return example


def test_can_rebuild_graph_from_matrix(graph_via_adjacency_matrix_example):

    reconstructed = eval(repr(graph_via_adjacency_matrix_example))

    assert reconstructed == graph_via_adjacency_matrix_example
