"""
makes MitM functionality available from within Python

(does not actually depend on Sage at this point but might in the future)
"""

from openmath import openmath as om
from openmath import helpers

class MitMHelper(helpers.CDBaseHelper):
    """holds all functionality for making MitM tools available in Python"""
    def __init__(self, cdbase, conv):
        """conv: the OM converter to use for building Python objects"""
        self._conv = conv
        super().__init__(cdbase)
    def __call__(self, a):
        """runs a computation or query through MitM"""
        obj = helpers.interpretAsOpenMath(a)
        print("this should run", obj)
        # apply conv to imports result(s) into Python

# the main MitM object
MitM = MitMHelper("http://???", None) # replace None with our Converter
systems = MitM.systems

def Gap(obj):
    """marks an OM object for evaluation in Gap"""
    return systems.eval(systems.Gap, obj)
def Sage(obj):
    """marks an OM object for evaluation in Sage"""
    return systems.eval(systems.Sage, obj)
def Singular(obj):
    """marks an OM object for evaluation in Singular"""
    return systems.eval(systems.Singular, obj)

def LMFDB(obj):
    """marks an OM object for evaluation through LMFDB (i.e., as an LMFDB query)"""
    q = systems.queryEval(systems.LMFDB, obj)
    return ListHelper(q)


### building queries

mmt = helpers.CDBaseHelper("http://???")
qmt = mmt.qmt

class QueryHelper(helpers.WrappedHelper):
    """base of classes representing queries"""
    def toOM(self):
        pass

def FROM(db):
    """starts constructing a query
    db: a CDHelper referencing a virtual theory"""
    return FROMQuery(db)

class FROMQuery(QueryHelper):
    """helper object for building queries"""
    def __init__(self, db):
        self.db = db
    def toOM(self):
        return om.OMSymbol(cdbase=self.db.cdbase, cd=self.db.cd, name="")
    def WHERE(self, **kwargs):
        conditions = [qmt.condition(self.db.__getattr__(k),v) for k,v in kwargs.items()]
        return WHEREQuery(self, conditions)

class WHEREQuery(QueryHelper):
    """helper object for adding conditions to a query"""
    def __init__(self, fq, cs):
        self.fromquery = fq
        self.conditions = cs
    def toOM(self):
        return qmt.where(self.fromquery.toOM(), *self.conditions)

### working with query results

# the CD of lists
lists = MitM.lists

class ListHelper(WrappedHelper):
    """wraps around an OM object that will evaluate to a Python list (e.g., a query)
    adds list operations"""
    def map(self, f):
        return ListHelper(lists.map(self, f))
    def filter(self, f):
        return ListHelper(lists.filter(self, f))

### Use case test

lmfdbBase = CDBaseHelper("http://lmfdb.org")
algebra = MitM.algebra

p = LMFDB(FROM(lmfdbBase.hilbertforms).WHERE(dim=2))
q = p.map(lambda x: algebra.hecke(x))
r = MitM(q)