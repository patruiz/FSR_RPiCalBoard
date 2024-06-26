"""
keysight_kt34400 Python API Example Program

Creates a driver object, reads a few DriverIdentity interface properties, and checks
the instrument error queue.  May include additional instrument specific functionality.

Runs in simulation mode without an instrument.

Requires Python 3.6 or newer and keysight_kt34400 Python module installed.
"""

import keysight_kt34400 as m
import numpy as np # Required by keysight_kt34400
import time


def main():
    """
    Edit resource_name and options as needed.  resource_name is ignored if option Simulate=True.
    For this example, resource_name may be a VISA address(e.g. "TCPIP0::<ipAddress or hostName>::INSTR")
    or a VISA alias.  For more information on using VISA aliases, refer to the Keysight IO
    Libraries Connection Expert documentation.
    See driver help file topic 'Creating a Driver Instance' for constructor options details.
    """
    resource_name = "MyVisaAlias"
    #resource_name = "TCPIP0::127.0.0.1::INSTR"
    idQuery = True
    reset   = True
    options = "QueryInstrStatus=False, Simulate=True, Trace=False"

    try:
        print("\n  keysight_kt34400 Python API Example1\n")

        # Call driver constructor with options
        global driver # May be used in other functions
        driver = None
        driver = keysight_kt34400.Kt34400(resource_name, idQuery, reset, options)
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
Top

Status Service Request
File: keysight_kt34400_status_srq.py

"""
keysight_kt34400 Python API Status SRQ Example Program

Demonstrates how to setup the instrument status system to request service when
a supported condition occurs and how to detect the SRQ using 2 techniques:
    1. Polling the instrument status byte
    2. Asynchronous SRQ event callback

Runs in simulation mode without an instrument.

Requires Python 3.6 or newer and keysight_kt34400 Python module installed.
"""

import keysight_kt34400
import numpy as np # For keysight_kt34400 arrays
import time


