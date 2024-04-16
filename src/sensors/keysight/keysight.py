import keysight_kt34400 
import keysight_kt34400.keysight_kt34400
import numpy as np 
import keyboard
import datetime
import time
import csv
import os 

def store_data(data, fsr_num, save_data = True):
    if save_data == True:
        save_dir = os.path.join('data', 'raw', 'keysight')
        datetime_stamp = datetime.now().strftime('%d%b%y_%H-%M-%S')
        file_name = f"FSR{fsr_num}_calibration_{datetime_stamp}.csv"
        file_path = os.path.join(save_dir, file_name)
        print(file_path)

def main(resource_name):
    data = []

    idQuery = True
    reset = True
    options = "QueryInstrStatus=True, Simulate=False, Trace=True"

    try:
        os.system('cls')
        print("Keysight EDU34450A Python Driver Initilizing ...")
        time.sleep(3)
        driver = keysight_kt34400.Kt34400(resource_name, idQuery, reset, options)
        print("Driver Initialized\n")

        print('  identifier: ', driver.identity.identifier)
        print('  revision:   ', driver.identity.revision)
        print('  vendor:     ', driver.identity.vendor)
        print('  description:', driver.identity.description)
        print('  model:      ', driver.identity.instrument_model)
        print('  resource:   ', driver.driver_operation.io_resource_descriptor)
        print('  options:    ', driver.driver_operation.driver_setup)
        print(' ')

        driver.utility.reset()

        driver.trigger.source = keysight_kt34400.TriggerSource.IMMEDIATE

        # driver.resistance.configure(10E+3,keysight_kt34400.keysight_kt34400.Resolution.MIN)
        driver.resistance.configure(1E+8, keysight_kt34400.keysight_kt34400.Resolution.MED)

        sample_delay = datetime.timedelta(milliseconds=2e+6)

        try:
            while True:
                val = driver.measurement.read(sample_delay)
                print(val)
                data.append(val)
        except KeyboardInterrupt:
            store_data(data, '1', True)

    except Exception as e:
        print("\n Exception:", e.__class__.__name__, e.args)


if __name__ == '__main__':
    resource_name = 'USB0::0x2A8D::0x8E01::CN62180061::0::INSTR'

    main(resource_name)