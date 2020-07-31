""" Evaluations store the test results from a single execution of the test suite. """

from functools import reduce
from typing import List, Union
import pandas as pd

class Evaluation():
    """
    A collection of test results from a single evaluation of a piece
    of software on one or more test cases.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe that contains the test results of the given evaluation,
        rows for each test case and columns for each recorded metric

    eval_id : int, optional
        The ID number of the evaluation, by default None
    """

    def __init__(self, df: pd.DataFrame, eval_id: int = None):
        self._df = df
        self._eval_id = eval_id

    def get_df(self) -> pd.DataFrame:
        """
        Returns a copy of the Pandas DataFrame that represents the evaluation
        """
        return self._df.copy()

    def get_eval_id(self) -> Union[int, None]:
        """
        Returns the ID number of the evaluation if specified, otherwise None
        """
        return self._eval_id
    
    def get_copy(self) -> 'Evaluation':
        """
        Returns a deep copy of the Evaluation instance
        """
        return Evaluation(self.get_df(), self.get_eval_id())

    def process(self, pipeline: List['Processor']) -> 'Evaluation':
        """
        Executes each processor in the pipeline and returns a new Evaluation.

        Args
        -------
            pipeline: a list of Processors to process the Evaluation in order

        Returns:
            an Evaluation instance that was processed by the pipeline
        """
        return reduce(lambda r, p: p.process(r), pipeline, self)

    def __add__(self, other: 'Evaluation') -> 'Evaluation':
        """
        Magic method for concatenating two Evaluations, returning an Evaluation
        with dataframe (self + other).

        Args
        ------
            other: the other Evaluation to concatenate
        
        Returns:
            a new Evaluation that consists of the two Evaluations concatenated
        """
        if not isinstance(other, Evaluation):
            raise TypeError(f"can only concatenate Evaluation (not {type(other).__name__}) to Evaluation")
        new_df = pd.concat([self.get_df(), other.get_df()], ignore_index=True)
        return Evaluation(new_df)

    def __radd__(self, other: 'Evaluation') -> 'Evaluation':
        """
        Magic method for reverse concatenating two Evaluations, returning an
        Evaluation with dataframe (other + self).

        Args
        ------
            other: the other Evaluation to concatenate
        
        Returns:
            a new Evaluation that consists of the two Evaluations concatenated
        """
        # handle default start value of sum() is `0`
        if other == 0:
            return self.get_copy()
        return self.__add__(other)