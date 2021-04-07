![Build Status](https://github.com/Black-Swan-ICL/PySCMs/actions/workflows/python-package.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# StructuralCausalModels
## Description
A Python package implementing Structural Causal Models (SCMs). 

The package makes it possible to go from Structural Causal Models to 
Graphs. It is also possible to generate a Linear Structural Causal 
Model directly from a coefficient matrix (i.e. the weighted adjacency
matrix of the graph).

'Graph' objects are defined by giving an adjacency matrix (and a name,
optionally). They contain and maintain different representations of a
graph which can be useful depending on the circumstances, and tools to
go from any one representation to any other. 

The representations implemented at present are:

- via an adjacency matrix,
- via adjacency lists,
- via edges ("typed" edges : no edge, forward, backward or undirected 
  edge).
  
## Documentation
The documentation for the package is available 
[here](https://pyscms.readthedocs.io/en/latest/modules.html).
