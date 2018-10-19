"""
makes MitM functionality available from within Python

(does not actually depend on Sage at this point but might in the future)
"""

from openmath import openmath as om
from openmath import helpers

import qmt

converter = None # TODO: Use the MitM converter
lmfdb = qmt.UseSystemHelper("http://www.lmfdb.org/db", "lmfdb", converter)

smglom = helpers.CDBaseHelper("http://mathhub.info/MitM/smglom", converter)
algebra = smglom / "algebra"

# Generate a query to be sent over the wire
# TODO: Actually run the query
query = lmfdb.hmf_forms.where(algebra.base_field_degree(2)).get().map(lambda x: lmfdb.hecke(x))
print(query._query)