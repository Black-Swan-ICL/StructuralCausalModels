from enum import Enum


class EdgeType(Enum):
    NONE = 'no edge'
    FORWARD = '->'
    BACKWARD = '<-'
    UNDIRECTED = '--'

    def __repr__(self):
        """
        Returns a string representation of the object from which it can be
        rebuilt.

        Returns
        -------
        str
            A string representation of the object from which it can be rebuilt.
        """
        return f"EdgeType.{self.name}"


class GraphsCannotBeCompared(Exception):

    pass


class ImpossibleEdgeConfiguration(Exception):

    pass


class GraphViaEdges:

    # TODO parameter validation
    # TODO document
    def __init__(self, edges, name=''):
        self.edges = edges
        self.name = name

    @staticmethod
    def compute_penalty(edge_1, edge_2):
        """
        Provides a default method to compute the penalty incurred when two edges
        are of a same type or of different types.

        Parameters
        ----------
        edge_1 : EdgeType
            The first edge.
        edge_2 : EdgeType
            The second edge.

        Returns
        -------
        float
            The penalty incurred.
        """

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

    def structural_hamming_distance(self,
                                    other,
                                    penalty_edge_mismatch_func=None):
        """
        Computes the Structual Hamming Distance between two graphs. By default
        it is equal to the number of edges in the graphs that are not of the
        same type. A different weighted scheme for penalty computation may be
        provided (we may want to penalise the presence of an edge in the
        opposite direction more than the absence of an edge, for example).

        Parameters
        ----------
        other : GraphViaEdges
            The graph to compare.
        penalty_edge_mismatch_func : callable
            The edge mismatch penalty scheme.

        Returns
        -------
        float
            The Structural Hamming Distance (SHD), in its default form or under
            a user-provided edge mismatch penalty scheme.

        Raises
        ------
        GraphsCannotBeCompared
            Raised if the graphs do not have the same vertex set.
        """

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

    def __str__(self):
        """
        Returns a user-friendly string representation of the object.

        Returns
        -------
        str
            A user-friendly string representation of the object.
        """
        s = f"GraphViaEdges '{self.name}',\nedges :\n"
        for edge, edgetype in self.edges.items():
            s += f"    {edge[0]} {edgetype.value} {edge[1]}\n"

        return s

    def __repr__(self):
        """
        Returns a string representation of the object from which it can be
        rebuilt.

        Returns
        -------
        str
            A string representation of the object from which it can be rebuilt.
        """
        s = f"GraphViaEdges(name={repr(self.name)}, "
        s += f"edges={repr(self.edges)})"

        return s

    def __eq__(self, other):
        """
        Checks whether the object is equal to another GraphViaEdges object. Two
        GraphViaEdges objects are equal if they have the same edges and the same
        names.

        Parameters
        ----------
        other : GraphViaEdges
            The other GraphViaEdges object.

        Returns
        -------
        bool
            Whether the two GraphViaEdges objects are equal.
        """
        if self.edges != other.edges:
            return False

        if self.name != other.name:
            return False

        return True
