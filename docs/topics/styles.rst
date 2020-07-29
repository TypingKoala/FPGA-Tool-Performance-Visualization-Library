.. _topics-styles:

======
Styles
======

Overview
========
`Styles` are a special subclass of :ref:`topics-processors` that transform the values 
inside an :ref:`topics-evaluation` into CSS styles. The output of a Style can
then be used with certain :ref:`topics-visualizers` to add color to the final
display.

Using Colormaps
===============
The :ref:`topics-api-colormapstyle` style takes a `Matplotlib Colormap`_ as a
parameter, which allows for the background color of each cell to be dependent on
the value inside it. Since `Colormaps` expect the input value to be between 0 and 1,
we usually have a processor in the pipeline before applying the Style. This is
demonstrated in the :ref:`intro-styling` section of the :ref:`intro-firststeps`
guide.

.. _Matplotlib Colormap: https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html