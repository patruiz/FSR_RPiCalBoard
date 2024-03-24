from src.sensors.futek import IPM650

def main():
    futek_port = r"/dev/tty.usbserial-811647"

    loadcell = IPM650(port = futek_port, baudrate = 115200, timeout = 1)
    loadcell.open_connection()
    for i in range(1):
        loadcell.start_test(5, print_vals = False)
    print(loadcell.data)
    loadcell.close_connection()
    loadcell.store_data(False)

def test():
    pass

if __name__ == "__main__":
    # main()
    test()