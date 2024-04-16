import keysight_kt34400
import datetime
import numpy as np 

class DMM_Resistance:
    def __init__(self, resource_name):
        self.resource_name = resource_name 
        idQuery = True
        rset = True
        options = "QueryInstrStatus=True, Simulate=False, Trace=True"
resource_name = 'USB0::0x2A8D::0x8E01::CN62180061::0::INSTR'