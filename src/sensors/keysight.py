import keysight_kt34400
import datetime
import numpy as np
import pyvisa

class ResistanceMeasurement:
    def __init__(self, resource_name: str):
        self.driver = keysight_kt34400.Kt34400(resource_name, id_query = True, reset = True)
        self.resistance = self.driver.resistance 
        self.resistance.aperture_enabled(True)
        self.integration_time = datetime.timedelta(seconds = 3)
        self.resistance.aperture = self.integration_time


    def measure_disc(self):
        return self.resistance.measure()
    
    def measure_cont(self):
        while True:
            print(self.resistance.measure())

    def close_driver(self):
        self.driver.close()

def main():
    resource_name = 'USB0::0x2A8D::0x8E01::CN62180061::0::INSTR'
    resistance_meter = ResistanceMeasurement(resource_name)
    resistance_meter.measure_cont()
    resistance_meter.close_driver()

    # res = pyvisa.ResourceManager()
    # print(res.list_resources_info())

if __name__ == "__main__":
    main()
    
