"""
Exporting semantic information from Sage

EXAMPLES::

    sage: import sagetypes
    sage: import json
    sage: data = sagetypes.export()
    sage: with open('sagetypes.json', 'w') as outfile:
    ....:     json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

.. TODO::

    - What information do we want to export?
      The super categories? or the axioms and structure?
"""

from sage.misc.cachefunc import cached_function
from sage.categories.category import Category
from sage.categories.category_with_axiom import CategoryWithAxiom
from sage.categories.covariant_functorial_construction import FunctorialConstructionCategory
from sage.sets.recursively_enumerated_set import RecursivelyEnumeratedSet
from sage.rings.rational_field import QQ

def nested_categories(category):
    result = []
    for key,value in category.__class__.__base__.__dict__.iteritems():
        if isinstance(value, type):
            if issubclass(value, (CategoryWithAxiom, FunctorialConstructionCategory)):
                if key == "Algebras":
                    result.append(getattr(category, key)(QQ))
                else:
                    result.append(getattr(category, key)())
    return result

@cached_function
def category_sample():
    r"""
    Return a sample of categories.

    It is constructed by looking for all concrete category classes declared in
    ``sage.categories.all``, calling :meth:`Category.an_instance` on those and
    taking all their super categories.

    EXAMPLES::

        sage: from sage.categories.category import category_sample
        sage: sorted(category_sample(), key=str)
        [Category of G-sets for Symmetric group of order 8! as a permutation group,
         Category of Hecke modules over Rational Field,
         Category of additive magmas, ...,
         Category of fields, ...,
         Category of graded hopf algebras with basis over Rational Field, ...,
         Category of modular abelian varieties over Rational Field, ...,
         Category of simplicial complexes, ...,
         Category of vector spaces over Rational Field, ...,
         Category of weyl groups,...
    """
    import sage.categories.all
    abstract_classes_for_categories = [Category]
    seeds = tuple(cls.an_instance()
                  for cls in sage.categories.all.__dict__.values()
                  if isinstance(cls, type) and issubclass(cls, Category) and cls not in abstract_classes_for_categories)
    return list(RecursivelyEnumeratedSet(seeds, nested_categories))

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
            "__doc__": category.__doc__,
            "name": category_name(category),
            "axioms": list(category.axioms()),
            "structure": [category_name(cat) for cat in category.structure()],
            "type": "Sage_Category",
            "required_methods": category.required_methods()
    }

def export():
    return [export_category(category) for category in category_sample()]
