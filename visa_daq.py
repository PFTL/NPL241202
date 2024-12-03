from serial_daq import Device
import pyvisa
from time import sleep

rm = pyvisa.ResourceManager('@py')


class VisaDAQ(Device):
    def initialise(self):
        self.dev = rm.open_resource(self.port)
        sleep(1)
        self.dev.write_termination = '\n'
        self.dev.read_termination = '\r\n'

    def query(self, message):
        return self.dev.query(message)
    

if __name__ == "__main__":
    visa_dev = VisaDAQ('ASRL/dev/cu.usbmodem11201::INSTR')
    visa_dev.initialise()
    visa_dev.idn()

    visa_dev.set_output(0, 4000)
    print(visa_dev.read_input(0))
    visa_dev.finalise()