""" This module defines fetchers for ftpvl. """
from typing import Any

import pandas as pd
from ftpvl import Evaluation

class Fetcher():
    """
    This is a superclass for all fetchers.

    Fetchers allow the user to retrieve test data from a data source and output
    it in a standard format for use by other tools in the library.
    """

    def __init__(self) -> None:
        pass

    def _download(self) -> Any:
        """
        Retrieves evaluation data over the internet.
        """
        raise NotImplementedError

    def _preprocess(self, data: Any) -> pd.DataFrame:
        """
        Given the downloaded data, process the data and return the resulting
        dataframe.
        """
        raise NotImplementedError

    def get_evaluation(self) -> Evaluation:
        """
        Returns an Evaluation that represents the fetched data.
        """
        data = self._download()
        df = self._preprocess(data)
        return Evaluation(df)


class HydraFetcher(Fetcher):
    """
    Download and preprocess test results from `hydra.vtr.tools`.

    Attributes:
        eval_num: A non-negative integer for the evaluation number to download,
            with `0` being the latest evaluation
        mapping: An optional dictionary mapping input column names to output
            column names. If empty, does not remap the fetched data.
    """

    def __init__(self, eval_num: int = 0, mapping: dict = None) -> None:
        """
        Inits HydraFetcher with eval_num and mapping.
        """
        super().__init__()
        self.eval_num = eval_num
        self.mapping = {} if mapping is None else mapping

    def _download(self) -> Any:
        """
        Fetches data from Hydra.

        Overrides Fetcher._download().
        """
        # TODO
        raise NotImplementedError

    def _preprocess(self, data: Any) -> pd.DataFrame:
        """
        Using data from _download(), processes and standardizes the data and
        returns a Pandas DataFrame.

        Overrides Fetcher._preprocess().
        """
        # TODO
        raise NotImplementedError

# class GCSFetcher(Fetcher):
