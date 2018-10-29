import os
import socket
from six.moves import socketserver
import logging

from openmath.convert_pickle import PickleConverter as MitMConverter
from openmath import openmath as om

from scscp.client import TimeoutError, CONNECTED
from scscp.server import SCSCPServer
from scscp.scscp import SCSCPQuit, SCSCPProtocolError
from scscp import scscp

from scscp.socketserver import SCSCPServerRequestHandler, SCSCPSocketServer

import traceback

# improve sage openmath serialisation
# imported only for side-effects
import pickle_improvements

MitMBase = "http://opendreamkit.org/"
MitMCD = "scscp_transient_1"
MitMEval = "MitM_Evaluate"

class MitMRequestHandler(SCSCPServerRequestHandler):
    def __init__(self, converter, *args, **kwargs):
        self.converter = converter
        SCSCPServerRequestHandler.__init__(self, *args, **kwargs)
    
    def handle_call(self, call, head):
        if call.data.elem.cdbase == MitMBase and call.data.elem.cd == MitMCD and call.data.elem.name == MitMEval:
           # we take the one argument of MitMEval, import it (which triggers computation), and export it (i.e., the result of the computation)
           obj = call.data.arguments[0]
           try:
              objPy = self.converter.to_python(obj)
              return self.converter.to_openmath(objPy)
           except Exception as e:
              # we have to protect our error messages, the SCSCP server would swallow them
              eS = traceback.format_exc()
              return om.OMString(str(eS))
        return SCSCPServerRequestHandler.handle_call(self, call, head) # super does not work on this class in Python 2 

    def get_allowed_heads(self, data):
        return scscp.symbol_set([om.OMSymbol(base = MitMEval, cd = MitMCD, name = MitMEval)], cdnames=[MitMCD, 'scscp1'])
    
    def is_allowed_head(self, data):
        head = data.arguments[0]
        return conv.to_openmath((head.cdbase == MitMBase and head.cd == MitMCD and head.name == MitMEval)
                              or head.cd == 'scscp1')

    def get_service_description(self, data):
        return scscp.service_description(self.server.name.decode(),
                                             self.server.version.decode(),
                                             self.server.description)

class MitMSCSCPServer(SCSCPSocketServer):
    def __init__(self, openmath_converter, host='localhost', port=26136,
                     logger=None, name=b'MitM Server', version=b'none',
                     description='MitM SCSCP server'):
        
        # build a converter class
        class ReqHandler(MitMRequestHandler):
            def __init__(self, *args, **kwargs):
                MitMRequestHandler.__init__(self, openmath_converter, *args, **kwargs)
        
        SCSCPSocketServer.__init__(self, host=host, port=port, 
            logger=logger or logging.getLogger(__name__), name=name, version=version, 
            description=description, RequestHandlerClass=ReqHandler)

# run an SCSCP server
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('demo_server')

    conv = MitMConverter()

    # Sage specific customization of the conversion
    bc = conv._basic_converter
    sageCDBase = bc._omBase
    def sageOMS(cd,name):
        return om.OMS(cdbase=sageCDBase, cd=cd, name=name)

    # fix to avoid coding large integers as strings
    import copyreg
    from sage.rings.integer import Integer
    def pickle_sage_integer(i):
       return Integer, (int(i),)
    copyreg.pickle(Integer, pickle_sage_integer)

    # import polynomials
    reg = bc.register_to_python_name
    polyConsCD  = "sage.rings.polynomial.polynomial_element"
    polyConsName = "Polynomial"
    polyConsImpl = lambda R, d: R(d)
    reg(sageCDBase, polyConsCD, polyConsName, lambda: polyConsImpl)

    # export polynomial rings
    from sage.rings.polynomial.multi_polynomial_ring_base import MPolynomialRing_base
    from sage.rings.polynomial.polynomial_ring import PolynomialRing_general, PolynomialRing
    polyRingConsCD = "sage.rings.polynomial.polynomial_ring_constructor"
    polyRingConsName = "PolynomialRing"
    def polyRingExp(R):
        br = R.base_ring()
        vns = R.variable_names()
        brO = conv.to_openmath(r)
        vnsO = [om.omString(s) for s in vns]
        RO = om.OMApplication(sageOMS(polyRingConsCD, polyRingConsName), brO, vnsO)
        return RO
    bc.register_to_openmath(MPolynomialRing_base, polyRingExp)
    bc.register_to_openmath(PolynomialRing_general, polyRingExp)

    # export polynomials
    from sage.rings.polynomial.polynomial_element import Polynomial
    def polyExp(p):
        par = p.parent()
        d = p.dict()
        parO = conv.to_openmath(par)
        dO = conv.to_openmath(d)
        om.OMApplication(sageOMS(polyConsCD, polyConsName), parO, dO)
    bc.register_to_openmath(Polynomial, polyExp)

    # start the server
    srv = MitMSCSCPServer(conv, host=os.environ.get('SCSCP_HOST') or 'localhost', logger=logger)
    
    R = PolynomialRing(Integers(), ["x1","x2"])
    print(conv.to_openmath(R))

    try:
        print("starting SCSCP server")
        # srv.serve_forever()
        print("server terminated")
    except KeyboardInterrupt:
        srv.shutdown()
        srv.server_close()
