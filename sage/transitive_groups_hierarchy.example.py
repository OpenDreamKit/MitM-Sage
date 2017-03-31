from sage.structure.category_object import CategoryObject
from sage.groups.group import Group
from sage.groups.group import FiniteGroup
from sage.groups.perm_gps.permgroup import PermutationGroup_generic
from sage.groups.perm_gps.permgroup_named import PermutationGroup_unique

e.harvest_categories()
e.harvest_sage_object(TransitiveGroups())
e.harvest_sage_object(TransitiveGroup(4,1))
e.harvest_sage_object(TransitiveGroup(4,1).an_element())
e.harvest_sage_object(TransitiveGroup)
e.harvest_sage_object(PermutationGroup_unique)
e.harvest_sage_object(PermutationGroup_generic)
e.harvest_sage_object(FiniteGroup)
e.harvest_sage_object(Group)
e.harvest_sage_object(Parent)
e.harvest_sage_object(CategoryObject)
e.harvest_sage_object(Category)
e.harvest_sage_object(SageObject)

