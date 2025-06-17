# Arduino.py
from pyfirmata import Arduino as FirmataArduino, util
import time

class Arduino:
    def __init__(self, baudrate, port="COM7"):
        self.board = FirmataArduino(port)
        self.it = util.Iterator(self.board)
        self.it.start()
        time.sleep(1)
        self.digital = self.board.digital
        self.analog = self.board.analog

    def pinMode(self, pin, mode):
        if mode.upper() == "OUTPUT":
            self.board.digital[pin].mode = 1  # pyfirmata.OUTPUT
        elif mode.upper() == "INPUT":
            self.board.digital[pin].mode = 0  # pyfirmata.INPUT

    def digitalWrite(self, pin, value):
        if isinstance(value, str):
            value = 1 if value.upper() == "HIGH" else 0
        self.board.digital[pin].write(value)
