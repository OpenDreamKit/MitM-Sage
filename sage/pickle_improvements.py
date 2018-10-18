"""
Experimental improvements to SageMath' pickling / OpenMath serialization

Those should eventually be integrated into the official SageMath library
"""

import sage.all
import sage.structure.unique_representation

# More concise pickling for cached representation objects
def __reduce__(self):
    if self._reduction[2]:
        return (unreduce, self._reduction)
    else:
        return self._reduction[:2]

sage.structure.unique_representation.CachedRepresentation.__reduce__ = __reduce__

"""

"""

from openmath.dsl_helpers import *

# shortcuts for QMT queries
mmt = CDBaseHelper("http://???")
qmt = mmt.qmt
query = qmt.query

class MitMHelper(CDBaseHelper):
    """holds all functionality for making MitM tools available in Python"""
    def Gap(self, obj):
        return self.systems.eval(self.systems.Gap, obj)
    def Singular(self, obj):
        return self.systems.eval(self.systems.Singular, obj)
    def LMFDB(self, db, **kwargs):
        where = [self.__getattr__(k)(v) for k,v in kwargs.items()]
        q = query(self.uri(), *where)
        return ListHelper(self.systems.queryeval(q))

# the main MitM object
MitM = MitMHelper("http://???")

# the CD of lists, TODO check path
lists = MitM.lists

class ListHelper(WrappedHelper):
    """wraps around an OM object that will evaluate to a Python list (e.g., a query)
    adds list operations"""
    def map(self, f):
        return ListHelper(lists.map(self.toOM(), f))
    def filter(self, mapFun):
        return ListHelper(lists.filter(self.toOM(), f))


