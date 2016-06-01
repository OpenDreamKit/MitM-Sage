"""
Exporting semantic information from Sage

EXAMPLES::

    sage: import sagetypes
    sage: import json
    sage: data = sagetypes.export()
    sage: with open('sagetypes.json', 'w') as outfile:
    ....:     json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
"""

import sage.categories.category

def category_name(category):
    """
    Return the name for the category

    EXAMPLES::

        sage: sagetypes.category_name(Groups())
        'sage.categories.groups.Groups'
    """
    cls = category.__class__.__base__
    return cls.__module__+"."+cls.__name__

def export_category(category):
    """
    Export semantic information about the category

    EXAMPLES::

        sage: sagetypes.export_category(Groups())
        {'implied': ['sage.categories.monoids.Monoids',
          'sage.categories.magmas.Magmas.Unital.Inverse'],
         'name': 'sage.categories.groups.Groups',
         'type': 'Sage_Category'}
    """
    return {"implied": [category_name(cat) for cat in category.super_categories()],
            "name": category_name(category),
            "type": "Sage_Category"}

def export():
    return [export_category(category) for category in sage.categories.category.category_sample()]
