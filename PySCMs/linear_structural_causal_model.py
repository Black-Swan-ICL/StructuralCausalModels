import numpy as np

from PySCMs.graph_utilities import validate_directed_graph
from PySCMs.structural_equation import StructuralEquation
from PySCMs.structural_causal_model import StructuralCausalModel


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
        if not validate_directed_graph(binarised_matrix):
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
# if __name__ == '__main__':
#
#     from scipy.stats import randint
#
#     _constant_0 = 1
#     _constant_1 = 0
#     _constant_2 = 100
#     _constant_3 = 0
#
#     nb_samples = 5
#
#     def matrix_coefficients():
#         """
#         The matrix of coefficients from which to build the linear SCM (i.e. its
#         weighted adjacency matrix) modulo the exogenous variables.
#         """
#         mat = np.asarray([
#             [0, -2, 4, 2],
#             [0, 0, -8, 0],
#             [0, 0, 0, 0],
#             [0, 0.5, 1.5, 0]
#         ])
#
#         return mat
#
#
#     def exogenous_variables():
#         exogenous_variables = [randint(low=_constant_0, high=(_constant_0 + 1)),
#                                randint(low=_constant_1, high=(_constant_1 + 1)),
#                                randint(low=_constant_2, high=(_constant_2 + 1)),
#                                randint(low=_constant_3, high=(_constant_3 + 1))]
#
#         return exogenous_variables
#
#
#     linear_scm = LinearStructuralCausalModel.create_from_coefficient_matrix(
#         name='test linear scm',
#         matrix=matrix_coefficients(),
#         causal_order=[0, 3, 1, 2],
#         exogenous_variables=exogenous_variables())
#
#     actual_data = linear_scm.generate_data(nb_samples).values