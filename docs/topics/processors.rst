.. _topics-processors:

==========
Processors
==========

Overview
========
`Processors` transform an evaluation to make it easier to draw conclusions
from the data. They are useful in converting test data fetched using a
:ref:`topics-fetchers` into the desired format for visualization.

One example of a processor is ``Normalize``, which normalizes all specified test
metrics around zero to improve the understandability of the results.


Processing Pipelines
====================
Processors can be chained together to form a *processing pipeline*, which is
a list of processors that are used one after the other to transform an
Evaluation.

Here is an example of the processing pipeline that is used in the 
:ref:`intro-firststeps` guide::

    processing_pipeline = [
        StandardizeTypes(df_types),
        CleanDuplicates(
            duplicate_col_names=["project", "toolchain"],
            sort_col_names=["freq"]),
        AddNormalizedColumn(
            groupby="project", 
            input_col_name="freq", 
            output_col_name="normalized_max_freq"),
        ExpandColumn(
            input_col_name="toolchain", 
            output_col_names=("synthesis_tool", "pr_tool"),
            mapping=toolchain_map),
        Reindex(["project", "synthesis_tool", "pr_tool", "toolchain"]),
        SortIndex(["project", "synthesis_tool"])
    ]