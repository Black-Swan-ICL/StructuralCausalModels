from enum import Enum


class EdgeType(Enum):
    NONE = 'no edge'
    FORWARD = '->'
    BACKWARD = '<-'
    UNDIRECTED = '--'


class GraphsCannotBeCompared(Exception):

    pass


class ImpossibleEdgeConfiguration(Exception):

    pass


class GraphViaEdges:

    # TODO parameter validation
    def __init__(self, edges, name=''):
        self.edges = edges
        self.name = name

    # TODO document
    @staticmethod
    def compute_penalty(edge_1, edge_2):

        if edge_1 == edge_2:
            return 0
        elif {edge_1, edge_2} == {EdgeType.NONE, EdgeType.FORWARD}:
            return 1
        elif {edge_1, edge_2} == {EdgeType.NONE, EdgeType.BACKWARD}:
            return 1
        elif {edge_1, edge_2} == {EdgeType.NONE, EdgeType.UNDIRECTED}:
            return 1
        elif {edge_1, edge_2} == {EdgeType.FORWARD, EdgeType.BACKWARD}:
            return 1
        elif {edge_1, edge_2} == {EdgeType.FORWARD, EdgeType.UNDIRECTED}:
            return 1
        elif {edge_1, edge_2} == {EdgeType.BACKWARD, EdgeType.UNDIRECTED}:
            return 1
        else:
            raise ImpossibleEdgeConfiguration

    # TODO document
    def structural_hamming_distance(self,
                                    other,
                                    penalty_edge_mismatch_func=None):

        edges_1 = self.edges
        edges_2 = other.edges
        if penalty_edge_mismatch_func is None:
            penalty_edge_mismatch_func = GraphViaEdges.compute_penalty

        if set(edges_1.keys()) != set(edges_2.keys()):
            msg = 'The Structural Hamming Distances cannot be computed : the '
            msg += 'graphs cannot be compared.'
            raise GraphsCannotBeCompared(msg)

        shd = 0

        for key in edges_1.keys():

            shd += penalty_edge_mismatch_func(
                edge_1=edges_1[key],
                edge_2=edges_2[key]
            )

        return shd

    # TODO __str__ method
    # TODO __repr__ method
    # TODO __eq__ method
