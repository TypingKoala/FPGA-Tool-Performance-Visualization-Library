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
retrieve this dataframe by using the ``get_df()`` method. This can be used to
manipulate the underlying data without needing to use the built-in FTPVL processors.

.. note:: ``get_df()`` returns a defensive copy of the dataframe, so any 
    mutations to the returned dataframe will not be reflected in the original
    Evaluation. Instead, you must instantiate a new ``Evaluation`` by passing
    in the dataframe and evaluation ID.

.. automethod:: ftpvl.evaluation.Evaluation.get_df

Example
*******

.. code-block:: python

    >>> eval1 = Evaluation(pd.DataFrame([{"a": 1, "b": 2}, {"a": 4, "b": 5}]), eval_id=1)
    >>> df = eval1.get_df() # extract Pandas dataframe
    >>> df
        a   b
    0   1   2
    1   4   5
    >>> df["c"] = [3, 6] # add a new column
    >>> eval2 = Evaluation(df, eval_id=eval1.get_eval_id()) # create new evaluation
    >>> eval2.get_df()
        a   b   c
    0   1   2   3
    1   4   5   6