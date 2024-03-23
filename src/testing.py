import serial 
import serial.tools.list_ports

class Sensor:
    def __init__(self, port, baudrate = 9600, timeout = 1):
        self.port = port 
        self.baudrate = baudrate
        self.timeout = timeout
        self.conn = None

    def open_connection(self):
        try:
            self.conn = serial.Serial(self.port, self.baudrate, timeout = self.timeout)
            print("Serial Connection Established")
        except serial.SerialException as e:
            print(f"Error: {e}")

    def close_connection(self):
        if self.conn and self.conn.isOpen():
            self.conn.close()
            print("Serial Connection Disconnected")
        else:
            print("No Active Serial Connection.")

    # def read_data(self):
    #     if self.conn and self.conn.isOpen():
    #         try:
    #             data = self.conn.conn.readline().decode("utf-8", errors = 'replace').strip()
    #             return data
    #         except serial.SerialException as e:
    #             print(f"Error reading data: {e}")
    #     else:
    #         print("No Active Serial Connection.")

    def record_vals(self, sample_size):
        values = []

        if not self.conn or not self.conn.isOpen():
            print("No Active Serial Connection.")
            return values 
        
        while len(values) < sample_size:
            try:
                serial_output = self.conn.readline().decode('utf-8', errors = 'replace').strip()
                lines = serial_output.split('\n')

                for line in lines:
                    if "lbs" in line:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part == "lbs":
                                try:
                                    value = abs(float(parts[i - 1]))
                                    values.append(value)
                                except ValueError:
                                    print("Value Error")
                                    pass

            except serial.SerialException as e:
                print(f"Error Reading Data: {e}")
        
        self.close_connection()
        return values