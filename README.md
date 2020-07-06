# FPGA Tool Performance Visualization Library (FTPVL)
![Python application](https://github.com/TypingKoala/FPGA-Tool-Performance-Visualization-Library/workflows/Python%20application/badge.svg)

FTPVL is a library for simplifying the data collection and visualization process
for Symbiflow development. Although it was made with Symbiflow in mind, it is
highly extensible for future integration with other software.

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

## Example Usage
Take a look at the notebooks below to demonstrate the functionality of FTPVL.

1. [Using `HydraFetcher` and `DebugVisualizer`](https://colab.research.google.com/drive/1BIQ-iulDFpzcve7lGJPwLePJ5ETBJ6Ut?usp=sharing)