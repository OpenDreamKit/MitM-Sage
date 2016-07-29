"""
Exporting semantic information from Sage

EXAMPLES::

    sage: import sagetypes
    sage: import json
    sage: data = sagetypes.export()
    sage: with open('sagetypes.json', 'w') as outfile:
    ....:     json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '), default=str, allow_nan=True)

.. TODO::

    - What information do we want to export?
      The super categories? or the axioms and structure?
"""

from sage.misc.misc import attrcall
from sage.misc.cachefunc import cached_function
from sage.misc.abstract_method import AbstractMethod
from sage.misc.sageinspect import sage_getargspec
from sage.categories.category import Category, JoinCategory
from sage.categories.category_with_axiom import CategoryWithAxiom
from sage.categories.covariant_functorial_construction import FunctorialConstructionCategory
from sage.sets.recursively_enumerated_set import RecursivelyEnumeratedSet
from sage.categories.rings import Rings
import mygap

def related_categories(category):
    result = list(category.super_categories())
    for key,value in category.__class__.__base__.__dict__.iteritems():
        if isinstance(value, type):
            if issubclass(value, (CategoryWithAxiom, FunctorialConstructionCategory)):
                if key == "Algebras":
                    result.append(getattr(category, key)(Rings()))
                else:
                    result.append(getattr(category, key)())
    return result

axioms_of_magmas = ['Associative', 'Finite', 'Inverse','Unital','FinitelyGenerated','Commutative']
#,'CartesianProducts','Metric','Topological','Quotients','Subquotients','Subobjects','IsomorphicObjects']

