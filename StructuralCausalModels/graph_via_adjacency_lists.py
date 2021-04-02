class InvalidAdjacencyLists(Exception):
    pass


class GraphViaAdjacencyLists:
    """
    Implements a graph structure representing an adjacency list representation.
    """

    def __init__(self, nb_vertices, adjacency_lists, name=''):

        if not len(adjacency_lists) == nb_vertices:
            msg = 'There should be as many adjacency lists as vertices !'
            raise InvalidAdjacencyLists(msg)

        self.name = name
        self.nb_vertices = nb_vertices
        self.adjacency_lists = adjacency_lists
        self.indegrees = []
        for i in range(self.nb_vertices):
            count = sum([int(i in adj_l) for adj_l in self.adjacency_lists])
            self.indegrees.append(count)

    def __str__(self):
        """
        Returns a user-friendly string representation of the object.

        Returns
        -------
        str
            A user-friendly string representation of the object.
        """
        s = f"AlternativeGraph '{self.name}', {self.nb_vertices} vertices, "
        s += f"adjacency lists:\n{self.adjacency_lists}"

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
        s = f"GraphViaAdjacencyLists(nb_vertices={repr(self.nb_vertices)}, "
        s += f"adjacency_lists={repr(self.adjacency_lists)}, "
        s += f"name={repr(self.name)})"

        return s

    def __eq__(self, other):
        """
        Checks whether the object is equal to another AlternativeGraph object.
        The two objects are equal if they have the same number of vertices, the
        same adjacency lists and the same names.

        Parameters
        ----------
        other : GraphViaAdjacencyLists
            The other AlternativeGraph object.

        Returns
        -------
        bool
            Whether the objects are equal.
        """

        if self.nb_vertices != other.nb_vertices:
            return False

        if len(self.adjacency_lists) != len(other.adjacency_lists):
            return False
        else:
            for l1, l2 in zip(self.adjacency_lists, other.adjacency_lists):
                if set(l1) != set(l2):
                    return False

        if self.name != other.name:
            return False

        return True