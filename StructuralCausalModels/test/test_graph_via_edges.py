import pytest

from StructuralCausalModels.graph_via_edges import EdgeType, GraphViaEdges

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
