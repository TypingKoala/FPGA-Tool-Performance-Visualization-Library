""" Evaluations store the test results from a single execution of the test suite. """

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

    def process(self, pipeline: List['Processor']) -> 'Evaluation':
        """
        Executes each processor in the pipeline and returns a new Evaluation.

        Args
        -------
            pipeline: a list of Processors to process the Evaluation in order

        Returns:
            an Evaluation instance that was processed by the pipeline
        """
        result = self
        for processor in pipeline:
            result = processor.process(result)
        return result
