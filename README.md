# FPGA Tool Performance Visualization Library (FTPVL)
![Python application](https://github.com/TypingKoala/FPGA-Tool-Performance-Visualization-Library/workflows/Python%20application/badge.svg)

<img src="https://raw.githubusercontent.com/TypingKoala/FPGA-Tool-Performance-Visualization-Library/master/examples/images/singletablevisualizer.png" alt="Single Table Visualization" width="100%">

FTPVL is a library for simplifying the data collection and visualization process
for Symbiflow development. Although it was made with Symbiflow in mind, it is
highly extensible for future integration with other software.

## Example Usage
Take a look at the notebooks below to demonstrate the functionality of FTPVL.

1. [Using `HydraFetcher` and Processors](https://colab.research.google.com/drive/1BIQ-iulDFpzcve7lGJPwLePJ5ETBJ6Ut?usp=sharing)
2. [Styling tables with `SingleTableVisualizer`](https://colab.research.google.com/drive/1u3EnmIYnTBk-LXZhqNHt_h4aMuq-_cWq?usp=sharing)
3. [Comparing two different Evaluations](https://colab.research.google.com/drive/1I7InmA6210vIIwdQ7TGHE6aF_WwIm1dM?usp=sharing)

## Documentation
Doucmentation of this library is generated in the `docs/` folder by reading
the docstrings from the source code.
The website is generated using [Sphinx](https://www.sphinx-doc.org/en/master/)
using the [Read the Docs theme](https://github.com/readthedocs/sphinx_rtd_theme).

```bash
pip install -r requirements.txt
cd docs
make html
```

## Dependencies
The library extensively uses [Pandas](https://pandas.pydata.org/) for data
management and processing. Other dependencies are explained below:
* `pandas`: for data management and processing
* `seaborn`: for colormap generation
* `jinja2`: for visualization generation

### Development Dependencies
* `requests-mock`: for mocking request object for testing fetchers
* `pylint`: for linting
* `pytest`: testrunner
* `coverage`: for coverage testing
* `black`: for auto-formatting
* `sphinx`: for documentation generation
* `sphinx-rtd-theme`: for documentation generation (theme)

