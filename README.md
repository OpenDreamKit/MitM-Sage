# Sage and Math-in-the-Middle

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/OpenDreamKit/MitM-Sage/master)

This repository contains utilities to integrate
[SageMath](http://sagemath.org) in the in-development
Math-in-the-Middle (MitM) interoperability layer between computational
math software.

## Generic system-near OpenMath export for Python and Sage objects

See the [demo notebook](sage/openmath_pickle_demo.ipynb), or run it on
[Binder@EGI](https://binderhub.fedcloud-tf.fedcloud.eu/v2/gh/OpenDreamKit/MitM-Sage/master?filepath=sage/openmath_pickle_demo.ipynb)

## Generic SCSCP server for SageMath

See the [demo notebook](sage/demo_sage_scscp.ipynb), or run it on
[Binder@EGI](https://binderhub.fedcloud-tf.fedcloud.eu/v2/gh/OpenDreamKit/MitM-Sage/master?filepath=sage/demo_sage_scscp.ipynb)

## Exporting Sage's Content Dictionaries (API) to MMT

Output browsable at: https://odk.mathhub.info/mh/mmt/?http://www.sagemath.org

### How to regenerate the Content Dictionaries

Run this [notebook](sage/export.ipynb), either on
[Binder@EGI](https://binderhub.fedcloud-tf.fedcloud.eu/v2/gh/OpenDreamKit/MitM-Sage/master?filepath=sage/export.ipynb),
or after installing this package and its dependencies in SageMath:

    cd sage;
    sage -pip install --user -e .

Optional: commit the output file:

    git commit -m "Update Sage's CDs" sagetypes.json

### How to process Sage's Content Dictionaries

(usually done by Dennis Müller, upon request)

Partial instructions, written by @pdehaye:

Make sure you have the necessary MMT plugin installed. From jEdit console: 

    extension info.kwarc.mmt.odk.Plugin

Build the omdoc archive from the json export generated above:

    build ODK/Sage sage-omdoc
