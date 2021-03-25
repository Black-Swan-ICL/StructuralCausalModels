import numpy as np


def validate_adjacency_matrix(matrix):
    """
    Checks that a matrix is an adjacency matrix (i.e. a square matrix containing
    only 0's and 1's).

    Parameters
    ----------
    matrix : array_like
        The matrix to check.

    Returns
    -------
    bool
        Whether the matrix is a valid adjacency matrix.
    """
    if len(matrix.shape) != 2:

        return False

    if matrix.shape[0] != matrix.shape[1]:

        return False

    if not np.all(np.logical_or(matrix == 1, matrix == 0)):

        return False

    return True


def validate_directed_graph(matrix):
    """
    Checks that a matrix is a valid adjacency matrix for a directed graph.

    Parameters
    ----------
    matrix : array_like
        The matrix to check.

    Returns
    -------
    bool
        Whether the matrix to check is a valid adjacency matrix for a directed
        graph.
    """
    if not validate_adjacency_matrix(matrix):

        return False

    # Check that there are no self-loops
    no_self_loops = np.asarray([matrix[i, i] == 0 for i in
                                range(matrix.shape[0])])
    if not np.all(no_self_loops):
        return False

    # Check that there are no undirected edges
    for i in range(matrix.shape[0]):
        for j in range(i):
            if matrix[i, j] == 1 and matrix[j, i] == 1:
                return False

    return True


def validate_directed_acyclic_graph(matrix, atol=1e-6):
    """
    Checks that a matrix is a valid adjacency matrix for a directed acyclic
    graph. Uses the characterisation of acyclicity established by D. Wei, T.
    Gao and Y. Yu in "DAGs with No Fears : A Closer Look at Continuous
    Optimization for Learning Bayesian Networks" (2020) : a directed graph is
    acyclic if and only if its adjacency matrix is nilpotent.

    Parameters
    ----------
    matrix : array_like
        The matrix to check.
    atol : float
        The absolute tolerance used to check that the eigenvalues are all equal
        to 0.

    Returns
    -------
    bool
        Whether the matrix to check is a valid adjacency matrix for a directed
        acyclic graph.
    """
    if not validate_directed_graph(matrix):

        return False

    eigenvalues = np.linalg.eigvals(matrix)
    comparand = np.zeros_like(eigenvalues)

    return np.allclose(eigenvalues, comparand, atol=atol)
