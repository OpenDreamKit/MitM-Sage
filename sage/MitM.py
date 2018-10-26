"""
makes MitM functionality available from within Python

(does not actually depend on Sage at this point but might in the future)
"""

from openmath import openmath as om
from openmath import helpers
from openmath import encoder
from openmath import convert_pickle

from scscp import SCSCPCLI
from scscp import scscp

from lxml.etree import tostring

import qmt

def run(query, host="127.0.0.1", port=26134):
    """ Evaluates a query on a MitM server """
    client = None; result = None
    try:
    
        print(tostring(encoder.encode_xml(query.getQuery())))

        sys.exit(1)
        client = SCSCPCLI(host, port=port)
        return client.heads.mitm_transient.mitmEval([query.getQuery()])
    finally:
        if client:
            client.quit()

converter = convert_pickle.PickleConverter() # TODO: Use the MitM converter
lmfdb = qmt.UseSystemHelper("http://www.lmfdb.org/db", "lmfdb", converter)

smglom = helpers.CDBaseHelper("http://mathhub.info/MitM/smglom", converter)
algebra = smglom / "algebra"

smglom = helpers.CDBaseHelper("http://mathhub.info/MitM/smglom", converter)
mitm = helpers.CDBaseHelper("http://mathhub.info/MitM", converter)

# Generate a query to be sent over the wire
# TODO: Actually run the query
query = lmfdb.hmf_forms.where(algebra.HilbertNewforms.base_field_degree(2), algebra.HilbertNewforms.dimension(2)).limit(until=10).map(algebra.HilbertNewforms.base_field_degree)
print(run(query))