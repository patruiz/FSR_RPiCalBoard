from src.testing import Sensor

portname = r"/dev/tty.usbserial-811647"

if __name__ == "__main__":
    IPM650 = Sensor(port = portname, baudrate = 115200, timeout = 1)
    IPM650.open_connection()
    values = IPM650.record_vals(10)
    print(values)

