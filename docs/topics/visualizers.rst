.. _topics-visualizers:

===========
Visualizers
===========

Overview
========
`Visualizers` bring the data to life by creating a displayable representation
of one or more :ref:`topics-evaluation`. 

Version Info
============
You can choose to show the version info of each test result by setting the
``version_info`` parameter to True (which is False by default). This results in
the display of the version info that is provided by Hydra.


Displaying the Visualizaton
============================
After instantiating the desired visualizer, you can call the 
``get_visualization()`` method to return an object that can be displayed in an 
IPython notebook by calling the ``display()`` function (`documentation`_).

.. autofunction:: ftpvl.visualizers.Visualizer.get_visualization

.. _documentation: https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html#IPython.display.display