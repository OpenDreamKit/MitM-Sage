
# sage/src/sage/structure/sage_object.pyx

cdef class SageObject:
    def _test_new(self, **options):
    def rename(self, x=None):
    def reset_name(self):
    def __repr__(self):
    def _ascii_art_(self):
    def _unicode_art_(self):
    def __hash__(self):
    def _cache_key(self):
    def save(self, filename=None, compress=True):
    def dump(self, filename, compress=True):
    def dumps(self, compress=True):
    def db(self, name, compress=True):
    def category(self):
    def _test_category(self, **options):
    def parent(self):
    def _tester(self, **options):
    def _test_not_implemented_methods(self, **options):
    def _test_pickling(self, **options):
    def _sage_(self):
    def _interface_(self, I):
    def _interface_init_(self, I=None):
    def _interface_is_cached_(self):
    def _gap_(self, G=None):
    def _gap_init_(self):
    def _gp_(self, G=None):
    def _gp_init_(self):
    def _kash_(self, G=None):
    def _kash_init_(self):
    def _axiom_(self, G=None):
    def _axiom_init_(self):
    def _fricas_(self, G=None):
    def _fricas_init_(self):
    def _giac_(self, G=None):
    def _giac_init_(self):
    def _maxima_(self, G=None):
    def _maxima_init_(self):
    def _maxima_lib_(self, G=None):
    def _maxima_lib_init_(self):
    def _magma_init_(self, magma):
    def _macaulay2_(self, G=None):
    def _macaulay2_init_(self):
    def _maple_(self, G=None):
    def _maple_init_(self):
    def _mathematica_(self, G=None):
    def _mathematica_init_(self):
    def _octave_(self, G=None):
    def _octave_init_(self):
    def _r_init_(self):
    def _singular_(self, G=None, have_ring=False):
    def _singular_init_(self, have_ring=False):
    def _pari_(self):
    def _pari_init_(self):

# sage/local/lib/python2.7/site-packages/sage/categories/category.py

class Category(UniqueRepresentation, SageObject):
    def __classcall__(cls, *args, **options):
    def __init__(self, s=None):
    def _label(self):
    def __repr_object_names(self):
    def _repr_object_names(self):
    def _short_name(self):
    def an_instance(cls):
    def __call__(self, x, *args, **opts):
    def _call_(self, x):
    def _repr_(self):
    def _latex_(self):
    def _subcategory_hook_(self, category):
    def __contains__(self, x):
    def __classcontains__(cls, x):
    def is_abelian(self):
    def category_graph(self):
    def super_categories(self):
    def _all_super_categories(self):
    def _all_super_categories_proper(self):
    def _set_of_super_categories(self):
    def all_super_categories(self, proper=False):
    def _super_categories(self):
    def _super_categories_for_classes(self):
    def additional_structure(self):
    def structure(self):
    def is_full_subcategory(self, other):
    def full_super_categories(self):
    def _test_category_graph(self, **options):
    def _test_category(self, **options):
    def _make_named_class(self, name, method_provider, cache=False, picklable=True):
    def subcategory_class(self):
    def parent_class(self):
    def element_class(self):
    def morphism_class(self):
    def required_methods(self):
    def is_subcategory(self, c):
    def or_subcategory(self, category = None, join = False):
    def _is_subclass(self, c):
    def _meet_(self, other):
    def meet(categories):
    def axioms(self):
    def _with_axiom_as_tuple(self, axiom):
    def _with_axiom(self, axiom):
    def _with_axioms(self, axioms):
    def _without_axiom(self, axiom):
    def _without_axioms(self, named=False):
    def _sort(categories):
    def __and__(self, other):
    def __or__(self, other):
    def join(categories, as_list=False, ignore_axioms=(), axioms=()):
    def category(self):
    def example(self, *args, **keywords):


# sage/src/sage/structure/category_object.pyx

