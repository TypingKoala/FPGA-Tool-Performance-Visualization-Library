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
Extensive documentation, including a *Getting Started* guide, is available on
[ReadTheDocs](https://ftpvl.readthedocs.io).

Documentation of this library is generated in the `docs/` folder by reading
the docstrings from the source code.
The website is generated using [Sphinx](https://www.sphinx-doc.org/en/master/)
using the [Read the Docs theme](https://github.com/readthedocs/sphinx_rtd_theme).

```bash
pip install -r requirements.txt
cd docs
make html
```

## Dependencies
* `pandas`: for data management and processing ([website](https://pandas.pydata.org/))
* `seaborn`: for colormap generation ([website](https://seaborn.pydata.org/))
* `jinja2`: for visualization generation ([website](https://jinja.palletsprojects.com/))

### Development Dependencies
* `requests-mock`: for mocking request object for testing fetchers ([website](https://requests-mock.readthedocs.io/en/latest/))
* `pylint`: for linting ([website](https://www.pylint.org/))
* `pytest`: testrunner ([website](https://docs.pytest.org/en/stable/))
* `coverage`: for coverage testing ([website](https://coverage.readthedocs.io/))
* `black`: for auto-formatting ([website](https://github.com/psf/black))
* `sphinx`: for documentation generation ([website](https://www.sphinx-doc.org/en/master/))
* `sphinx-rtd-theme`: for documentation generation (theme) ([website](https://github.com/readthedocs/sphinx_rtd_theme))

## Changes
### 0.1.5
* Added support for custom projects and jobsets in HydraFetcher.

### 0.1.4
* Added RelativeDiff processor.
* Updated some internal docstrings

