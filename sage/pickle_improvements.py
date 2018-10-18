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
