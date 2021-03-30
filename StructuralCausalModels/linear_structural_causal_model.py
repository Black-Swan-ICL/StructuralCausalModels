import numpy as np

from StructuralCausalModels.directed_graph import DirectedGraph
from StructuralCausalModels.structural_equation import StructuralEquation
from StructuralCausalModels.structural_causal_model import StructuralCausalModel


class InvalidWeightedAdjacencyMatrix(Exception):

    pass


class InvalidNumberOfExogenousVariables(Exception):

    pass


class LinearStructuralCausalModel(StructuralCausalModel):

    def __init__(self, name, nb_var, structural_equations):
        super().__init__(name, nb_var, structural_equations)

    @staticmethod
    def create_from_coefficient_matrix(name, matrix, causal_order,
                                       exogenous_variables):

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

            def generate_partial_function(index_lhs, indices_rhs):

                def func(u, *inputs):
                    if not inputs:
                        return u
                    else:
                        res = u.astype(float)
                        for j in range(len(indices_rhs)):
                            # TODO are we sure the right coeff will always go
                            #  with the right input ?
                            res += matrix[indices_rhs[j], index_lhs] * inputs[j]
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
