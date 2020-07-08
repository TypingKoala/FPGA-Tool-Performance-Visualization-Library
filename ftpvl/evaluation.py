""" This module defines evaluations for ftpvl. """

from typing import List, Union

import pandas as pd

class Evaluation():
    """
    This class represents one evaluation of the FPGA-tool-perf tests.

    It stores the results in a dataframe, which can be transformed using a
    processing pipeline. The columns of the dataframe are standardized for all
    Evaluation instances.

    Methods:
        get_df(): returns a copy of the dataframe that represents the evaluation
        process(pipeline): given a list of processors, returns an Evaluation
            after it has been processed by all processors
    """

    def __init__(self, df: pd.DataFrame, eval_id: int = None):
        """
        Init Evaluation with dataframe.
        """
        self._df = df
        self._eval_id = eval_id

    def get_df(self) -> pd.DataFrame:
        """
        Returns a copy of the Pandas DataFrame that represents the evaluation
        """
        return self._df.copy()

    def get_eval_id(self) -> Union[int, None]:
        """
        Returns the eval_id if specified, otherwise None
        """
        return self._eval_id

    def process(self, pipeline: List['Processor']) -> 'Evaluation':
        """
        Executes each processor in the pipeline and returns a new Evaluation.

        Args:
            pipeline: a list of Processors to process the Evaluation in order

        Returns:
            an Evaluation instance that was processed by the pipeline
        """
        result = self
        for processor in pipeline:
            result = processor.process(result)
        return result