def main():
    """
    Edit resourceName and options as needed.  resourceName is ignored if option Simulate=True
    For this example, resourceName may be a VISA address(e.g. "TCPIP0::<ipAddress or hostName>::INSTR") or a VISA alias.
    For more information on using VISA aliases, refer to the Keysight IO Libraries Connection Expert documentation.
    """
    resource_name = "MyVisaAlias"
    #resource_name = "TCPIP0::<IP_Address>::INSTR"
    idQuery = True
    reset   = True
    options = "QueryInstrStatus=False, Simulate=True, Trace=False"

    try:
        print("\n  keysight_kt34400 Python API Example1\n")

        # Call driver constructor with options
        global driver # May be used in other functions
        driver = None
        driver = keysight_kt34400.Kt34400(resource_name, idQuery, reset, options)
        print("Driver Initialized")

        #  Print a few identity properties
        print('  identifier: ', driver.identity.identifier)
        print('  model:      ', driver.identity.instrument_model)
        print('  resource:   ', driver.driver_operation.io_resource_descriptor)
        print('  options:    ', driver.driver_operation.driver_setup)


        # Configure and test SRQs
        print("\nTesting Service Request (SRQ) on OperationComplete...\n")

        # Configure status system to set StatusByte, RequestService bit on EventStatusRegister, OperationComplete bit.
        driver.status.preset();
        driver.status.standard_event.enable_register = keysight_kt34400.StatusStandardEventFlags.OPERATION_COMPLETE
        driver.status.service_request_enable_register = keysight_kt34400.StatusByteFlags.STANDARD_EVENT_SUMMARY
        driver.status.clear() # Clear error queue and event registers for new events

        # Polling for SRQ technique
        # Program polls StatusByte while waiting for SRQ or until max time elapses.
        print("Testing polling status byte for SRQ")

        # Do something that will cause the SRQ event to be fired
        # Most but not all instruments support *OPC...
        driver.system.write_string("*OPC") # Sets ESR Operation Complete bit 0 when all pending operations are complete

        # Polling loop
        srq_occurred = False
        status_byte = keysight_kt34400.StatusByteFlags.NONE
        i=0
        while i < 10: # Wait up to 500ms (iterations * sleep time) for SRQ
            time.sleep(.050) # time sets polling interval
            status_byte = driver.status.serial_poll() # Use ReadstatusByte() on non-488.2 connections (e.g. SOCKET, ASRL)
            if driver.driver_operation.simulate:
                status_byte = keysight_kt34400.StatusByteFlags.REQUEST_SERVICE_SUMMARY # Simulate SRQ

            # StatusByteFlags enums have binary weighted integer values so they can be used for bitwise operations.
            if (status_byte.value & keysight_kt34400.StatusByteFlags.REQUEST_SERVICE_SUMMARY.value) == keysight_kt34400.StatusByteFlags.REQUEST_SERVICE_SUMMARY.value:
                print("  SRQ detected")
                # Service SRQ
                # Your code to query additional status registers to determine the specific source of the SRQ,
                # if needed, and to take appropriate action to service the SRQ.
                print("  SerialPoll(): {} ({})".format(status_byte, int(status_byte)))
                print("  EventStatusRegister:", driver.status.standard_event.read_event_register())
                print()
                srq_occurred = True
                break
            i += 1
        if not srq_occurred:
            print("  ** SRQ did not occur in allotted time\n")


        # Asynchronous SRQ event callback technique
        # Does not work on non-488.2 compliant I/O interface connections (e.g. SOCKET, ASRL)
        # Driver asynchronously calls an event handler method when SRQ occurs.  Program execution may continue.
        print("Testing asynchronous SRQ event callback")
        global handler_called
        handler_called = False

        # Register (add) the SRQ event handler method to be called when the event occurs
        event = driver.status.service_request_event # Get event object
        event.add(srq_event_handler) # Add handler
        #event += srq_event_handler  # Alternate syntax

        # Enable SRQ event callbacks
        driver.status.clear() # Clear error queue and event registers for new events
        driver.status.enable_service_request_events() # Enable SRQ callbacks

        # Do something that will cause the SRQ event to be fired
        # Most but not all instruments support *OPC...
        driver.system.write_string("*OPC") # Sets ESR Operation Complete bit 0 when all pending operations are complete
        time.sleep(.500) # Wait up to 500ms for SRQ but your program can continue to perform other tasks
        if not handler_called:
            print("  ** SRQ did not occur in allotted time\n")

        # Unregister (remove) the SRQ event handler method if done using it
        event.remove(srq_event_handler)
        #event -= srq_event_handler # Alternate syntax

        # End configure and test SRQs


        # Check instrument for errors
        print()
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


def srq_event_handler(args):
    # SRQ event handler function to be called when the event occurs
    global driver
    global handler_called
    handler_called = True
    print('  srq_event_handler called')

    # args.status_byte is the value of the StatusByte when the SRQ occurred including the ServiceRequest bit 6,
    # value 64.  It can be tested, if multiple StatusByte bits are configured to source SRQs, without interfering
    # with any other instrument IO.
    # Note: When run in simulation, args.status_byte will be set to StatusByteFlags.REQUEST_SERVICE_SUMMARY (64) and
    # and all other status event register queries will return StatusByteFlags.NONE (0).
    print("  args.status_byte: {} ({})".format(args.status_byte, int(args.status_byte)))

    # Code to query additional status registers to determine the specific source of the SRQ, if needed, and to
    # take appropriate action to service the SRQ.  Because this method is called asynchronously, any instrument
    # I/O done here may interfere with any I/O in progress from the main program execution.  Your code must
    # manage this appropriately...
    driver.system.clear_io();
    print("  EventStatusRegister:", driver.status.standard_event.read_event_register())
    print();


if __name__ == "__main__":
    main()
Top

Table of Contents
Example Code
Basic Measurement
Status Service Request
Previous topic
Programming Basics

Next topic
Status System Overview

Quick search
indexnext |previous |home | Example Code
© Copyright 2022-24, Keysight Technologies. v2.1.2. Created using Sphinx 7.2.6.