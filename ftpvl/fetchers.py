""" Fetchers are responsible for ingesting and standardizing data for future processing. """
import json
from typing import Any, Dict, List

import pandas as pd
import requests

import ftpvl.helpers as Helpers
from ftpvl.evaluation import Evaluation


class Fetcher:
    """
    This is a superclass for all fetchers.

    Fetchers allow the user to retrieve test data from a data source and output
    as an Evaluation for use by other tools in the library.
    """

    def __init__(self):
        self._eval_id = None

    def _download(self) -> Any:
        """
        Retrieves evaluation data over the internet and returns the data.
        """
        raise NotImplementedError

    def _preprocess(self, data: Any) -> pd.DataFrame:
        """
        Process the data and return the resulting dataframe.
        """
        raise NotImplementedError

    def get_evaluation(self) -> Evaluation:
        """
        Returns an Evaluation that represents the fetched data.
        """
        data = self._download()
        preprocessed_df = self._preprocess(data)
        return Evaluation(preprocessed_df, eval_id=self._eval_id)


class HydraFetcher(Fetcher):
    """
    Represents a downloader and preprocessor of test results from
    `hydra.vtr.tools`.

    Parameters
    ----------
    eval_num : int, optional
        A non-negative integer for the evaluation number to download,
        with `0` being the latest evaluation, by default 0
    mapping : dict, optional
        A dictionary mapping input column names to output
        column names, if needed for remapping, by default None
    hydra_clock_names : list, optional
        An optional ordered list of strings used in finding
        the actual frequency for each build result, by default None
    """

    def __init__(
        self, eval_num: int = 0, mapping: dict = None, hydra_clock_names: list = None
    ) -> None:
        super().__init__()
        self.eval_num = eval_num
        self.mapping = mapping
        self.hydra_clock_names = hydra_clock_names

    def _download(self) -> List[Dict]:
        """
        Fetches data from Hydra, returning a list of decoded meta.json dicts
        corresponding to the builds of the eval_num evaluation.

        Returns
        -------
        List[Dict]
            A list of dictionaries that represent the decoded meta.json files
            of each test result.

        Raises
        ------
        ConnectionError
            Raised if `hydra.vtr.tools` returns a non-200 status code when
            fetching evals.

        IndexError
            Raised if the specified eval_num is invalid due to it being too
            large.

        ValueError
            Raised if all builds in a given eval failed.
        """
        # get build numbers from eval_num
        resp = requests.get(
            "https://hydra.vtr.tools/jobset/dusty/fpga-tool-perf/evals",
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            raise ConnectionError("Unable to get evals from server.")
        evals_json = resp.json()
        if self.eval_num >= len(evals_json["evals"]):
            raise IndexError(f"Invalid eval_num: {self.eval_num}")
        build_nums = evals_json["evals"][self.eval_num]["builds"]

        # collect the 'meta.json' build products
        data = []
        for build_num in build_nums:
            resp = requests.get(
                f"https://hydra.vtr.tools/build/{build_num}/download/1/meta.json",
                headers={"Content-Type": "application/json"},
            )
            if resp.status_code != 200:
                print(
                    "Warning:",
                    f"Unable to get build {build_num}. It might have failed.",
                )
                continue
            try:
                data += [resp.json()]
            except json.decoder.JSONDecodeError:
                print("Warning:", f"Unable to decode build {build_num}")

        if len(data) == 0:
            raise ValueError(f"All builds from eval_num {self.eval_num} failed")

        self._eval_id = evals_json["evals"][self.eval_num]["id"]
        return data

    def _preprocess(self, data: List[Dict]) -> pd.DataFrame:
        """
        Using data from _download(), processes and standardizes the data and
        returns a Pandas DataFrame.
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
            processed_row["freq"] = Helpers.get_actual_freq(row, self.hydra_clock_names)
            processed_row.update(Helpers.get_versions(row))
            processed_data.append(processed_row)

        return pd.DataFrame(processed_data).dropna(axis=1, how="all")
    
    def get_evaluation(self) -> Evaluation:
        return super().get_evaluation()


class JSONFetcher(Fetcher):
    """
    Represents a loader and preprocessor of test results from a JSON file.

    Parameters
    ----------
    path : str
        A string file path pointing to the dataframe JSON file.

    mapping : dict, optional
        An optional dictionary mapping input column names to output
        column names., by default None
    """

    def __init__(self, path: str, mapping: dict = None) -> None:

        super().__init__()
        self.path = path
        self.mapping = mapping

    def _download(self) -> str:
        """
        Returns the path of the JSON file.
        """
        return self.path

    def _preprocess(self, path: str) -> pd.DataFrame:
        """
        Given the path, load the data in pandas, process the data, and return
        the resulting dataframe.
        """
        loaded_df = pd.read_json(path)
        if self.mapping is None:
            return loaded_df
        else:
            return loaded_df.filter(items=self.mapping.keys()).rename(
                columns=self.mapping
            )

    def get_evaluation(self) -> Evaluation:
        return super().get_evaluation()
