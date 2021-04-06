import copy
import numpy as np
import pandas as pd

from StructuralCausalModels.dag import DirectedAcyclicGraph


class InconsistentStructuralCausalModelDefinition(Exception):
    """Raised if the Structural Causal Model is not defined in a consistent way.
    """
    pass


class CyclicityWarning(UserWarning):
    """Raised if there is a high probability that the SCM contains a cycle.
    """
    pass


class InvalidIntervention(Exception):
    """Raised if the intervention attempted is invalid.
    """
    pass


# TODO allow cycles in init yes/no ?
# TODO add string representation of Structural Causal Model
class StructuralCausalModel:
    """A class to represent Structural Causal Models (SCMs).

    As an "extra security", the number of variables must be provided in addition
    to the structural equations ; the number of variables must be equal to the
    number of structural equations.

    Parameters
    ----------
    nb_var : int
        The number of variables in the SCM.
    structural_equations : list
        The list of the structural equations defining the SCM.
    name : str, optional
        The name of the SCM (default is '').

    Raises
    ------
    InconsistentStructuralCausalModelDefinition
        If the number of structural equations provided does not correspond to
        the number of variables in the SCM.
    CyclicityWarning
            If the SCM defined is (highly likely to be) cyclic.
    """

    def __init__(self, nb_var, structural_equations, name=''):

        if nb_var != len(structural_equations):
            msg = 'There should be as many structural equations as there are '
            msg += 'variables in the SCM !'
            raise InconsistentStructuralCausalModelDefinition(msg)

        self.name = name
        self.nb_var = nb_var
        self.structural_equations = structural_equations

        # Checks whether the SCM defined may be cyclic
        self.check_no_cycles()

    def generate_data(self, nb_samples):
        """Generates samples from an SCM.

        Parameters
        ----------
        nb_samples : int
            The number of samples to generate.

        Returns
        -------
        pandas.DataFrame
            A dataframe containing the samples.

            The column names correspond to the variables in the SCM. Thus column
            0 contains the samples for :math:`X_0`, column 1 the samples for
            :math:`X_1` etc.
        """

        index = range(nb_samples)
        columns = [i for i in range(self.nb_var)]
        data = pd.DataFrame(
            np.empty((nb_samples, self.nb_var,)),
            index=index,
            columns=columns
        )
        for structural_equation in self.structural_equations:
            data = structural_equation.generate_data(data)

        return data

    def adjacency_matrix(self):
        """Generates the adjacency matrix of the graph corresponding to the SCM.

        Returns
        -------
        numpy.ndarray
            The adjacency matrix of the graph corresponding to the SCM.
        """

        nb_nodes = len(self.structural_equations)
        adjacency_matrix = np.zeros(shape=(nb_nodes, nb_nodes))

        for structural_equation in self.structural_equations:

            parents = structural_equation.indices_rhs
            child = structural_equation.index_lhs

            for parent in parents:

                adjacency_matrix[parent, child] = 1

        adjacency_matrix = adjacency_matrix.astype(int)

        return adjacency_matrix

    def check_no_cycles(self, atol=1e-6):
        """Checks that the SCM defined is not cyclic.

        Note that this function is essentially a wrapper around static method
        DirectedAcyclicGraph.validate_dag_adjacency_matrix, which relies on
        characterisation of acyclicity by the nilpotence of the adjacency
        matrix.

        As eigenvalues are only ever computed approximately, it is theoretically
        possible than an eigenvalue is computed as very small but non-zero even
        though it is actually zero hence the use of a tolerance.

        Parameters
        ----------
        atol : float, optional
            The absolute tolerance used to check that the eigenvalues are all
            equal to 0 (default is :math:`10^{-6}`).

        Raises
        ------
        CyclicityWarning
            If the SCM is (highly likely to be) cyclic.
        """

        adjacency_matrix = self.adjacency_matrix()

        if not DirectedAcyclicGraph.validate_dag_adjacency_matrix(
                adjacency_matrix, atol):

            msg = "The SCM defined is very likely to be cyclic. Beware !"

            raise CyclicityWarning(msg)

    def perform_intervention(self, new_structural_equation):
        """Performs an intervention on the SCM.

        Performs an intervention on the SCM by replacing one of its constitutive
        structural equations by a new structural equation.

        Parameters
        ----------
        new_structural_equation : StructuralEquation
            The new structural equation.

        Returns
        -------
        StructuralCausalModel
            The post-intervention SCM.

        Raises
        ------
        InvalidIntervention
            If the new structural equation does not correspond to an existing
            one i.e. it has :math:`X_{i_0}` on its left-hand side but there is
            no :math:`X_{i_0}` variable in the SCM.
        CyclicityWarning
            If the post-intervention SCM is (highly likely to be) cyclic.
        """

        target_node = new_structural_equation.index_lhs
        nodes_and_indices = dict()
        for i in range(len(self.structural_equations)):
            nodes_and_indices[self.structural_equations[i].index_lhs] = i
        existing_nodes = nodes_and_indices.keys()

        if target_node not in existing_nodes:
            # We do not allow interventions to create new (i.e. non previously
            # existing) nodes in the (DAG associated to the) SCM
            msg = "The target node does not exist in the SCM !"
            raise InvalidIntervention(msg)

        # TODO should also test the variables in the RHS in the new eq are in
        #  the SCM

        idx_target_node = nodes_and_indices[target_node]
        new_scm = copy.deepcopy(self)
        new_scm.structural_equations[idx_target_node] = new_structural_equation

        # Check whether the intervention may have created a cycle in the SCM
        new_scm.check_no_cycles()

        return new_scm
