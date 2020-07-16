.. _topics-evaluation:

==========
Evaluation
==========

Overview
========
Evaluations store the test results from a single execution of the test suite.
They are constructed either using :ref:`topics-fetchers` or manually by specifying
a Pandas dataframe and evaluation ID. 

Processing
==========
Evaluations can be processed by using the ``process()`` method. Its only
parameter is a list of :ref:`topics-processors` that will be used to
transform the evaluation one-at-a-time.

.. automethod:: ftpvl.evaluation.Evaluation.process

Extracting the internal dataframe
=================================
Evaluations store the test results internally using a Pandas dataframe. You can
retrive this dataframe by using the ``get_df()`` method.

.. automethod:: ftpvl.evaluation.Evaluation.get_df