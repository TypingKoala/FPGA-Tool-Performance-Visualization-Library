""" Defines helper functions useful for classes """
from typing import Union

def flatten(input_dict: dict) -> dict:
    """
    Given an input dictionary that may contain nested dictionaries, return
    a new dictionary that is flattened such that there are no dictionary
    values. Keys in the returned dictionary are a period-delimited list of
    the keys used to index the original dictionary.

    Example: {"a": {"b": "c"}} => {"a.b": "c"}
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
    the versions in that object
    """
    return {k:v for k, v in obj.items() if k.startswith("versions.")}


def rescale_actual_freq(freq: Union[int, float]) -> Union[int, float]:
    """
    Given an int or float, returns frequency in megahertz by autoscaling
    """
    one_mhz = 1_000_000
    if freq > one_mhz:
        return freq / one_mhz
    else:
        return freq


def get_actual_freq(obj: dict, hydra_clock_names: list = None):
    """
    Given an object decoded from meta.json, return the actual frequency
    as an integer in megahertz.
    """
    # set default clock names
    if hydra_clock_names is None:
        hydra_clock_names = ["clk", "sys_clk", "clk_i"]

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
        max_freq_keys = [x for x in obj.keys() if
                         x.startswith("max_freq.") and x.endswith(".actual")]
        if len(max_freq_keys) > 0:
            shortest_clock_name = min(max_freq_keys, key=len)
            return rescale_actual_freq(obj[shortest_clock_name])
        else:
            return None

def get_styling(val, cmap):
    """
    Given a value, returns a CSS string with the background-color set to the
    color in the cmap, or an empty CSS string if the value is not a float
    between 0 and 1.
    """
    if isinstance(val, float) and 0 <= val <= 1:
        color = tuple([int(x * 255) for x in cmap(val)[:-1]])
        hex_color = '#%02x%02x%02x' % color # convert to hex format #FFFFFF
        return "background-color: {}".format(hex_color)
    else:
        return ""
