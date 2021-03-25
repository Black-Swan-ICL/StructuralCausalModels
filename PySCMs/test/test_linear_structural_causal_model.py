import pytest
import numpy as np

from scipy.stats import randint

from PySCMs.linear_structural_causal_model import LinearStructuralCausalModel


_constant_0 = 1
_constant_1 = 0
_constant_2 = 100
_constant_3 = 0


@pytest.fixture
def nb_samples():

    return 1000


@pytest.fixture
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


@pytest.fixture
def exogenous_variables():

    exogenous_variables = [randint(low=_constant_0, high=(_constant_0 + 1)),
                           randint(low=_constant_1, high=(_constant_1 + 1)),
                           randint(low=_constant_2, high=(_constant_2 + 1)),
                           randint(low=_constant_3, high=(_constant_3 + 1))]

    return exogenous_variables


@pytest.fixture
def linear_scm_data_generation_function(nb_samples, matrix_coefficients,
                                        exogenous_variables):
    data = np.zeros(shape=(nb_samples, matrix_coefficients.shape[0]))
    data[:, 0] = _constant_0
    data[:, 3] = matrix_coefficients[0, 3]*data[:, 0] + _constant_3
    data[:, 1] = (matrix_coefficients[0, 1]*data[:, 0] +
                  matrix_coefficients[3, 1]*data[:, 3] + _constant_1)
    data[:, 2] = (matrix_coefficients[0, 2]*data[:, 0] +
                  matrix_coefficients[3, 2]*data[:, 3] +
                  matrix_coefficients[1, 2]*data[:, 1] + _constant_2)

    return data


def test_create_from_coefficient_matrix(nb_samples, matrix_coefficients,
                                        exogenous_variables,
                                        linear_scm_data_generation_function):

    linear_scm = LinearStructuralCausalModel.create_from_coefficient_matrix(
        name='test linear scm',
        matrix=matrix_coefficients,
        exogenous_variables=exogenous_variables)

    actual_data = linear_scm.generate_data(nb_samples).values

    expected_data = linear_scm_data_generation_function

    assert np.equal(actual_data, expected_data).all()