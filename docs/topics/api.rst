.. _topics-api:

========
Core API
========

.. _topics-api-evaluation:

Evaluation API
==============
.. autoclass:: ftpvl.evaluation.Evaluation
    :members:

.. _topics-api-fetchers:

Fetchers API
============
.. automodule:: ftpvl.fetchers

.. _topics-api-hydrafetcher:

HydraFetcher
************
.. autoclass:: ftpvl.fetchers.HydraFetcher
    :members:

.. _topics-api-jsonfetcher:

JSONFetcher
***********
.. autoclass:: ftpvl.fetchers.JSONFetcher
    :members:

.. _topics-api-processors:

Processors API
==============
.. automodule:: ftpvl.processors

.. autoclass:: ftpvl.processors.AddNormalizedColumn
    :members:

.. autoclass:: ftpvl.processors.CleanDuplicates
    :members:

.. autoclass:: ftpvl.processors.ExpandColumn
    :members:

.. autoclass:: ftpvl.processors.MinusOne
    :members:

.. autoclass:: ftpvl.processors.Normalize
    :members:

.. autoclass:: ftpvl.processors.NormalizeAround
    :members:

.. autoclass:: ftpvl.processors.Reindex
    :members:

.. autoclass:: ftpvl.processors.SortIndex
    :members:

.. autoclass:: ftpvl.processors.StandardizeTypes
    :members:

.. autoclass:: ftpvl.processors.RelativeDiff
    :members:

.. autoclass:: ftpvl.processors.FilterByIndex
    :members:

.. autoclass:: ftpvl.processors.Aggregate
    :members:

.. autoclass:: ftpvl.processors.GeomeanAggregate
    :members:

.. autoclass:: ftpvl.processors.CompareToFirst

.. _topics-api-styles:

Styles API
==========
.. automodule:: ftpvl.styles

.. _topics-api-colormapstyle:

ColorMapStyle
*************
.. autoclass:: ftpvl.styles.ColorMapStyle
    :members:

.. _topics-api-visualizers:

Visualizers API
===============
.. automodule:: ftpvl.visualizers

.. autoclass:: ftpvl.visualizers.DebugVisualizer
    :members:

.. autoclass:: ftpvl.visualizers.SingleTableVisualizer
    :members:

Enums
=====
Direction
*********
.. autoclass:: ftpvl.processors.Direction
    :members:

    .. autoattribute:: MAXIMIZE
    
        Indicates that the corresponding metric is optimized by 
        *maximizing* the value
    
    .. autoattribute:: MINIMIZE
    
        Indicates that the corresponding metric is optimized by
        *minimizing* the value
