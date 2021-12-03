---
title: 'Simframe: A Python Framework for Scientific Simulations'
tags:
  - Python
  - Jupyter Notebook
  - NumPy
  - SciPy
authors:
  - name: Sebastian M. Stammler^[corresponding author]
    orcid: 0000-0002-1589-1796
    affiliation: 1
  - name: Tilman Birnstiel
    orcid: 0000-0002-1899-8783
    affiliation: 1
affiliations:
  - name: University Observatory, Faculty of Physics, Ludwig-Maximilians-Universität München, Scheinerstr. 1, 81679 Munich, Germany
    index: 1
date: 11 August 2021
bibliography: paper.bib
---

# Summary

`Simframe` is a Python framework to facilitate scientific simulations. It can be used to easily integrate differential equations.

Conceptually, upon initialization `Simframe` is an empty frame that can be filled with `Field`s containing the data. `Field`s are derived from `numpy.ndarray`s [@harris2020Natur.585..357H], but with extended functionality. The user can then specify differential equations to those data fields and can set up an integrator which is integrating those fields according the given differential equations.

Fields that should not be integrated but are still required for the model can be assigned an update function, according to which they will be updated once per integration step.

`Simframe` contains a number of integration schemes of different orders, both for explicit and implicit integration. Furthermore, `Simframe` includes methods to read and write output files.

Due to its modular structure, `Simframe` can be extended at will, for example, by implementing new integration schemes and/or user-defined output formats.

# Statement of need

Solving differential equations is part of the daily work of scientists. `Simframe` facilitates this by providing the infrastructure: Data structures, integration schemes, and methods to write and read output files.

On one hand, `Simframe` can be used to quickly solve small scientific problems, and, on the other hand, can be easily extended to larger projects due to its versatility and modular structure.

Furthermore, `Simframe` is ideal for beginners without programming experience who are taking their first steps in solving differential equations. It can therefore be used to design lectures or practical courses at schools and universities, as it allows students to concentrate on the essentials without having to write larger programs on their own.

While plenty of ODE solver packages exist, `Simframe` offers a flexible framework to define, group, and describe data, define how it is updated, use existing integrators or define new ones, and to handle writing of data or serializing the entire simulation object, all in one modular package.

# Features

## Data fields

The data fields of `Simframe` are subclassed `NumPy` `ndarray`s. The full `NumPy` functionality can therefore be used on `Simframe` data fields. The `ndarray`s have been extended to store additional information about differential equations or update functions and a string description of the field.

## Integration schemes

`Simframe` includes a number of integration schemes by default. All of the implemented schemes are Runge-Kutta methods of different orders. Some of the methods are adaptive, i.e., they are embedded Runge-Kutta methods, that return an optimal step size for the integration variable, such that the desired accuracy is achieved. The implicit methods require a matrix inversion that is either done directly by `NumPy` or by using the GMRES solver provided by `SciPy`.

Here is a list of all implemented integration schemes:

| Order | Scheme                      |          |          | solver |
| :---: | --------------------------- | :------: | :------: | ------ |
|   1   | Euler                       | explicit |          |        |
|   1   | Euler                       | implicit |          | direct |
|   1   | Euler                       | implicit |          | GMRES  |
|   2   | Fehlberg                    | explicit | adaptive |        |
|   2   | Heun                        | explicit |          |        |
|   2   | Heun-Euler                  | explicit | adaptive |        |
|   2   | midpoint                    | explicit |          |        |
|   2   | midpoint                    | implicit |          | direct |
|   2   | Ralston                     | explicit |          |        |
|   3   | Bogacki-Shampine            | explicit | adaptive |        |
|   3   | Gottlieb-Shu                | explicit | adaptive |        |
|   3   | Heun                        | explicit |          |        |
|   3   | Kutta                       | explicit |          |        |
|   3   | Ralston                     | explicit |          |        |
|   3   | Strong Stability Preserving | explicit |          |        |
|   4   | 3/8 rule                    | explicit |          |        |
|   4   | Ralston                     | explicit |          |        |
|   4   | Runge-Kutta                 | explicit |          |        |
|   5   | Cash-Karp                   | explicit | adaptive |        |
|   5   | Dormand-Prince              | explicit | adaptive |        |

## I/O

By default `Simframe` has two options for storing simulation results. One is by storing the data in a separate namespace within the `Simframe` object itself, useful for small simulations to access results without writing/reading data files. Another one is by storing the data in HDF5 data files using the `h5py` package.

If configured by the user, `Simframe` is writing dump files, from which the simulation can be resumed, in case the program crashed unexpectedly. These dump files are serialized `Simframe` objects using the `dill` package.

# Acknowledgements

The authors acknowledge funding from the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme under grant agreement No 714769 and funding by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) under Ref no. FOR 2634/1 and under Germany's Excellence Strategy - EXC-2094 - 390783311.

# References