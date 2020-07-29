.. _topics-fetchers:

========
Fetchers
========

Overview
========
`Fetchers` serve as a convenient way to ingest information from a source and
create an :ref:`topics-evaluation`. Sources can either be local or over the
network.

Fetching from Hydra
===================
You can fetch from `Hydra`_ by using the :ref:`topics-api-hydrafetcher` fetcher. 
Its functionality is explained in the :ref:`intro-fetching` section of the
:ref:`intro-firststeps` guide.


Fetching from a JSON dataframe
==============================
You can also fetch from a properly-formatted JSON dataframe by using the 
:ref:`topics-api-jsonfetcher` fetcher and specifying the path to the JSON file 
in the parameter. This is useful if some pre-processing needs to be performed,
or the test runner is able to output a dataframe as a build artifact.

Most commonly, this fetcher can import JSON-encoded dataframes if they are 
exported from a separate Pandas dataframe. Learn about exporting as a 
`JSON file from Pandas`_.

Getting the Evaluation
======================
To get the :ref:`topics-evaluation` object from the Fetcher, call the
``get_evaluation()`` method.

.. automethod:: ftpvl.fetchers.Fetcher.get_evaluation


.. _Hydra: https://hydra.vtr.tools
.. _JSON file from Pandas: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html