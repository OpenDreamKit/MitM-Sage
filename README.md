# Sage -> MMT exporter

Output browsable at: https://odk.mathhub.info/mh/mmt/?http://www.sagemath.org

## How to regenerate Sage's output (usually done by @nthiery, upon request)

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

## How to process Sage's output (usually done by Dennis Müller, upon request)

Partial instructions, written by @pdehaye:

Make sure you have the necessary MMT plugin installed. From jEdit console: 

    extension info.kwarc.mmt.odk.Plugin

Build the omdoc archive from the json export generated above:

    build ODK/Sage sage-omdoc

