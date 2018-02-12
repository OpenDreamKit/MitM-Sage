# Sage -> Math-in-the-Middle exporter

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/OpenDreamKit/MitM-Sage/master).

## Exporting Sage's API to MMT

Output browsable at: https://odk.mathhub.info/mh/mmt/?http://www.sagemath.org

### How to regenerate Sage's Content Dictionary (usually done by @nthiery, upon request)

Install this package and its dependencies:

    cd sage;
    sage -pip install --user -e .

Run the following commands:

    sage: from sagetypes import Exporter
    sage: e = Exporter()
    sage: e.harvest_categories()
    sage: e.save('sagetypes.json')

One can also selectively harvest specific objects, classes and
categories before saving. For example::

    sage: e.harvest_sage_object(TransitiveGroups())

Commit the output file:

    git commit -m "Update Sage's CDs" sagetypes.json

Alternatively, you can use the binder link above, run the commands in
a fresh notebook, and download the produced sagetypes.json.

### How to process Sage's output (usually done by Dennis Müller, upon request)

Partial instructions, written by @pdehaye:

Make sure you have the necessary MMT plugin installed. From jEdit console: 

    extension info.kwarc.mmt.odk.Plugin

Build the omdoc archive from the json export generated above:

    build ODK/Sage sage-omdoc

## System-near OpenMath export for Sage

See the [demo notebook](sage/openmath_pickle_demo), or run it on
[Binder](https://mybinder.org/v2/gh/OpenDreamKit/MitM-Sage/master?filepath=sage%2Fopenmath_pickle_demo.ipynb).
