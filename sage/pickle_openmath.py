
# coding: utf-8

# In[20]:


from pickle import Pickler, Unpickler, _Stop #, _Unframer, dumps, bytes_types,
import io
import pickle
import copy
import importlib
import zlib
from openmath import openmath as om
from six.moves import cStringIO as StringIO
import openmath.convert
from sage.structure.sage_object import dumps


##############################################################################
# Shorthands
##############################################################################

def OMloads(str):
    str = zlib.decompress(str)
    file = StringIO(str)
    # file = io.BytesIO(str) # Python3
    return OMUnpickler(file).load()
def mydump(obj):
    file = io.StringIO()
    MyPickler(file, protocol=0).dump(obj)
    return file.getvalue()
class MyPickler(Pickler):
    pass


##############################################################################
# Some new OpenMath constructs
# Those are mostly lazy versions of unpickling operations
##############################################################################

def load_global(o):
    """
    Evaluate an OpenMath construct that loads a global symbol

    EXAMPLES::

        sage: o = om.OMApplication(om.OMSymbol(name='load_global', cd='python'),
        ....:                      [om.OMString("math.sin")])
        sage: load_global(o)
        <built-in function sin>
        sage: openmath.convert.to_python(o)
        <built-in function sin>
    """
    f = openmath.convert.to_python(o.arguments[0]).split(".")
    module = '.'.join(f[:-1])
    if not module:
        module = "sage.all"
    module = importlib.import_module(module)
    return getattr(module, f[-1])

openmath.convert.register_to_python('python',
                                    'load_global',
                                    load_global
                                    )
def apply_function(o):
    """
    Evaluate an OpenMath function application

    EXAMPLES::

        sage: import openmath.openmath as om
        sage: import math
        sage: f = om.OMApplication(om.OMSymbol(name='load_global', cd='python'),
        ....:                      [om.OMString("math.sin")])

        sage: o = om.OMApplication(om.OMSymbol(name='apply_function', cd='python'),
        ....:                      [f, om.OMFloat(3.14)])
        sage: apply_function(o)
        0.0015926529164868282

        sage: apply_function(o) == math.sin(3.14)
        True
    """
    data = [openmath.convert.to_python(arg) for arg in o.arguments]
    return data[0](*data[1:])
openmath.convert.register_to_python('python',
                                    'apply_function',
                                    apply_function
                                    )

def cls_new(o):
    data = [openmath.convert.to_python(arg) for arg in o.arguments]
    return data[0].__new__(data[0], *data[1:])
openmath.convert.register_to_python('python',
                                    'cls_new',
                                    cls_new
                                    )

def apply_global_python_function(o):
    f = openmath.convert.to_python(o.arguments[0]).split(".")
    module = '.'.join(f[:-1])
    if not module:
        module = "sage.all"
    module = importlib.import_module(module)
    f = getattr(module, f[-1])
    return f(*[openmath.convert.to_python(arg) for arg in o.arguments[1:]])
openmath.convert.register_to_python('python',
                                    'apply_global_function',
                                    apply_global_python_function
                                    )



def OMList(l):
    """
    Convert a list of OM objects into an OM object

    EXAMPLES::

        sage: OMList([om.OMInteger(2), om.OMInteger(2)])
        OMApplication(elem=OMSymbol(name='list', cd='list1', id=None, cdbase=None), arguments=[OMInteger(integer=2, id=None), OMInteger(integer=2, id=None)], id=None, cdbase=None)
    """
    return om.OMApplication(elem=om.OMSymbol(name='list', cd='list1', id=None, cdbase=None),
                            arguments=l, id=None, cdbase=None)

def OMTuple(l):
    """
    Convert a list of OM objects into an OM object

    EXAMPLES::

       sage: o = OMTuple([om.OMInteger(2), om.OMInteger(3)]); o
       OMApplication(elem=OMSymbol(name='apply_function', cd='python', id=None, cdbase=None),
                     arguments=[OMApplication(elem=OMSymbol(name='load_global', cd='python', id=None, cdbase=None),
                                              arguments=[OMString(string=u'__builtin__.tuple', id=None)],
                                              id=None, cdbase=None),
                                OMApplication(elem=OMSymbol(name='list', cd='list1', id=None, cdbase=None),
                                              arguments=[OMInteger(integer=2, id=None), OMInteger(integer=3, id=None)],
                                              id=None, cdbase=None)], id=None, cdbase=None)
       sage: openmath.convert.to_python(o)
       (2, 3)
    """
    return om.OMApplication(elem=om.OMSymbol(name='apply_function', cd='python', id=None, cdbase=None),
                            arguments=[om.OMApplication(elem=om.OMSymbol(name='load_global', cd='python', id=None, cdbase=None),
                                                        arguments=[om.OMString(string=u'__builtin__.tuple', id=None)],
                                                       id=None, cdbase=None),
                                       OMList(l)
                                      ],
                            id=None, cdbase=None)

