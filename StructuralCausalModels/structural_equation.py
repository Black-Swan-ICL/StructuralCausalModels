# TODO document
# TODO add string representation of Structural Equation
class StructuralEquation:

    def __init__(self, index_lhs, indices_rhs, exogenous_variable, function):
        self.index_lhs = index_lhs
        self.indices_rhs = indices_rhs
        self.exogenous_variable = exogenous_variable
        self.function = function

    def generate_data(self, data):
        sample_size = data.shape[0]
        inputs = [data.loc[:, i].values for i in self.indices_rhs]
        data.loc[:, self.index_lhs] = self.function(
            self.exogenous_variable.rvs(size=sample_size),
            *inputs
        )

        return data
