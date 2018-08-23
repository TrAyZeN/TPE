import serial
import time

class SerialCommunication():

    def __init__(self, port_name="COM3", baud_rate=9600):
        self.port_name = port_name      # name of the serial port
        self.baud_rate = baud_rate      # speed of the data in bits per seconds

        try:
            self.serial = serial.Serial(port=None, baudrate=self.baud_rate, bytesize=8)
        except serial.serialutil.SerialException as err:
            print(err)      

    def open(self, timeout=2):
        """ Open serial connection with the arduino """

        self.serial.port = self.port_name
        try:
            self.serial.open()
        except serial.serialutil.SerialException as err:
            print(err)
        else:
            time.sleep(timeout)

    def close(self):
        """ Stop the serial connection """

        if self.is_open():
            try:
                self.serial.close()
            except serial.serialutil.SerialException as err:
                print(err)

    def is_open(self):
        return self.serial.is_open

    def write_string(self, string):
        try:
            self.serial.write(string.encode())
        except serial.serialutil.SerialException as err:
                print(err)
