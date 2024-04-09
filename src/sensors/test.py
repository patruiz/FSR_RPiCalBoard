import keysight_kt34400
import numpy as np 
import pyvisa
import datetime

def main():
    # resource_name = "MyVisaAlias"
    resource_name = pyvisa.ResourceManager().list_resources()[0]

    id_query = True
    reset = True
    options = "QueryInstrStatus=False, Simulate=False, Trace=False"

    try: 
        #Initialize Driver
        driver = None
        driver = keysight_kt34400.Kt34400(resource_name, id_query, reset, options)
        print("Driver Initialized")

        print('         description:', driver.identity.description)

        max_time = datetime.timedelta(seconds = 5)

        #Kt34400Resistance Driver
        r_driver = driver.K

        print('         description:', r_driver.identity.description)

        driver.utility.reset()

        driver.trigger.source = keysight_kt34400.TriggerSource.IMMEDIATE
        
        
        r_driver.resistance.configure(10E+6,m.Resolution.MAX)

        data = r_driver.measurement.read(max_time)
        print("2-Wire Resistance measurement: ,",data, " Ohms")

    except Exception as e:
        # print("\n  Exception:", e.__class__.__name__, e.args)
        print("fuck")
        pass

    finally:
        if driver is not None: # Skip close() if constructor failed
            driver.close()
        input("\nDone - Press Enter to Exit")



if __name__ == "__main__":
    main()