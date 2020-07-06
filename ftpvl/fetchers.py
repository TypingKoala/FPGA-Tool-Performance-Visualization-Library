""" This module defines fetchers for ftpvl. """
from typing import Any, List, Dict
import requests

import pandas as pd
from ftpvl.evaluation import Evaluation
import ftpvl.helpers as Helpers

class Fetcher():
    """
    This is a superclass for all fetchers.

    Fetchers allow the user to retrieve test data from a data source and output
    as an Evaluation for use by other tools in the library.
    """

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
    Represents a downloader and preprocessor of test results from
    `hydra.vtr.tools`.

    Attributes:
        eval_num: A non-negative integer for the evaluation number to download,
            with `0` being the latest evaluation
        mapping: An optional dictionary mapping input column names to output
            column names. If empty, does not remap the fetched data.
        hydra_clock_names: An optional ordered list of strings used in finding
            the actual frequency for each build result.
    """

    def __init__(self, eval_num: int = 0, mapping: dict = None,
                 hydra_clock_names: list = None) -> None:
        """
        Inits HydraFetcher with eval_num and mapping.
        """
        self.eval_num = eval_num
        self.mapping = mapping
        self.hydra_clock_names = hydra_clock_names

    def _download(self) -> List[Dict]:
        """
        Fetches data from Hydra, returning a list of decoded meta.json dicts
        corresponding to the builds of the eval_num evaluation.

        Overrides Fetcher._download().
        """
        # get build numbers from eval_num
        resp = requests.get(
            'https://hydra.vtr.tools/jobset/dusty/fpga-tool-perf/evals',
            headers={'Content-Type': 'application/json'})
        if resp.status_code != 200:
            raise ConnectionError("Unable to get evals.")
        evals_json = resp.json()
        if self.eval_num >= len(evals_json['evals']):
            raise IndexError(f"Invalid eval_num: {self.eval_num}")
        build_nums = evals_json['evals'][self.eval_num]['builds']

        # collect the 'meta.json' build products
        data = []
        for build_num in build_nums:
            resp = requests.get(
                f'https://hydra.vtr.tools/build/{build_num}/download/1/meta.json',
                headers={'Content-Type': 'application/json'})
            if resp.status_code != 200:
                print("Warning:", f"Unable to get build {build_num}")
                # raise ConnectionError(f"Unable to get build {build_num}")
            else:
                data += [resp.json()]

        return data

    def _preprocess(self, data: List[Dict]) -> pd.DataFrame:
        """
        Using data from _download(), processes and standardizes the data and
        returns a Pandas DataFrame.

        Overrides Fetcher._preprocess().
        """
        flattened_data = [Helpers.flatten(x) for x in data]

        processed_data = []
        for row in flattened_data:
            processed_row = {}
            if self.mapping is None:
                processed_row = row
            else:
                for in_col_name, out_col_name in self.mapping.items():
                    processed_row[out_col_name] = row[in_col_name]
            processed_row["freq"] = Helpers.get_actual_freq(row,
                                                            self.hydra_clock_names)
            processed_row.update(Helpers.get_versions(row))
            processed_data.append(processed_row)

        return pd.DataFrame(processed_data).dropna(axis=1, how='all')


class JSONFetcher(Fetcher):
    """
    Represents a loader and preprocessor of test results from local storage.

    Attributes:
        path: A string file path pointing to the dataframe JSON file.
        mapping: An optional dictionary mapping input column names to output
            column names. If empty, does not remap the fetched data.
    """

    def __init__(self, path: str, mapping: dict = None) -> None:
        """
        Inits FeatherFetcher with path and mapping.
        """
        self.path = path
        self.mapping = mapping

    def _download(self) -> str:
        """
        Retrieves evaluation data over the internet.
        """
        return self.path

    def _preprocess(self, path: str) -> pd.DataFrame:
        """
        Given the path, load the data in pandas, process the data, and return
        the resulting dataframe.
        """
        df = pd.read_json(path)
        if self.mapping is None:
            return df
        else:
            return (df.filter(items=self.mapping.keys())
                    .rename(columns=self.mapping))
