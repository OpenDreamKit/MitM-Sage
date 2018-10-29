"""
makes MitM functionality available from within Python

(does not actually depend on Sage at this point but might in the future)
"""

from openmath import openmath as om
from openmath import helpers
from openmath import encoder
from openmath import convert as c
from openmath import convert_pickle

from scscp import SCSCPCLI
from scscp import scscp

from lxml.etree import tostring

import qmt
import sage.all

hack = c.Converter()

hack.register_to_python_name("http://python.org/", "Python", "list", lambda *args: list(args))
hack.register_to_python_class(om.OMString, lambda s:s.string)
hack.register_to_python_class(om.OMInteger, lambda i:i.integer)

from sage.rings.rational_field import RationalField
hack.register_to_python_name("http://python.org/", "sage.rings.rational_field", "RationalField", RationalField())

from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
hack.register_to_python_name("http://python.org/", "sage.rings.polynomial.polynomial_ring_constructor", "PolynomialRing", PolynomialRing)

def run(query, host="127.0.0.1", port=26134):
    """ Evaluates a query on a MitM server """
    xml = encoder.encode_xml(query.getQuery())

    client = None; result = None
    try:
        client = SCSCPCLI(host, port=port)
        res = client.heads.mitm_transient.mitmEval([query.getQuery(), Systems.SageEval._toOM()], timeout=100000000)
        return hack.to_python(res)
    finally:
        if client:
            client.quit()



converter = convert_pickle.PickleConverter() # TODO: Use the MitM converter
from sage.rings.integer import Integer
converter._basic_converter.register_to_openmath(Integer, lambda i: om.OMInteger(int(i)))

Systems = helpers.CDBaseHelper("http://opendreamkit.org/", converter).Systems
lmfdb = qmt.UseSystemHelper("http://www.lmfdb.org/db", "lmfdb", converter)

smglom = helpers.CDBaseHelper("http://mathhub.info/MitM/smglom", converter)
algebra = smglom / "algebra"

smglom = helpers.CDBaseHelper("http://mathhub.info/MitM/smglom", converter)
mitm = helpers.CDBaseHelper("http://mathhub.info/MitM", converter)