# TODO reorganise and document
import pytest

from StructuralCausalModels.graph_via_edges import EdgeType, GraphViaEdges


@pytest.fixture
def graph_via_edges_example():

    example = GraphViaEdges(
        edges={
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
        name=''
    )

    return example


@pytest.mark.parametrize(
    "edge_1, edge_2, expected_penalty",
    [
        (EdgeType.FORWARD, EdgeType.FORWARD, 0),
        (EdgeType.UNDIRECTED, EdgeType.NONE, 1),
    ]
)
def test_compute_penalty_edge_mismatch(edge_1, edge_2, expected_penalty):

    actual_penalty = GraphViaEdges.compute_penalty(edge_1, edge_2)

    assert actual_penalty == expected_penalty


def test_can_rebuild_graph_from_edges(graph_via_edges_example):

    reconstructed = eval(repr(graph_via_edges_example))

    assert reconstructed == graph_via_edges_example
