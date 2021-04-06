import numpy as np

from StructuralCausalModels.directed_graph import DirectedGraph
from StructuralCausalModels.structural_equation import StructuralEquation
from StructuralCausalModels.structural_causal_model import StructuralCausalModel


class InvalidWeightedAdjacencyMatrix(Exception):
    """Raised if the weighted adjacency matrix does not define a directed graph.
    """
    pass


class InvalidNumberOfExogenousVariables(Exception):
    """Raised if the number of exogenous variables provided is incorrect.

    By incorrect is meant that the number of exogenous variables provided is
    inconsistent with the number of variables expected in the SCM.
    """
    pass


class LinearStructuralCausalModel(StructuralCausalModel):
    """A class to represent linear Structural Causal Models.

    Beware, does not check the equation are linear.

    Parameters
    ----------
    nb_var : int
        The number of variables in the SCM.
    structural_equations : list
        The list of the structural equations defining the SCM.
    name : str, optional
        The name of the SCM (default is '').
    """

    def __init__(self, name, nb_var, structural_equations):
        super().__init__(name=name,
                         nb_var=nb_var,
                         structural_equations=structural_equations)

    @staticmethod
    def create_from_coefficient_matrix(matrix, causal_order,
                                       exogenous_variables, name=''):
        """Creates a linear SCM from a coefficient matrix.

        The coefficient matrix is interpreted as the weighted adjacency matrix
        of the graph associated to a linear SCM.

        Parameters
        ----------
        matrix : numpy.ndarray
            The weighted adjacency matrix of the graph associated to the linear
            SCM to build.
        causal_order : array_like
            A causal order of the graph associated to the SCM.
        exogenous_variables : list
            The list of the exogenous variables. Note that the list must be
            ordered in the "natural" way - not necessarily in the causal
            ordering. In other terms, exogenous_varoables[0] contains the
            exogenous variables for the structural equation that has :math:`X_0`
            on its left-hand side etc.
        name : str, optional
            The name of the linear SCM created (default is '').

        Returns
        -------
        LinearStructuralCausalModel
            The linear SCM corresponding to the weighted adjacency matrix
            provided.

        Raises
        ------
        InvalidWeightedAdjacencyMatrix
            If the weighted adjacency matrix provided defines a graph that is
            not a directed graph.
        InvalidNumberOfExogenousVariables
            If the number of exogenous variables provided does not correspond to
            the number of variables expected from the matrix provided.
        """

        # Check that the matrix is a valid weighted adjacency matrix for a
        # directed graph
        binarised_matrix = matrix.copy()
        binarised_matrix[binarised_matrix != 0] = 1
        if not DirectedGraph.validate_directed_graph_adjacency_matrix(
                binarised_matrix):
            msg = "The graph induced by the matrix is not a directed graph !"
            raise InvalidWeightedAdjacencyMatrix(msg)

        # Check the number of exogenous variables provided is correct
        nb_var = len(exogenous_variables)
        m = matrix.shape[0]
        if nb_var != m:
            msg = f"{nb_var} exogenous variables provided. Exactly {m} needed !"
            raise InvalidNumberOfExogenousVariables(msg)

        structural_equations = []

        for i in causal_order:

            index_lhs = i
            indices_rhs = sorted(np.where(matrix[:, i] != 0)[0].tolist())
            exogenous_variable = exogenous_variables[i]

            def generate_partial_function(lhs_index, rhs_indices):

                def func(u, *inputs):
                    if not inputs:
                        return u
                    else:
                        res = u.astype(float)
                        for j in range(len(rhs_indices)):
                            # TODO are we sure the right coeff will always go
                            #  with the right input ?
                            res += matrix[rhs_indices[j], lhs_index] * inputs[j]
                        return res

                return func

            f = generate_partial_function(index_lhs, indices_rhs)

            structural_equation = StructuralEquation(
                index_lhs=index_lhs,
                indices_rhs=indices_rhs,
                exogenous_variable=exogenous_variable,
                function=f
            )
            structural_equations.append(structural_equation)

        linear_scm = LinearStructuralCausalModel(
            name=name,
            nb_var=m,
            structural_equations=structural_equations
        )

        return linear_scm
