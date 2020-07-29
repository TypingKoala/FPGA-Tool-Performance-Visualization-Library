""" Defines helper functions useful for classes """
from typing import Union, Any, Tuple

from ftpvl import settings
from matplotlib.colors import Colormap


def flatten(input_dict: dict) -> dict:
    """
    Given an input dictionary that may contain nested dictionaries, return
    a new dictionary that is flattened such that there are no dictionary
    values.

    Keys in the returned dictionary are a period-delimited list of
    the keys used to index the original dictionary.

    Parameters
    ----------
    input_dict : dict
        a potentially-nested dictionary

    Returns
    -------
    dict
        a new flattened input dictionary
    
    Examples
    --------
    >>> flatten({"a": {"b": "c"}})
    {"a.b": "c"}
    """
    new_dict = {}
    for k_1, v_1 in input_dict.items():
        if isinstance(v_1, dict):
            result = flatten(v_1)
            for k_2, v_2 in result.items():
                combined_key = f"{k_1}.{k_2}"
                new_dict[combined_key] = v_2
        else:
            new_dict[k_1] = v_1
    return new_dict


def get_versions(obj: dict) -> dict:
    """
    Given a flattened object decoded from meta.json, return a dictionary of
    the versions in that object.

    Filters the dictionary for all keys that start with `versions.`

    Parameters
    ----------
    obj : dict
        a flattened dictionary

    Returns
    -------
    dict
        a copy of the input dictionary only containing keys starting with
        `versions.`
    """
    return {k: v for k, v in obj.items() if k.startswith("versions.")}


def rescale_actual_freq(freq: Union[int, float]) -> Union[int, float]:
    """
    Given a frequency with an unspecified unit, returns frequency in megahertz
    by assuming the original unit is hertz if input frequency is greater than 1
    million.

    Parameters
    ----------
    freq : Union[int, float]
        a number that is a frequency

    Returns
    -------
    Union[int, float]
        the input frequency in megahertz
    """
    one_mhz = 1_000_000
    if freq > one_mhz:
        return freq / one_mhz
    else:
        return freq


def get_actual_freq(obj: dict, hydra_clock_names: list = None) -> Union[int, float]:
    """
    Given a flattened object decoded from meta.json, return the actual frequency
    as a number in megahertz.

    Since a meta.json object might contain multiple frequencies, we look through
    all clock names specified in hydra_clock_names and use the first one in the
    list. If none of the specified clock names exists in the object, we use
    the shortest clock name to find the frequency.

    Parameters
    ----------
    obj : dict
        A decoded and flattened meta.json file

    hydra_clock_names : list, optional
        An ordered list of clock names to look for in the obj, by default None

    Returns
    -------
    Union[int, float]
        the frequency of the actual clock specified in the object
    """
    # set default clock names
    if hydra_clock_names is None:
        hydra_clock_names = settings.default_hydra_clock_names

    # if max_freq is unnested
    if "max_freq" in obj:
        return rescale_actual_freq(obj["max_freq"])
    else:
        # check if max_freq contains clock_name in HYDRA_CLOCK_NAMES
        for clock_name in hydra_clock_names:
            key = f"max_freq.{clock_name}.actual"
            if key in obj:
                return rescale_actual_freq(obj[key])

        # if none of those exist, choose the shortest one or return None
        max_freq_keys = [
            x for x in obj.keys() if x.startswith("max_freq.") and x.endswith(".actual")
        ]
        if len(max_freq_keys) > 0:
            shortest_clock_name = min(max_freq_keys, key=len)
            return rescale_actual_freq(obj[shortest_clock_name])
        else:
            return None


def get_styling(val: Any, cmap: Colormap, val_range: Tuple[int, int] = (0, 1)) -> str:
    """
    Given a value between two integers, returns a CSS string with the 
    background-color set to the color in the colormap, or an empty CSS string if
    the value is not a number between the specified range.

    Parameters
    ----------
    val : Any
        A value (possibly non-numeric) that needs to be styled

    cmap : Colormap
        A colormap to use when styling the background

    val_range : Tuple[int, int], optional
        The range that val is in, which is used to determine which color to use 
        in the colormap, by default (0, 1)

    Returns
    -------
    str
        a CSS string specifying the background color based on the color map,
        or an empty string if the val is not a float between 0 and 1.
    """
    if type(val) not in [int, float]:
        return ""
    
    normalized_val = (val - val_range[0]) / (val_range[1] - val_range[0])
    if 0 <= normalized_val <= 1:
        color = tuple([int(x * 255) for x in cmap(normalized_val)[:-1]])
        hex_color = "#%02x%02x%02x" % color  # convert to hex format #FFFFFF
        return "background-color: {}".format(hex_color)
    else:
        return ""
