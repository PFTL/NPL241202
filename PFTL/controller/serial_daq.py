import matplotlib.pyplot as plt

import serial 
from time import sleep


class Device:
    def __init__(self, port):
        self.port = port
        self.dev = None

    def initialise(self):
        self.dev = serial.Serial(self.port)
        sleep(1)

    def query(self, message):
        out = message + '\n'
        out = out.encode('ascii')
        self.dev.write(out)
        ans = self.dev.readline().decode('ascii').strip()
        if ans.startswith('ERROR'):
            raise Exception(f'Wrong command: {out}')

        return ans

    def idn(self):
        ans = self.query('*IDN?')
        print(ans)

    def set_output(self, channel, value):
        """ Channel 0 or 1, value integer between 0 and 4095"""
        out = f'OUT:CH{channel} {value}'
        self.query(out)

    def read_input(self, channel):
        out = f'MEAS:CH{channel}?'
        return int(self.query(out))

    def finalise(self):
        self.dev.close()


if __name__ == '__main__':
    dev = Device('/dev/cu.usbmodem11201')
    dev.initialise()
    dev.idn()

    currents = []
    voltages = []
    try:
        for i in range(0, 4096, 50):
            dev.set_output(0, i)
            ans = dev.read_input(0) * 3.3 / 1023
            current = ans / 220
            currents.append(current)
            voltages.append(i * 3.3 / 4095)

    except Exception as e:
        print(e)

    dev.finalise()

    plt.plot(voltages, currents, '.')
    plt.xlabel('Voltages (V)')
    plt.ylabel('Current (A)')
    plt.show()
