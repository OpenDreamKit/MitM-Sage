
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

        sage: from pickle_openmath import *

    Constants:

        sage: OMloads(dumps(False))
        OMSymbol(name='false', cd='logic1', id=None, cdbase=None)
        sage: OMtest_pickling(False)

        sage: OMloads(dumps(True))
        OMSymbol(name='true', cd='logic1', id=None, cdbase=None)
        sage: OMtest_pickling(True)

        sage: OMloads(dumps(None))     # todo: not implemented
        sage: OMtest_pickling(None)    # todo: not implemented

    Strings:

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

    Lists of sets of Sage integers:

        sage: OMtest_pickling([{1,3}, {2}])
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

    dispatch = copy.copy(Unpickler.dispatch)

    # Constants

    def load_false(self):
        Unpickler.load_false(self)
        self.stack.append(openmath.convert.to_openmath(self.stack.pop()))
    dispatch[pickle.NEWFALSE] = load_false

    def load_true(self):
        Unpickler.load_true(self)
        self.stack.append(openmath.convert.to_openmath(self.stack.pop()))
    dispatch[pickle.NEWTRUE] = load_true

    # Integer types
    def load_int(self):
        Unpickler.load_int(self)
        self.stack.append(openmath.convert.to_openmath(self.stack.pop()))
    dispatch[pickle.INT[0]] = load_int

    def load_binint1(self):
        Unpickler.load_binint1(self)
        self.stack.append(openmath.convert.to_openmath(self.stack.pop()))
    dispatch[pickle.BININT1[0]] = load_binint1

    # String types
    def load_string(self):
        Unpickler.load_string(self)
        self.stack.append(openmath.convert.to_openmath(self.stack.pop()))
    dispatch[pickle.STRING[0]] = load_string

    def load_short_binstring(self):
        Unpickler.load_short_binstring(self)
        self.stack.append(openmath.convert.to_openmath(self.stack.pop()))
    dispatch[pickle.SHORT_BINSTRING] = load_short_binstring

    # Containers
    def load_list(self):
        super(OMUnpickler, self).load_list()
        self.stack.append(om.OMList(self.stack.pop()))
    dispatch[pickle.LIST[0]] = load_list

    def load_empty_list(self):
        # This is assuming we own the OpenMath object
        self.append(openmath.convert.to_openmath([]))
    dispatch[pickle.EMPTY_LIST[0]] = load_empty_list

    def load_append(self):
        stack = self.stack
        value = stack.pop()
        list = stack[-1]
        list.arguments.append(value)
    dispatch[pickle.APPEND[0]] = load_append


    def load_appends(self):
        stack = self.stack
        mark = self.marker()
        list = stack[mark - 1].arguments
        list.extend(stack[mark + 1:])
        del stack[mark:]

    dispatch[pickle.APPENDS[0]] = load_appends

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
