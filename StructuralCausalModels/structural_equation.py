# TODO add string representation of Structural Equation
class StructuralEquation:
    """A class to represent structural equations.

    Structural Equations are assignments of the sort

    .. math::
        X_{i} := g((X_j)_{j ~\in ~J}, U_i),

    where :math:`U_i` is an exogenous (random) variable.

    Parameters
    ----------
    index_lhs : int
        The index of the structural variable on the left-hand side of the
        structural equation (the ":math:`i`").
    indices_rhs : list
        The indices of the structural variables on the right-hand side of the
        structural equation (the ":math:`j`'s in :math:`J`").
    exogenous_variable : scipy.stats.rv_continuous or scipy.stats.rv_discrete
        The exogenous variable (the ":math:`U_i`").
    function : callable
        The function defining the functional form of the assignment in the
        structural equation (the ":math:`g`").
    """

    def __init__(self, index_lhs, indices_rhs, exogenous_variable, function):
        self.index_lhs = index_lhs
        self.indices_rhs = indices_rhs
        self.exogenous_variable = exogenous_variable
        self.function = function

    def generate_data(self, data):
        """Generates samples from a structural equation.

        Parameters
        ----------
        data : pandas.DataFrame
            A dataframe containing data at least for the structural variables on
            the right-hand side of the structural equation.

            If it contains data for the structural variable on the left-hand
            side of the structural equation, that data will be overwritten.

        Returns
        -------
        pandas.DataFrame
            The samples.
        """
        sample_size = data.shape[0]
        inputs = [data.loc[:, i].values for i in self.indices_rhs]
        data.loc[:, self.index_lhs] = self.function(
            self.exogenous_variable.rvs(size=sample_size),
            *inputs
        )

        return data