def sub_categories_of_magmas(cat):
    result = []
    for ax in axioms_of_magmas:
        try:
            result.append(getattr(cat, ax)())
        except AttributeError:
            pass
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
    seeds = {cls.an_instance()
             for cls in sage.categories.all.__dict__.values()
             if isinstance(cls, type) and issubclass(cls, Category) and cls not in abstract_classes_for_categories}
    return list(RecursivelyEnumeratedSet(seeds, related_categories))

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

        sage: from sagetypes import export_category
        sage: export_category(Groups())
        {'implied': ['sage.categories.monoids.Monoids',
          'sage.categories.magmas.Magmas.Unital.Inverse'],
         'name': 'sage.categories.groups.Groups',
         'type': 'Sage_Category'}
    """
    semantic = getattr(category, "_semantic", {})
    return {"implied": [category_name(cat) for cat in category.super_categories()],
              "__doc__": category.__doc__,
              "name": category_name(category),
              "axioms": list(category.axioms()),
              "structure": [category_name(cat) for cat in category.structure()],
              "type": "Sage_Category",
              #"required_methods": required_methods(category),
              "parent_class": export_class(category.parent_class),
              "element_class": export_class(category.element_class),
              "morphism_class": export_class(category.morphism_class),
              "subcategory_class": export_class(category.subcategory_class),
              "gap": semantic.get("gap", None),
              "mmt": semantic.get("mmt", None)}

def export_class(cls):
    """

    EXAMPLES::

        sage: class A:
        ....:     _semantic = {'truc': {'gap': 'coucou'} }
        ....:     def truc(x,y): pass
        ....:     def blah(x): pass
        sage: from sagetypes import export_class
        sage: export_class(A)
        {'__doc__': None,
         'methods': {'blah': {'__doc__': None,
           'args': ['x'],
           'argspec': ArgSpec(args=['x'], varargs=None, keywords=None, defaults=None)},
          'truc': {'__doc__': None,
           'args': ['x', 'y'],
           'argspec': ArgSpec(args=['x', 'y'], varargs=None, keywords=None, defaults=None),
           'gap': 'coucou'}}}
    """
    semantic = getattr(cls, "_semantic", {})
    return {
        "__doc__": getattr(cls, "__doc__", None),
        "methods": { key:
            export_method(method, semantic.get(key, {}))
            for (key, method) in cls.__dict__.iteritems()
            if key not in ["__doc__", "__module__", "_sage_src_lines_", "_reduction"]
            and (callable(method) or isinstance(method, AbstractMethod))
            and not any(hasattr(base, key) for base in cls.__bases__)
        }}

def export_method(method, semantic={}):
    """
    Export metadata about a single method, including stuff in semantic

    EXAMPLES::

        sage: def f(x,y): pass
        sage: export_method(f, {"gap":"coucou"})
        {'__doc__': None,
         'args': ['x', 'y'],
         'argspec': ArgSpec(args=['x', 'y'], varargs=None, keywords=None, defaults=None),
         'gap': 'coucou',
         'name': 'f'}
    """
    if isinstance(method, AbstractMethod):
        method = method._f
    try:
        argspec = sage_getargspec(method)
        result = {"__doc__": method.__doc__,
                  "args": argspec.args,
                  "argspec": argspec
        }
    except TypeError:
        result = {}
    result.update(semantic)
    return result

def export():
    return [export_category(category) for category in category_sample()]

def required_methods(self):
    """
    Returns the methods that are required and optional for parents
    in this category and their elements.

    EXAMPLES::

        sage: Algebras(QQ).required_methods()
        {'element': {'optional': ['_add_', '_mul_'], 'required': ['__nonzero__']},
         'parent': {'optional': ['algebra_generators'], 'required': ['__contains__']}}
    """
    return { "parent"  : abstract_methods_of_class(self.parent_class, export_method),
             "element" : abstract_methods_of_class(self.element_class, export_method),
             "morphism": abstract_methods_of_class(self.morphism_class, export_method),
             "subcategory": abstract_methods_of_class(self.subcategory_class, export_method)
    }

def abstract_methods_of_class(cls, extract=None):
    """
    Returns the required and optional abstract methods of the class

    EXAMPLES::

        sage: class AbstractClass:
        ...       @abstract_method
        ...       def required1(): pass
        ...
        ...       @abstract_method(optional = True)
        ...       def optional2(): pass
        ...
        ...       @abstract_method(optional = True)
        ...       def optional1(): pass
        ...
        ...       @abstract_method
        ...       def required2(): pass
        ...
        sage: sage.misc.abstract_method.abstract_methods_of_class(AbstractClass)
        {'optional': ['optional1', 'optional2'],
         'required': ['required1', 'required2']}

    """
    if extract is None:
        def extract(f):
            return f._name
    result = { "required"  : [],
               "optional"  : []
               }
    for name in dir(cls):
        entry = getattr(cls, name)
        if not isinstance(entry, AbstractMethod):
            continue
        if entry.is_optional():
            result["optional"].append(extract(entry))
        else:
            result["required"].append(extract(entry))
    return result

def category_graph(categories = None, relabel="object_names"):
    """
    Return the graph of the categories in Sage.

    INPUT:

    - ``categories`` -- a list (or iterable) of categories

    If ``categories`` is specified, then the graph contains the
    mentioned categories together with all their super
    categories. Otherwise the graph contains (an instance of) each
    category in :mod:`sage.categories.all` (e.g. ``Algebras(QQ)`` for
    algebras).

    For readability, the names of the category are shortened.

    .. TODO:: Further remove the base ring (see also :trac:`15801`).

    EXAMPLES::

        sage: G = sage.categories.category.category_graph(categories = [Groups()])
        sage: G.vertices()
        ['groups', 'inverse unital magmas', 'magmas', 'monoids', 'objects',
         'semigroups', 'sets', 'sets with partial maps', 'unital magmas']
        sage: G.plot()
        Graphics object consisting of 20 graphics primitives

        sage: sage.categories.category.category_graph().plot()
        Graphics object consisting of ... graphics primitives
    """
    from sage import graphs
    if categories is None:
        categories = category_sample()
    # Include all the super categories
    # Get rid of join categories
    categories = set(cat
                     for category in categories
                     for cat in category.all_super_categories(proper=isinstance(category, JoinCategory)))
    g = graphs.digraph.DiGraph()
    for cat in categories:
        g.add_vertex(cat)
        for source in categories:
            # Don't use super_categories() since it might contain join categories
            for target in source._super_categories:
                g.add_edge([source, target])

    if relabel == "object_names":
        g.relabel(attrcall("_repr_object_names"))
    return g
