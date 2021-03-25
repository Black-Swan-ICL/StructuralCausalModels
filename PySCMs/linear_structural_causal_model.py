import numpy as np

from PySCMs.graph_utilities import validate_directed_graph
from PySCMs.structural_equation import StructuralEquation
from PySCMs.structural_causal_model import StructuralCausalModel


class InvalidConstruction(Exception):

    pass


class LinearStructuralCausalModel(StructuralCausalModel):

    def __init__(self, name, nb_var, structural_equations):
        super().__init__(name, nb_var, structural_equations)

    @staticmethod
    def create_from_coefficient_matrix(name, matrix, exogenous_variables):

        # Check that the matrix is a valid weighted adjacency matrix for a
        # directed graph
        binarised_matrix = matrix
        binarised_matrix[binarised_matrix != 0] = 1

        # Check the number of exogenous variables provided is correct
        nb_var = len(exogenous_variables)
        m = matrix.shape[0]
        if nb_var != m:

            msg = f"{nb_var} exogenous variables provided. Need exactly {m} !"
            raise InvalidConstruction(msg)

        structural_equations = []

        for i in range(m):

            index_lhs = i
            indices_rhs = np.where(matrix[:, i] != 0)[0].tolist()
            indices_rhs.sort()
            exogenous_variable = exogenous_variables[i]

            def scalar_f(u, arr_variables):

                if len(indices_rhs) == 0:
                    res = u
                else:
                    res = u + np.dot(matrix[indices_rhs, i], arr_variables)

                return res

            def f(u, *arr_variables):

                res = np.zeros_like(u)
                for i in range(len(u)):

                    scalar_variables = [variable[i] for variable in
                                        arr_variables]
                    res[i] = scalar_f(u[i], scalar_variables)

                return res

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


if __name__ == '__main__':

    from scipy.stats import randint

    _constant_0 = 1
    _constant_1 = 0
    _constant_2 = 100
    _constant_3 = 0

    nb_samples = 1000

    def matrix_coefficients():
        """
        The matrix of coefficients from which to build the linear SCM (i.e. its
        weighted adjacency matrix) modulo the exogenous variables.
        """
        mat = np.asarray([
            [0, -2, 4, 2],
            [0, 0, -8, 0],
            [0, 0, 0, 0],
            [0, 0.5, 1.5, 0]
        ])

        return mat


    def exogenous_variables():
        exogenous_variables = [randint(low=_constant_0, high=(_constant_0 + 1)),
                               randint(low=_constant_1, high=(_constant_1 + 1)),
                               randint(low=_constant_2, high=(_constant_2 + 1)),
                               randint(low=_constant_3, high=(_constant_3 + 1))]

        return exogenous_variables


    linear_scm = LinearStructuralCausalModel.create_from_coefficient_matrix(
        name='test linear scm',
        matrix=matrix_coefficients(),
        exogenous_variables=exogenous_variables())

    actual_data = linear_scm.generate_data(nb_samples).values
