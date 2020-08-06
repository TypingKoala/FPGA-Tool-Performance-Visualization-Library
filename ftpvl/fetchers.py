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
    project : str
        The project name to use when fetching from Hydra
    jobset : str
        The jobset name to use when fetching from Hydra
    eval_num : int, optional
        An integer that specifies the evaluation to download. Functionality
        differs depending on whether `absolute_eval_num` is True, by default 0
    absolute_eval_num : bool, optional
        Flag that specifies if the eval_num is an absolute identifier instead of
        a relative identifier. If True, the fetcher will find an evaluation
        with the exact ID in `eval_num`. If False, `eval_num` should be a
        non-negative integer with `0` being the latest evaluation and `1` being
        the second latest evaluation, etc. By default False.
    mapping : dict, optional
        A dictionary mapping input column names to output
        column names, if needed for remapping, by default None
    hydra_clock_names : list, optional
        An optional ordered list of strings used in finding
        the actual frequency for each build result, by default None
    """

    def __init__(
        self,
        project: str,
        jobset: str,
        eval_num: int = 0,
        absolute_eval_num: bool = False,
        mapping: dict = None,
        hydra_clock_names: list = None
    ) -> None:
        super().__init__()
        self.project = project
        self.jobset = jobset
        self.eval_num = eval_num
        self.absolute_eval_num = absolute_eval_num
        self.mapping = mapping
        self.hydra_clock_names = hydra_clock_names

    def _get_builds(self, eval_num: int, absolute_eval_num: bool, params: str = "") -> List[int]:
        """
        Recursive function that returns a list of build numbers given an eval_num
        and whether it is an absolute eval num.

        Parameters
        ----------
        eval_num : int
            An integer that specifies the evaluation to download. Functionality
            differs depending on whether `absolute_eval_num` is True
        absolute_eval_num : bool
            Flag that specifies if the eval_num is an absolute identifier instead of
            a relative identifier. If True, the fetcher will find an evaluation
            with the exact ID in `eval_num`. If False, `eval_num` should be a
            non-negative integer with `0` being the latest evaluation and `1` being
            the second latest evaluation, etc.
        params : str
            A string of query parameters used when fetching the evaluations.
            Most commonly used for pagination. By default, "".

        Returns
        -------
        List[int]
            A list of builds that correspond with the eval_num

        Raises
        ------
        ConnectionError
            Raised if the HTTP request to get the evaluations fails.
        IndexError
            Raised if the relative eval_num is not valid.
        ValueError
            Raised if the eval_num has no associated builds.
        """
        resp = requests.get(
            f"https://hydra.vtr.tools/jobset/{self.project}/{self.jobset}/evals{params}",
            headers={"Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            raise ConnectionError("Unable to get evals from server.")
        evals_json = resp.json()
        
        if not self.absolute_eval_num: # if relative eval_num
            if eval_num >= len(evals_json["evals"]):
                # check if there is a second page
                if "next" in evals_json:
                    return self._get_builds(
                        eval_num - len(evals_json["evals"]),
                        absolute_eval_num,
                        evals_json["next"] # query param for next page
                    )
                else:
                    raise IndexError(f"Invalid eval_num: {self.eval_num}")
            self._eval_id = evals_json["evals"][eval_num]["id"]
            return evals_json["evals"][eval_num]["builds"]
            
        else: # if absolute eval_num
            self._eval_id = self.eval_num
            for eval_data in evals_json["evals"]:
                if eval_data["id"] == self.eval_num:
                    return eval_data["builds"]
            if "next" in evals_json:
                return self._get_builds(
                    eval_num,
                    absolute_eval_num,
                    evals_json["next"] # query param for next page
                )
            else: # if couldn't find ID and there is no next page
                raise ValueError(f"Unable to find eval_num {eval_num}")

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
        build_nums = self._get_builds(self.eval_num, self.absolute_eval_num)

        # fetch build info and download 'meta.json'
        data = []
        for build_num in build_nums:
            # get build info
            resp = requests.get(
                f"https://hydra.vtr.tools/build/{build_num}",
                headers={"Content-Type": "application/json"},
            )
            if resp.status_code != 200:
                raise Exception(f"Unable to get build {build_num}, got status code {resp.status_code}.")
            
            decoded = None
            try:
                decoded = resp.json()
            except json.decoder.JSONDecodeError as err:
                raise Exception(f"Unable to decode build {build_num} JSON file, {str(err)}")
                
            # check if build was successful
            if decoded.get("buildstatus") != 0:
                print(f"Warning: Build {build_num} failed with non-zero exit. Skipping...")
                continue

            # check if meta.json exists
            meta_json_id = None
            for product_id, product_desc in decoded.get("buildproducts", {}).items():
                if product_desc.get("name", "") == "meta.json":
                    meta_json_id = product_id
            
            if meta_json_id is None:
                print(f"Warning: Build {build_num} does not contain meta.json file. Skipping...")
                continue
            
            # download meta.json
            resp = requests.get(
                f"https://hydra.vtr.tools/build/{build_num}/download/{meta_json_id}/meta.json",
                headers={"Content-Type": "application/json"},
            )
            if resp.status_code != 200:
                print(
                    "Warning:",
                    f"Unable to get build {build_num} meta.json file.",
                )
                continue
            try:
                data.append(resp.json())
            except json.decoder.JSONDecodeError:
                print("Warning:", f"Unable to decode build {build_num}")

        if len(data) == 0:
            raise ValueError(f"Unable to get any successful builds from eval_num {self.eval_num}.")

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
