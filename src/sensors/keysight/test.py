import keysight_kt34400
import datetime
import keysight_kt34400.keysight_kt34400
import numpy as np


resource_name = 'USB0::0x2A8D::0x8E01::CN62180061::0::INSTR'
driver = keysight_kt34400.Kt34400(resource_name, id_query = True, reset = True)
driver.utility.reset()
driver.trigger.source = keysight_kt34400.keysight_kt34400.TriggerSource.IMMEDIATE

# driver.resistance.configure()
# driver.resistance.configure(10E+3,keysight_kt34400.keysight_kt34400.Resolution.MAX)
driver.resistance.configure(10E+3,keysight_kt34400.keysight_kt34400.Resolution.MIN)

print(driver.system.io_timeout)

maxtime = datetime.timedelta(milliseconds=2e+6)



# data = driver.measurement.read(maxtime)
while True:
    data = driver.measurement.read(maxtime)
# driver.measurement.delete_readings()
    print(data)
print(data)
