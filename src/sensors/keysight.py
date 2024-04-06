import keysight_kt34400
import numpy as np
import pyvisa

resource_name = "MyVisaAlias"
id_query = True
reset = True
options = ""
driver = keysight_kt34400.Kt34400(resource_name, id_query, reset, options)