def OMDict(d):
    """
    Convert a list of OM objects into an OM object

    EXAMPLES::

       sage: o = OMTuple([om.OMInteger(2), om.OMInteger(3)]); o
       OMApplication(elem=OMSymbol(name='apply_function', cd='python', id=None, cdbase=None),
                     arguments=[OMApplication(elem=OMSymbol(name='load_global', cd='python', id=None, cdbase=None),
                                              arguments=[OMString(string=u'__builtin__.tuple', id=None)],
                                              id=None, cdbase=None),
                                OMApplication(elem=OMSymbol(name='list', cd='list1', id=None, cdbase=None),
                                              arguments=[OMInteger(integer=2, id=None), OMInteger(integer=3, id=None)],
                                              id=None, cdbase=None)], id=None, cdbase=None)
       sage: openmath.convert.to_python(o)
       (2, 3)
    """
    return om.OMApplication(elem=om.OMSymbol(name='apply_function', cd='python', id=None, cdbase=None),
                            arguments=[om.OMApplication(elem=om.OMSymbol(name='load_global', cd='python', id=None, cdbase=None),
                                                        arguments=[om.OMString(string=u'__builtin__.dict', id=None)],
                                                       id=None, cdbase=None),
                                       OMList(d.items())
                                      ],
                            id=None, cdbase=None)

def OMtest_pickling(l):
    o = OMloads(dumps(l))
    l2 = openmath.convert.to_python(o)
    assert l == l2
    assert type(l) is type(l2)

