``simframe`` Documentation
=========================================

| ``simframe`` is a Python framework to facilitate scientific simulations. The scope of the software is to provide a framework which can hold data fields, which can be used to integrate differential equations, and which can read and write data files.

| Data fields are stored in modified ``numpy.ndarrays``. Therefore, ``simframe`` can only work with data, that can be stored in ``NumPy`` arrays.

| To install ``simframe`` simply type
| ``pip install simframe``

| Please have a look at the following examples to learn how to use ``simframe``.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   1_simple_integration
   2_advanced_integration
   3_updating
   4_custom_schemes
   5_adaptive_schemes
   6_implicit_integration
   example_coupled_oscillators
   example_double_pendulum
   example_compartmental_models
   A_citation
   B_contrib_bug_feature
   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
