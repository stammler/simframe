---
title: 'Simframe: A Python Package for Scientific Simulations'
tags:
  - Python
  - Jupyter Notebook
authors:
  - name: Sebastian M. Stammler^[corresponding author]
    orcid: 0000-0002-1589-1796
    affiliation: "1"
  - name: Tilman Birnstiel
    orcid: 0000-0002-1899-8783
    affiliation: 1
affiliations:
  - name: University Observatory, Faculty of Physics, Ludwig-Maximilians-Universität München, Scheinerstr. 1, 81679 Munich, Germany
    index: 1
date: 11 August 2021
---

# Summary

`Simframe` is a Python framework to facilitate scientific simulations.

After initialisation, `Simframe` is an empty framework that can be filled with data fields. The user can now assign differential equations to these fields and configure an integrator with integration instructions.

Fields that should not be integrated can be assigned an update function, according to which they will be updated once per integration step.

`Simframe` contains a number of integration schemes of different orders, both for explicit and implicit integration. Furthermore, `Simframe` includes methods to read and write output files.

Due to its modular structure, `Simframe` can be extended at will, for example, by implementing new integration schemes and/or user-defined output formats.

# Statement of need

Solving differential equations is part of the daily work of scientists. `Simframe` facilitates this by providing the infrastructure: Data structures, integration schemes, and methods to write and read output files.

`Simframe` can be used to quickly solve small scientific problems. Due to its versatility it can be equally used for larger projects where it can be inherited as a starting point.

Furthermore, `Simframe` is ideal for beginners without programming experience who are taking their first steps in solving differential equations. It can therefore be used to design lectures or practical courses at schools and universities, as it allows students to concentrate on the essentials without having to write larger programmes on their own.

# Features

## Data fields

The data fields of `Simframe` are subclassed `NumPy` `ndarray`s. The full `NumPy` functionality can therefor be used on `Simframe` data fields.

## Integration schemes

`Simframe` includes a number of integration schemes as standard. All of these schemes are Runge-Kutta methods of different orders. Some of the methods are adaptive, i.e., they are embedded Runge-Kutta methods, that return an optimal step size for the integration variable, such that the desired accuracy is achieved. The implicit methods require a matrix inversion that is either done directly by `NumPy` or by using the GMRES solver provided by `SciPy`.

Here is a list of all implemented integration schemes:

| Order | Name                        |          |          |               |
|:-----:|-----------------------------|:--------:|:--------:|---------------|
|   1   | Euler                       | explicit |          |               |
|   1   | Euler                       | implicit |          | direct solver |
|   1   | Euler                       | implicit |          | GMRES solver  |
|   2   | Fehlberg                    | explicit | adaptive |               |
|   2   | Heun                        | explicit |          |               |
|   2   | Heun-Euler                  | explicit | adaptive |               |
|   2   | midpoint                    | explicit |          |               |
|   2   | midpoint                    | implicit |          | direct solver |
|   2   | Ralston                     | explicit |          |               |
|   3   | Bogacki-Shampine            | explicit | adaptive |               |
|   3   | Gottlieb-Shu                | explicit | adaptive |               |
|   3   | Heun                        | explicit |          |               |
|   3   | Kutta                       | explicit |          |               |
|   3   | Ralston                     | explicit |          |               |
|   3   | Strong Stability Preserving | explicit |          |               |
|   4   | 3/8 rule                    | explicit |          |               |
|   4   | Ralston                     | explicit |          |               |
|   4   | Runge-Kutta                 | explicit |          |               |
|   5   | Cash-Karp                   | explicit | adaptive |               |
|   5   | Dormand-Prince              | explicit | adaptive |               |

## I/O

By default `Simframe` has two options for storing simulation results. One is by storing the data in a separate namespace within the `Simframe` object itself. Another one is by storing the data in HDF5 data files using the `h5py` package.


If configured by the user, `Simframe` is writing dump files, from which the simulation can be resumed, in case the programme crashed unexpectedly. These dump files are serialized frame objects using the `dill` package.


# Acknowledgements

The authors acknowledge funding from the European Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme under grant agreement No 714769.