cdef class CategoryObject(SageObject):
    def __init__(self, category = None, base = None):
    def __cinit__(self):
    def _init_category_(self, category):
    def _refine_category_(self, category):
    def _is_category_initialized(self):
    def category(self):
    def categories(self):
    def gens_dict(self):
    def gens_dict_recursive(self):
    def objgens(self):
    def objgen(self):
    def _first_ngens(self, n):
    def _defining_names(self):
    def _assign_names(self, names=None, normalize=True, ngens=None):
    def normalize_names(self, ngens, names):
    def variable_names(self):
    def variable_name(self):
    def __temporarily_change_names(self, names, latex_names):
    def inject_variables(self, scope=None, verbose=True):
    def has_base(self, category=None):
    def base_ring(self):
    def base(self):
    def Hom(self, codomain, cat=None):
    def latex_variable_names(self):
    def latex_name(self):
    def __getstate__(self):
    def __setstate__(self,d):
    def __hash__(self):
    def __getattr__(self, name):
    cdef getattr_from_category(self, name):
    def __dir__(self):
    def __div__(self, other):

# sage/local/lib/python2.7/site-packages/sage/structure/parent.pyx

cdef class Parent(category_object.CategoryObject):
    def _init_category_(self, category):
    def _refine_category_(self, category):
    def _unset_category(self):
    def _abstract_element_class(self):
    def element_class(self):
    def __make_element_class__(self, cls, name = None, inherit = None):
    def _set_element_constructor(self):
    def category(self):
    def _test_category(self, **options):
    def _test_eq(self, **options):
    cdef int init_coerce(self, bint warn=True) except -1:
    def _introspect_coerce(self):
    def __getstate__(self):
    def __setstate__(self, d):
    def _repr_option(self, key):
    def is_atomic_repr(self):
    def __call__(self, x=0, *args, **kwds):
    def __mul__(self,x):
    def __contains__(self, x):
    cpdef coerce(self, x):
    def __nonzero__(self):
    cpdef bint _richcmp(left, right, int op) except -2:
    cpdef int _cmp_(left, right) except -2:
    def __getitem__(self, n):
    def _is_valid_homomorphism_(self, codomain, im_gens):
    def Hom(self, codomain, category=None):
    def hom(self, im_gens, codomain=None, check=None):
    def _unset_coercions_used(self):
    def _unset_embedding(self):
    cpdef bint is_coercion_cached(self, domain):
    cpdef bint is_conversion_cached(self, domain):
    cpdef register_coercion(self, mor):
    cpdef register_action(self, action):
    cpdef register_conversion(self, mor):
    cpdef register_embedding(self, embedding):
    def coerce_embedding(self):
    cpdef _generic_convert_map(self, S):
    def _coerce_map_via(self, v, S):
    cpdef bint has_coerce_map_from(self, S) except -2:
    cpdef _coerce_map_from_(self, S):
    cpdef coerce_map_from(self, S):
    cpdef _internal_coerce_map_from(self, S):
    cdef discover_coerce_map_from(self, S):
    cpdef convert_map_from(self, S):
    cpdef _internal_convert_map_from(self, S):
    cdef discover_convert_map_from(self, S):
    cpdef _convert_map_from_(self, S):
    cpdef get_action(self, S, op=operator.mul, bint self_on_left=True, self_el=None, S_el=None):
    cdef discover_action(self, S, op, bint self_on_left, self_el=None, S_el=None):
    cpdef _get_action_(self, S, op, bint self_on_left):
    def construction(self):
    cpdef an_element(self):
    def _an_element_(self):
    cpdef bint is_exact(self) except -2:


# sage/src/sage/groups/group.pyx

cdef class Group(Parent):
    def __init__(self, base=None, gens=None, category=None):
    def __contains__(self, x):
    def is_abelian(self):
    def is_commutative(self):
    def order(self):
    def is_finite(self):
    def is_multiplicative(self):
    def _an_element_(self):
    def quotient(self, H):

# sage/src/sage/groups/group.pyx

