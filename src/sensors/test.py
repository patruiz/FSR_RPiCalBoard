import keysight_kt34400
import numpy as np 
import pyvisa

def main():
    # resource_name = "MyVisaAlias"
    resource_name = pyvisa.ResourceManager().list_resources()[0]
    id_query = True
    reset = True
    options = ""

    try: 
        #Initialize Driver
        driver = None
        driver = keysight_kt34400.Kt34400(resource_name, id_query, reset, options)
        print("Driver Initialized")

        print('         description:', driver.identity.description)

        #Kt34400Resistance Driver
        r_driver = driver.resistance

        print('         description:', r_driver.identity.description)

        swag = r_driver.measure()
        print(swag)

    except Exception as e: 
        print("\n Exception:", e.__class__.__name__, e.args)
        # print("Driver Initialization Failed")
    
    finally:
        if driver is not None:
            driver.close()
        input("\nDone - Press Enter to Exit")


if __name__ == "__main__":
    main()