import numpy as np
import pandas as pd

from StructuralCausalModels.dag import DirectedAcyclicGraph


class CyclicityWarning(UserWarning):

    pass


class InvalidIntervention(Exception):

    pass


# TODO document
# TODO allow cycles in init yes/no ?
# TODO validation of attributes
# TODO add string representation of Structural Causal Model
class StructuralCausalModel:

    def __init__(self, name, nb_var, structural_equations):
        self.name = name
        self.nb_var = nb_var
        self.structural_equations = structural_equations

    def generate_data(self, nb_samples):

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

        nb_nodes = len(self.structural_equations)
        adjacency_matrix = np.zeros(shape=(nb_nodes, nb_nodes))

        for structural_equation in self.structural_equations:

            parents = structural_equation.indices_rhs
            child = structural_equation.index_lhs

            for parent in parents:

                adjacency_matrix[parent, child] = 1

        adjacency_matrix = adjacency_matrix.astype(int)

        return adjacency_matrix

    def check_no_cycles(self, atol):

        adjacency_matrix = self.adjacency_matrix()

        if not DirectedAcyclicGraph.validate_dag_adjacency_matrix(
                adjacency_matrix, atol):

            msg = "The SCM defined is very likely to be cyclic. Beware !"

            raise CyclicityWarning(msg)

    def perform_intervention(self, new_structural_equation):

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

        index_target_node = nodes_and_indices[target_node]
        self.structural_equations[index_target_node] = new_structural_equation

        return self
