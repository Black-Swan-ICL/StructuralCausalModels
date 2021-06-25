from copy import deepcopy
from StructuralCausalModels.graph import Graph


class PC:

    def __init__(self):
        pass

    @staticmethod
    def build_skeleton_and_separation_sets(data, ci_test_func):

        skeleton = Graph(
            adjacency_matrix=None
        )
        separation_sets = dict()

        return skeleton, separation_sets

    @staticmethod
    def orient_skeleton(skeleton, separation_sets):

        cpdag = deepcopy(skeleton)

        return cpdag

    @staticmethod
    def perform_causal_structure_discovery(data, ci_test_func):

        skeleton, separation_sets = PC.build_skeleton_and_separation_sets(
            data=data,
            ci_test_func=ci_test_func
        )

        cpdag = PC.orient_skeleton(skeleton=skeleton,
                                   separation_sets=separation_sets)

        return cpdag
