import pytest
import numpy as np

from scipy.stats import randint

from StructuralCausalModels.structural_equation import StructuralEquation
from StructuralCausalModels.structural_causal_model import StructuralCausalModel, \
    InvalidIntervention

_constant_0 = 1
_constant_1 = 2
_constant_2 = -4
_constant_3 = 0


@pytest.fixture
def nb_samples():

    return 1000


@pytest.fixture
def deterministic_scm():
    """
    Defines an SCM in which all th exogenous variables are constant. This will
    allow a degree of checks on the construction of SCMs via the class defined
    to be carried out.
    """
    # X_0 = epsilon_0, where epsilon_0 = constant_0
    def f_0(u, *args):
        return u
    constant_0 = _constant_0
    epsilon_0 = randint(low=constant_0, high=(constant_0 + 1))
    equation_0 = StructuralEquation(0, [], epsilon_0, f_0)

    # X_3 = X_0 +  epsilon_3, where epsilon_3 = constant_3
    def f_3(u, x):
        return (u + np.power(x, 1)).flatten()
    constant_3 = _constant_3
    epsilon_3 = randint(low=constant_3, high=(constant_3 + 1))
    equation_3 = StructuralEquation(3, [0], epsilon_3, f_3)

    # X_1 = X_0 - X_3 + epsilon_1, where epsilon_1 = constant_1
    def f_1(u, x, y):
        return u + x - y
    constant_1 = _constant_1
    epsilon_1 = randint(low=constant_1, high=(constant_1 + 1))
    equation_1 = StructuralEquation(1, [0, 3], epsilon_1, f_1)

    # X_2 = X_0 - X_3 + X_1 + epsilon_2, where epsilon_2 = constant_2
    def f_2(u, x, y, z):
        return u + x - y + z
    constant_2 = _constant_2
    epsilon_2 = randint(low=constant_2, high=(constant_2 + 1))
    equation_2 = StructuralEquation(2, [0, 3, 1], epsilon_2, f_2)

    equations = [equation_0, equation_3, equation_1, equation_2]

    scm = StructuralCausalModel('deterministic_scm', len(equations), equations)

    return scm


@pytest.fixture
def deterministic_scm_data_generation_function(deterministic_scm, nb_samples):

    data = np.zeros(shape=(nb_samples, deterministic_scm.nb_var))
    data[:, 0] = _constant_0
    data[:, 3] = data[:, 0] + _constant_3
    data[:, 1] = data[:, 0] - data[:, 3] + _constant_1
    data[:, 2] = data[:, 0] - data[:, 3] + data[:, 1] + _constant_2

    return data


@pytest.fixture
def deterministic_scm_adjacency_matrix():

    adjacency_matrix = np.asarray([
        [0, 1, 1, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]
    ])

    return adjacency_matrix


@pytest.fixture
def new_structural_equation():

    # X_2 = X_1 + epsilon_2, where epsilon_2 = constant_2
    def f_2(u, z):
        return u + z
    constant_2 = _constant_2
    epsilon_2 = randint(low=constant_2, high=(constant_2 + 1))
    equation_2 = StructuralEquation(2, [1], epsilon_2, f_2)

    return equation_2


@pytest.fixture
def post_intervention_deterministic_scm_data_generation_function(
        deterministic_scm, nb_samples):

    data = np.zeros(shape=(nb_samples, deterministic_scm.nb_var))
    data[:, 0] = _constant_0
    data[:, 3] = data[:, 0] + _constant_3
    data[:, 1] = data[:, 0] - data[:, 3] + _constant_1
    data[:, 2] = data[:, 1] + _constant_2

    return data


@pytest.fixture
def post_intervention_deterministic_scm_adjacency_matrix():

    adjacency_matrix = np.asarray([
        [0, 1, 0, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 0, 0]
    ])

    return adjacency_matrix


@pytest.fixture
def invalid_new_structural_equation():

    # X_4 = X_1 + epsilon_4, where epsilon_4 = 0
    def f_4(u, z):
        return u + z
    constant_4 = 0
    epsilon_4 = randint(low=constant_4, high=(constant_4 + 1))
    equation_4 = StructuralEquation(4, [1], epsilon_4, f_4)

    return equation_4


def test_correct_functionals(deterministic_scm, nb_samples,
                             deterministic_scm_data_generation_function):

    actual_data = deterministic_scm.generate_data(nb_samples).values

    expected_data = deterministic_scm_data_generation_function

    assert np.equal(actual_data, expected_data).all()


def test_correct_adjacency_matrix(deterministic_scm,
                                  deterministic_scm_adjacency_matrix):

    actual_adjacency_matrix = deterministic_scm.adjacency_matrix()

    assert np.equal(actual_adjacency_matrix,
                    deterministic_scm_adjacency_matrix).all()


def test_perform_intervention(
        deterministic_scm, new_structural_equation, nb_samples,
        post_intervention_deterministic_scm_data_generation_function,
        post_intervention_deterministic_scm_adjacency_matrix):

    new_scm = deterministic_scm.perform_intervention(new_structural_equation)

    # Check the data generated is what is expected
    actual_data = new_scm.generate_data(nb_samples).values
    expected_data = post_intervention_deterministic_scm_data_generation_function

    generated_data_correct = np.equal(actual_data, expected_data).all()

    # Check that the new adjacency matrix would be what is expected
    actual_adjacency_matrix = new_scm.adjacency_matrix()

    adjacency_matrix_correct = np.equal(
        actual_adjacency_matrix,
        post_intervention_deterministic_scm_adjacency_matrix).all()

    assert generated_data_correct and adjacency_matrix_correct


def test_invalid_intervention(deterministic_scm,
                              invalid_new_structural_equation):

    with pytest.raises(InvalidIntervention):

        deterministic_scm.perform_intervention(invalid_new_structural_equation)