class OMUnpickler(Unpickler):
    """
    An unpickler that constructs an OpenMath object whose later
    conversion to evaluation will produce the desired Pytho object.

    This can be seen as a lazy unpickler that produces an OpenMath
    object as intermediate step.

    EXAMPLES::

        sage: from pickle_openmath import *

    Constants::

        sage: OMloads(dumps(False))
        OMSymbol(name='false', cd='logic1', id=None, cdbase=None) 
        sage: OMtest_pickling(False)

        sage: OMloads(dumps(True))
        OMSymbol(name='true', cd='logic1', id=None, cdbase=None)
        sage: OMtest_pickling(True)

        sage: OMloads(dumps(None)) # todo: not implemented
        sage: OMtest_pickling(None) # todo: not implemented

    Strings::

        sage: OMloads(dumps('coucou'))
        OMString(string='coucou', id=None)
        sage: openmath.convert.to_python(_)
        'coucou'

    Python integers::

        sage: OMloads(dumps(3r))
        OMInteger(integer=3, id=None)
        sage: openmath.convert.to_python(_)
        3
        sage: OMtest_pickling(3r)

    Sage integers::

        sage: OMloads(dumps(3))
        OMApplication(elem=OMSymbol(name='apply_function', cd='python', id=None, cdbase=None),
                      arguments=[OMApplication(elem=OMSymbol(name='load_global', cd='python', id=None, cdbase=None),
                                               arguments=[OMString(string=u'sage.rings.integer.make_integer', id=None)],
                                               id=None, cdbase=None),
                                 OMString(string='3', id=None)],
                      id=None, cdbase=None)
        sage: OMtest_pickling(3)

    Sage real numbers::

        sage: OMtest_pickling(1.1+1.1)

    But not quite yet real literals::

        sage: OMtest_pickling(1.1)
        Traceback (most recent call last):
        ...
        AssertionError
        sage: l = 1.1
        sage: o = OMloads(dumps(1.1))
        sage: l2 = openmath.convert.to_python(o); l2
        1.10000000000000
        sage: l2 == l
        True
        sage: type(l2)
        <type 'sage.rings.real_mpfr.RealNumber'>
        sage: type(l)
        <type 'sage.rings.real_mpfr.RealLiteral'>

    Lists of integers::

        sage: l = [3r, 1r, 2r]
        sage: o = OMloads(dumps(l)); o
        OMApplication(elem=OMSymbol(name='list', cd='list1', id=None, cdbase=None),
                      arguments=[OMInteger(integer=3, id=None),
                                 OMInteger(integer=1, id=None),
                                 OMInteger(integer=2, id=None)],
                      id=None, cdbase=None)

    Sets of integers::

        sage: s = {1r}
        sage: OMloads(dumps(s))
        OMApplication(elem=OMSymbol(name='apply_function', cd='python', id=None, cdbase=None),
                      arguments=[OMApplication(elem=OMSymbol(name='load_global', cd='python', id=None, cdbase=None),
                                               arguments=[OMString(string=u'__builtin__.set', id=None)],
                                               id=None, cdbase=None),
                                 OMApplication(elem=OMSymbol(name='list', cd='list1', id=None, cdbase=None),
                                               arguments=[OMInteger(integer=1, id=None)], id=None, cdbase=None)],
                      id=None, cdbase=None)
        sage: OMtest_pickling(s)

    Lists of sets of Sage integers::

        sage: OMtest_pickling([{1,3}, {2}])

    Sage parents::

        sage: OMtest_pickling(Partitions(3))

    Sage objects::

        sage: OMloads(dumps(Partition([2,1]))) # todo: not implemented
    """

    # Only needed for print-debug purposes
    def load(self):
        """Read a pickled object representation from the open file.

        Return the reconstituted object hierarchy specified in the file.
        """
        self.mark = object() # any new unique object
        self.stack = []
        self.append = self.stack.append
        read = self.read
        dispatch = self.dispatch
        try:
            while 1:
                key = read(1)
                #print(dispatch[key[0]].__name__, self.stack)
                dispatch[key](self)
        except _Stop, stopinst:
            return stopinst.value

    dispatch = { key: Unpickler.dispatch[key]
                 for key in [pickle.PROTO,
                             pickle.STOP,
                             pickle.BINPUT, # ?
                             pickle.BINGET, # ?
                             pickle.MARK,   # ?
                             pickle.TUPLE1, # are those used to produced actual tuples, or only intermediate results?
                             pickle.TUPLE2,
                             pickle.TUPLE3,
                             pickle.EMPTY_TUPLE,
                             pickle.EMPTY_DICT,
                             pickle.NONE,
                             pickle.TUPLE,
                             pickle.SETITEMS,
                             pickle.NEWFALSE,
                             pickle.NEWTRUE,
                             pickle.INT[0],
                             pickle.BININT1[0],
                             pickle.STRING[0],
                             pickle.SHORT_BINSTRING,
                             pickle.EMPTY_LIST[0],
                             pickle.APPEND[0],
                             pickle.APPENDS[0],
                            ]
               }# copy.copy(Unpickler.dispatch)

    # Finalization
    def load_stop(self):
        value = self.stack.pop()
        value = self.finalize(value)
        raise _Stop(value)
    dispatch[pickle.STOP] = load_stop

    def finalize(self, value):
        if isinstance(value, openmath.openmath.OMApplication):
            for i in range(len(value.arguments)):
                value.arguments[i] = self.finalize(value.arguments[i])
        if isinstance(value, openmath.openmath.OMAny):
            return value
        elif isinstance(value, list):
            return OMList([self.finalize(arg) for arg in value])
        elif isinstance(value, tuple):
            return OMTuple([self.finalize(arg) for arg in value])
        elif isinstance(value, dict):
            return OMDict(value)
        else:
            return openmath.convert.to_openmath(value)

    def load_global(self):
        module = self.readline()[:-1].decode("utf-8")
        name = self.readline()[:-1].decode("utf-8")
        func_name = module+"."+name
        self.append(om.OMApplication(om.OMSymbol(name='load_global', cd='python'),
                                     [om.OMString(func_name)]))
        #def func(*args):
        #    return om.OMApplication(om.OMSymbol(name='apply_function', cd='python'),
        #                            (om.OMString(func_name),)+args)
        #self.append(func)
    dispatch[pickle.GLOBAL[0]] = load_global

    def load_reduce(self):
        stack = self.stack
        args = stack.pop()
        func = stack[-1]
        stack[-1] = om.OMApplication(om.OMSymbol(name='apply_function', cd='python'),
                                     (func,)+args)
    dispatch[pickle.REDUCE[0]] = load_reduce

    def load_newobj(self):
        args = self.stack.pop()
        cls = self.stack.pop()
        obj =  om.OMApplication(om.OMSymbol(name='cls_new', cd='python'),
                                (cls,) + args)
        self.append(obj)
    dispatch[pickle.NEWOBJ[0]] = load_newobj

    # TODO load_build, to restore the state

"""

# In[73]:



# In[74]:



# In[75]:


class A:
    pass
a = A()
a.x=3


# In[76]:


t = OMloads(dumps(a))
print(t)
a2 = openmath.convert.to_python(t)
print(a2)


# In[70]:


a2.x



"""
