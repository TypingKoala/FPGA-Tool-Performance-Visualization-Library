""" Implement testes for Style class """

import pandas as pd
import seaborn as sns
from pandas.testing import assert_frame_equal

from ftpvl.evaluation import Evaluation
from ftpvl.styles import ColorMapStyle


class TestStyle:
    """
    Testing by partition.

    ColorMapStyle()
        process()
    """
    def test_colormapstyle_process(self):
        cmap = sns.diverging_palette(180, 0, s=75, l=75, sep=100, as_cmap=True)
        df = pd.DataFrame([
            {"a": 0.1, "b": 0.2, "c": 0.3},
            {"a": 0.4, "b": 0.5, "c": 0.6},
            {"a": 0.7, "b": 0.8, "c": 0.9}
        ])
        eval1 = Evaluation(df)
        style = ColorMapStyle(cmap)
        pipeline = [style]

        result = eval1.process(pipeline).get_df()
        expected = pd.DataFrame([
            {"a": "background-color: #8ed8d0", "b": "background-color: #bde8e3", "c": "background-color: #eaf7f6"},
            {"a": "background-color: #f2f2f2", "b": "background-color: #f2f2f2", "c": "background-color: #f2f2f2"},
            {"a": "background-color: #fbe8eb", "b": "background-color: #f7d1d9", "c": "background-color: #f3bac5"}
        ])
        
        assert_frame_equal(result, expected)
