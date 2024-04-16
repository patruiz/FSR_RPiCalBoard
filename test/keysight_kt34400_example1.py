"""
keysight_kt34400 Python API Example Program

Creates a driver object, reads a few DriverIdentity interface properties, and checks
the instrument error queue.  May include additional instrument specific functionality.

Runs in simulation mode without an instrument.

Requires Python 3.6 or newer and keysight_kt34400 Python module installed.
"""

import keysight_kt34400 as m
import numpy as np # Required by keysight_kt34400
import datetime
import time


def main():
    """
    Edit resource_name and options as needed.  resource_name is ignored if option Simulate=True.
    For this example, resource_name may be a VISA address(e.g. "TCPIP0::<ipAddress or hostName>::INSTR")
    or a VISA alias.  For more information on using VISA aliases, refer to the Keysight IO
    Libraries Connection Expert documentation.
    See driver help file topic 'Creating a Driver Instance' for constructor options details.
    """
    # resource_name = "MyVisaAlias"
    resource_name = 'USB0::0x2A8D::0x8E01::CN62180061::0::INSTR'
    idQuery = True
    reset   = True
    options = "QueryInstrStatus=False, Simulate=False, Trace=False"

    try:
        print("\n  keysight_kt34400 Python API Example1\n")

        # Call driver constructor with options
        global driver # May be used in other functions
        driver = None
        driver = m.Kt34400(resource_name, idQuery, reset, options)
        print("Driver Initialized")

        #  Print a few identity properties
        print('  identifier: ', driver.identity.identifier)
        print('  revision:   ', driver.identity.revision)
        print('  vendor:     ', driver.identity.vendor)
        print('  description:', driver.identity.description)
        print('  model:      ', driver.identity.instrument_model)
        print('  resource:   ', driver.driver_operation.io_resource_descriptor)
        print('  options:    ', driver.driver_operation.driver_setup)


        # Reset the DMM
        driver.utility.reset()

        #Set up the DMM for immediate trigger
        driver.trigger.source = m.TriggerSource.IMMEDIATE

        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        #---------------------DC Volt measurements------------------------
        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        #Configure the meter to 10V range and fast mode (least resolution)
        driver.dc_voltage.configure(10, m.Resolution.MAX)
        max_time = datetime.timedelta(seconds = 5)
        data = driver.measurement.read(max_time)

        #Display the Raw DC Volts Measurement
        print("Raw DC Volts measurement: ,",data, " Volts")

        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        #---------------------AC Volt measurements------------------------
        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        #Configure the meter to 10VAC range and fast mode (least resolution)
        driver.ac_voltage.configure(10,m.Resolution.MAX)
        data = driver.measurement.read(max_time)

        #Display the Raw AC Volts Measurement
        print("Raw AC Volts measurement: ,",data, " Volts")

        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        #-------------------DC Current measurements-----------------------
        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        #Configure the meter to 100mA range and fast mode (least resolution)
        driver.dc_current.configure(100E-3,m.Resolution.MAX)
        data = driver.measurement.read(max_time)
        print("DC Current measurement: ,",data, " Amps")

        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        #-------------------AC Current measurements-----------------------
        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        #Configure the meter to 100mA range and fast mode (least resolution)
        driver.ac_current.configure(100E-3,m.Resolution.MAX)
        data = driver.measurement.read(max_time)
        print("AC Current measurement: ,",data, " Amps")

        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        #--------------------Frequency measurements-----------------------
        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        #Configure the meter to read frequency
        driver.frequency.configure(100,m.Resolution.MAX)
        driver.frequency.voltage_range = 10

        data = driver.measurement.read(max_time)
        print("Frequency measurement: ,",data, " Hz")

        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        #-------------------Resistance measurements-----------------------
        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        #Configure the meter to 10k ohm range and fast mode (least resolution)
        driver.resistance.configure(10E+3,m.Resolution.MAX)

        data = driver.measurement.read(max_time)
        print("2-Wire Resistance measurement: ,",data, " Ohms")

        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        #-------------------Temperature measurements----------------------
        #"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        #Configure the meter to 5k ohm range
        driver.temperature.configure()

        data = driver.measurement.read(max_time)
        print("Thermistormeasurement: ,",data, " degrees C")


        # Check instrument for errors
        print("\n")
        while True:
            outVal = ()
            outVal = driver.utility.error_query()
            print("  error_query: code:", outVal[0], " message:", outVal[1])
            if(outVal[0] == 0): # 0 = No error, error queue empty
                break

    except Exception as e:
        print("\n  Exception:", e.__class__.__name__, e.args)

    finally:
        if driver is not None: # Skip close() if constructor failed
            driver.close()
        input("\nDone - Press Enter to Exit")


if __name__ == "__main__":
    main()