# TODO reorganise and document
import pytest

from StructuralCausalModels.graph_via_adjacency_lists import \
    GraphViaAdjacencyLists


@pytest.fixture
def graph_via_adjacency_lists_example():

    example = GraphViaAdjacencyLists(adjacency_lists=[[1, 2, 3],
                                                      [2],
                                                      [],
                                                      [1, 2]],
                                     nb_vertices=4,
                                     name='')

    return example


def test_can_rebuild_graph_from_lists(graph_via_adjacency_lists_example):

    reconstructed = eval(repr(graph_via_adjacency_lists_example))

    assert reconstructed == graph_via_adjacency_lists_example
