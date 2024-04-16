import keysight_kt34400
import datetime
import keysight_kt34400.keysight_kt34400
import numpy as np
import pyvisa

class ResistanceMeasurement:
    def __init__(self, resource_name: str):
        self.driver = keysight_kt34400.Kt34400(resource_name, id_query = True, reset = True)

    def measure_cont(self):
        self.resistance = self.driver.resistance 
        self.trigger = self.driver.trigger
        sample_delay = datetime.timedelta(milliseconds = 100)
        sample_interval = datetime.timedelta(milliseconds = 10)
        trigger_source = keysight_kt34400.keysight_kt34400.TriggerSource.IMMEDIATE
        self.trigger.configure(delay = sample_delay, source = trigger_source, count = 5, sample_count = 10, sample_interval = sample_interval)
        while True:
            print(self.resistance.measure())

    def close_driver(self):
        self.driver.close()

def main():
    resource_name = 'USB0::0x2A8D::0x8E01::CN62180061::0::INSTR'
    resistance_meter = ResistanceMeasurement(resource_name)
    resistance_meter.measure_cont()
    resistance_meter.close_driver()

if __name__ == "__main__":
    main()
    
