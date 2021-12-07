# Simframe

[![Documentation Status](https://readthedocs.org/projects/simframe/badge/?version=latest)](https://simframe.readthedocs.io/en/latest/?badge=latest) 
![GitHub](https://img.shields.io/github/license/stammler/simframe) 
[![status](https://joss.theoj.org/papers/0ef61e034c57445e846b2ec383c920a6/status.svg)](https://joss.theoj.org/papers/0ef61e034c57445e846b2ec383c920a6) 
![PyPI - Downloads](https://img.shields.io/pypi/dm/simframe?label=PyPI%20downloads)

### Framework for scientific simulations

`Simframe` is a Python framework to facilitate scientific simulations. The scope of the software is to provide a framework which can hold data fields, which can be used to integrate differential equations, and which can read and write data files.

Data fields are stored in modified `numpy.ndarray`s. Therefore, `Simframe` can only work with data, that can be stored in `NumPy` arrays.

## Installation

`pip install simframe`

## Documentation

[https://simframe.readthedocs.io/](https://simframe.readthedocs.io/)

1. [Simple Integration](https://simframe.readthedocs.io/en/latest/1_simple_integration.html)
2. [Advanced Integration](https://simframe.readthedocs.io/en/latest/2_advanced_integration.html)
3. [Updating Groups and Fields](https://simframe.readthedocs.io/en/latest/3_updating.html)
4. [Custom Integration Schemes](https://simframe.readthedocs.io/en/latest/4_custom_schemes.html)
5. [Adaptive Integration Schemes](https://simframe.readthedocs.io/en/latest/5_adaptive_schemes.html)
6. [Implicit Integration](https://simframe.readthedocs.io/en/latest/6_implicit_integration.html)
7. [Coupled Oscillators](https://simframe.readthedocs.io/en/latest/7_coupled_oscillators.html)

[Module Reference](https://simframe.readthedocs.io/en/latest/api.html)

## Contributing

To contribute to the software, please read the [contribution guidelines](https://github.com/stammler/simframe/blob/master/.github/CONTRIBUTING.md).

## Ackowledgements

`simframe` has received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme under grant agreement No 714769.

`simframe` was developed at the [University Observatory](https://www.usm.uni-muenchen.de/index_en.php) of the [Ludwig Maximilian University of Munich](https://www.en.uni-muenchen.de/index.html).
