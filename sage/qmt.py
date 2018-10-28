# coding: utf-8
"""
    Helpers to build QMT queries
"""

from openmath import openmath as om
from openmath import helpers

import functools

# QMT Path Helpers
_qmt = helpers.CDBaseHelper("http://cds.omdoc.org/qmt")
qmt = _qmt.QMT
QMTTypes = _qmt.QMTTypes
QMTQuery = _qmt.QMTQuery
QMTProp = _qmt.QMTProp
QMTRelationExp = _qmt.QMTRelationExp
QMTJudgements = _qmt.QMTJudgements
QMTBinaries = _qmt.QMTBinaries
QMTUnaries = _qmt.QMTUnaries


_multibody = helpers.CDBaseHelper("http://cds.omdoc.org/mmt").OpenMath.MultiBody
_map = helpers.CDBaseHelper("http://gl.mathhub.info/MMT/LFX/Datatypes").ListSymbols.map


class _QueryBuilder(object):
    """ A class for helping to build QMT MiTM Queries """

    def __init__(self, converter, query, tags=None):
        self._converter = converter
        self._query = query
        self._tags = tags
    
    def where(self, *conditions):
        """ Create a new query that filters given a set of conditions """
        return WHERE(self._converter, self._query, conditions, tags=self._tags)
    
    def use(self, system):
        """ Use a given system """
        return USE(self._converter, self._query, system, tags=self._tags)

    def map(self, func):
        """ Maps a function over this query """
        qmt = self.query()
        return MAP(qmt._converter, qmt._query, func, tags=qmt._tags)
    
    def limit(self, frm=None, until=None):
        """ Limits the set of results to a fixed number """
        return LIMIT(self._converter, self._query, frm, until, tags=self._tags)
    
    def get(self):
        """ Applies all tags (if any) to this Query """
        query = self
        if self._tags is not None:
            for tag in self._tags:
                query = tag(query)
        else:
            return self
        
        query._tags = None
        return query
    
    def query(self):
        """ Applies all tags and wrap this query in the mitm eval symbol """
        query = self.get()
        return _QueryBuilder(query._converter, om.OMSymbol(name="ODKQuery", cd="Systems", cdbase="http://opendreamkit.org")(query._query), tags=query._tags)
    
    def getQuery(self):
        return self.get()._query

    def _toOM(self, term):
        return helpers.convertAsOpenMath(term, self._converter)

    def __str__(self):
        return "_QueryBuilder(%s, %s, %s, %s)" % (self.__class__.__name__, self._converter, self._query, self._tags)
    
    def __repr__(self):
        return "_QueryBuilder(%r, %r, %r, %r)" % (self.__class__.__name__, self._converter, self._query, self._tags)

class USE(_QueryBuilder):
    def __init__(self, converter, base, system, tags=None):
        super(USE, self).__init__(converter, QMTQuery.I(system, base), tags=tags)
        self._base = base
        self._system = system

class FROM(_QueryBuilder):
    def __init__(self, converter, lit, tags=None):
        super(FROM, self).__init__(converter, QMTQuery.Related(
            QMTQuery.Literal(lit),
            QMTRelationExp.ToObject(QMTBinaries.Declares)
        ), tags)
        self._lit = lit
    
    def __call__(self, *args, **kwargs):
        return self._lit(*args, **kwargs)

class MAP(_QueryBuilder):
    def __init__(self, converter, base, func, tags=None):
        super(MAP, self).__init__(converter, _map(base, func), tags)
        self._base = base
        self._func = func

class WHERE(_QueryBuilder):
    def __init__(self, converter, base, conditions, tags=None):
        super(WHERE, self).__init__(converter, None, tags=tags)

        # re-write the individual conditions
        cs = [QMTProp.Holds(om.OMVariable('x'), self._get_condition(c)) for c in conditions]
        
        # if we only have one condition, do not change anything 
        # on the base query
        if len(cs) == 0:
            self._query = base
        
        # if we have > 1, we need to add a holds()
        else:
            self._query = om.OMBinding(
                binder = QMTQuery.Comprehension,
                vars = om.OMBindVariables([om.OMVariable('x')]),
                obj = _multibody(
                    base,
                    functools.reduce(lambda a,b: QMTProp.And(a, b), cs)
                )
            )
        self._base = base
        self._conditions = conditions
    
    def _get_condition(self, term):
        # Things that shouldn't be re-written should be kept as is
        if isinstance(term, NoRewriteCondition):
            return term
        
        # rewrite it into a proper condition
        else:
            term = self._toOM(term)

            if not isinstance(term, om.OMApplication) or len(term.arguments) == 0:
                raise Exception("Has to be an application with at least one argument or a NoRewriteCondition")

            # extract operator, arguments and value
            op = term.elem
            value = term.arguments[0]
            args = term.arguments[1:]
            
            return om.OMBinding(
                binder = QMTJudgements.Equals,
                vars = om.OMBindVariables([om.OMVariable('x')]),
                obj = _multibody(
                    op(om.OMVariable('x'), *args),
                    value
                )
            )
    @staticmethod
    def _(term):
        return NoRewrite(term)
    
    def where(self, *conditions):
        newconditions = list(self._conditions) + list(conditions)
        return WHERE(self._converter, self._base, newconditions, tags=self._tags)

class LIMIT(_QueryBuilder):
    def __init__(self, converter, base, frm=None, until=None, tags=None):

        if frm is None and until is None:
            raise AssertionError("Need some limit")

        if frm is None:
            _query = QMTQuery.SliceUntil(str(until), base)
        elif until is None:
            _query = QMTQuery.SliceFrom(str(frm), base)
        else:
            _query = QMTQuery.Slice(str(frm), str(until), base)

        super(LIMIT, self).__init__(converter, _query, tags=tags)

        self._base = base
        self._frm = frm
        self._until = until

class NoRewriteCondition(helpers.WrappedHelper):
    pass

class UseSystemHelper(helpers.CDBaseHelper):
    def __init__(self, cdbase, system, converter):
        super(UseSystemHelper, self).__init__(cdbase, converter=converter, cdhook=self.__hook__)
        self._cdbase = cdbase
        self._system = system
        self._converter = converter
    
    def __hook__(self, cdbase, cd, converter, symbolhook):
        return FROM(converter, helpers.OMSymbol(name="", cd=cd, cdbase=cdbase, converter=converter), tags=[self])
    
    def __repr__(self):
        """ returns a unique representation of this object """
        return 'UseSystemHelper(%r, %r, [self], %r)' % (self._cdbase, self._converter, self._symbolhook)
    
    def __str__(self):
        """ returns a human-readable representation of this object """ 
        return 'UseSystemHelper(%s, %s, [self], %s)' % (self._cdbase, self._converter, self._symbolhook)
    
    def __call__(self, query):
        return query.use(self._system)

__all__ = ['USE', 'FROM', 'WHERE', 'MAP', 'UseSystemHelper']