# FPGA-Tool-Performance-Visualization-Library

Example usage: 
```python
# specify how to convert toolchains to synthesis_tool/pr_tool
toolchain_map = {
    'vpr': ('yosys', 'vpr'),
    'vpr-fasm2bels': ('yosys', 'vpr'),
    'yosys-vivado': ('yosys', 'vivado'),
    'vivado': ('vivado', 'vivado'),
    'nextpnr-ice40': ('yosys', 'nextpnr'),
    'nextpnr-xilinx': ('yosys', 'nextpnr'),
    'nextpnr-xilinx-fasm2bels': ('yosys', 'nextpnr')
}

df_types = {
    "project": str,
    "device": str,
    "toolchain": str,
    "freq": float,
    "bram": int,
    "carry": int,
    "dff": int,
    "iob": int,
    "lut": int,
    "pll": int,
    "synthesis": float,
    "pack": float,
    "place": float,
    "route": float,
    "fasm": float,
    "bitstream": float,
    "total": float
}

# define the pipeline to process the evaluation
processing_pipeline = [
    StandardizeTypes(df_types),
    CleanDuplicates(sort=["freq"], subset=["project", "toolchain"], keep="last"),
    AddRelativeFrequency(groupby="project"),
    ExpandToolchain(toolchain_map),
    Reindex(["project", "synthesis_tool", "pr_tool", "toolchain"]),
    SortIndex(["project", "synthesis_tool"])
]

# fetch and process first eval
eval1 = HydraFetcher(eval_num=0).get_evaluation()
eval1 = eval1.process(processing_pipeline)

# fetch and process second eval
eval2 = HydraFetcher(eval_num=1).get_evaluation()
eval2 = eval2.process(processing_pipeline)

# create a color map style to define how to convert from float to CSS
cmap = sns.diverging_palette(180, 0, s=75, l=75, sep=100, as_cmap=True)
cmap_style = ColorMapStyler(cmap)

# transform evaluations to a table of floats and apply color map style
style_processing_pipeline = [NormalizeAround("synthesis_tool", "vivado")]
style1 = eval1.process(style_processing_pipeline).process([cmap_style])
style2 = eval1.process(style_processing_pipeline).process([cmap_style])

# create visualizer and display with version_info
viz1 = SingleTableVisualizer(eval1, style1, version_info=True)
viz1.display()

# create visualizer and display without version_info
viz2 = SingleTableVisualizer(eval2, style2, version_info=False)
viz2.display()

# create style for a visualization that compares two evals
comparison_style_pipeline = [CompareTwo(eval1, eval2)]
style_compare = eval2.process(comparison_style_pipeline).get_style(cmap_style)

# create visualizer and display table that compares two evals
compare_viz = TwoTableVisualizer(eval1, eval2,  version_info=True)
compare_viz.display()
```