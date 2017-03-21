# Sage -> MMT exporter

Output browsable at: https://odk.mathhub.info/mh/mmt/?http://www.sagemath.org

## How to regenerate (usualy done by @nthiery, upon request)

Install the dependencies:

    git clone https://github.com/nthiery/sage-gap-semantic-interface.git
    cd sage-gap-semantic-interface
    sage -pip install .

Start Sage within the sage/ directory

    cd sage
    sage

Run the following commands:

    sage: import sagetypes
    sage: import json
    sage: data = sagetypes.export()
    sage: with open('sagetypes.json', 'w') as outfile:
    ....:     json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '), default=str, allow_nan=True)

Commit the output file:

    git commit -m "Update Sage CDs" sagetypes.json