cdef class FiniteGroup(Group):
    def __init__(self, base=None, gens=None, category=None):
    def is_finite(self):

# sage/local/lib/python2.7/site-packages/sage/groups/perm_gps/permgroup_named.py

class TransitiveGroup(PermutationGroup_unique):
    def __init__(self, d, n):
    def _repr_(self):

# sage/local/lib/python2.7/site-packages/sage/groups/perm_gps/permgroup.py

class PermutationGroup_generic(group.FiniteGroup):
    def __init__(self, gens=None, gap_group=None, canonicalize=True, domain=None, category=None):
    def construction(self):
    def _has_natural_domain(self):
    def _gap_init_(self):
    def _magma_init_(self, magma):
    def __cmp__(self, right):
    def _element_class(self):
    def __call__(self, x, check=True):
    def _coerce_impl(self, x):
    def list(self):
    def __contains__(self, item):
    def has_element(self, item):
    def __iter__(self):
    def gens(self):
    def gens_small(self):
    def gen(self, i=None):
    def identity(self):
    def exponent(self):
    def largest_moved_point(self):
    def degree(self):
    def domain(self):
    def _domain_gap(self, domain=None):
    def smallest_moved_point(self):
    def representative_action(self,x,y):
    def orbits(self):
    def orbit(self, point, action="OnPoints"):
    def transversals(self, point):
    def stabilizer(self, point, action="OnPoints"):
    def base(self, seed=None):
    def strong_generating_system(self, base_of_group=None):
    def _repr_(self):
    def _latex_(self):
    def _order(self):
    def order(self):
    def random_element(self):
    def group_id(self):
    def id(self):
    def group_primitive_id(self):
    def center(self):
    def socle(self):
    def frattini_subgroup(self):
    def fitting_subgroup(self):
    def solvable_radical(self):
    def intersection(self, other):
    def conjugacy_class(self, g):
    def conjugacy_classes(self):
    def conjugate(self, g):
    def direct_product(self, other, maps=True):
    def semidirect_product(self, N, mapping, check=True):
    def holomorph(self):
    def subgroup(self, gens=None, gap_group=None, domain=None, category=None, canonicalize=True, check=True):
    def as_finitely_presented_group(self, reduced=False):
    def quotient(self, N):
    def commutator(self, other=None):
    def cohomology(self, n, p = 0):
    def cohomology_part(self, n, p = 0):
    def homology(self, n, p = 0):
    def homology_part(self, n, p = 0):
    def character_table(self):
    def irreducible_characters(self):
    def trivial_character(self):
    def character(self, values):
    def conjugacy_classes_representatives(self):
    def conjugacy_classes_subgroups(self):
    def subgroups(self):
    def _regular_subgroup_gap(self):
    def has_regular_subgroup(self, return_group = False):
    def blocks_all(self, representatives = True):
    def cosets(self, S, side='right'):
    def minimal_generating_set(self):
    def normalizer(self, g):
    def centralizer(self, g):
    def isomorphism_type_info_simple_group(self):
    def is_abelian(self):
    def is_commutative(self):
    def is_cyclic(self):
    def is_elementary_abelian(self):
    def isomorphism_to(self, right):
    def is_isomorphic(self, right):
    def is_monomial(self):
    def is_nilpotent(self):
    def is_normal(self, other):
    def is_perfect(self):
    def is_pgroup(self):
    def is_polycyclic(self):
    def is_simple(self):
    def is_solvable(self):
    def is_subgroup(self, other):
    def is_supersolvable(self):
    def non_fixed_points(self):
    def fixed_points(self):
    def is_transitive(self, domain=None):
    def is_primitive(self, domain=None):
    def is_semi_regular(self, domain=None):
    def is_regular(self, domain=None):
    def normalizes(self, other):
    def composition_series(self):
    def derived_series(self):
    def lower_central_series(self):
    def molien_series(self):
    def normal_subgroups(self):
    def poincare_series(self, p=2, n=10):
    def sylow_subgroup(self, p):
    def upper_central_series(self):