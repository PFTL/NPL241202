from PFTL.controller.serial_daq import Device


class AnalogDAQ:
    def __init__(self, device_number):
        self.device_number = device_number

    def initialise(self):
        """ Initialises the Arduino on a given port number """
        port = f"COM{self.device_number}" # For Windows
        port = f"/dev/cu.usbmodem{self.device_number}"  # For Mac
        self.driver = Device(port)
        self.driver.initialise()

    def finalise(self):
        self.set_voltage(0, 0)
        self.set_voltage(1, 0)
        self.driver.finalise()

    def set_voltage(self, channel, volt):
        if volt > 3.3:
            raise Exception(f'Volt {volt} is above 3.3V')
        if channel not in (0, 1):
            raise Exception(f'Channel {channel} is not 0 or 1')

        self.driver.set_output(channel, int(volt/3.3*4095))

    def read_voltage(self, channel):
        volt = self.driver.read_input(channel)
        volt = volt * 3.3 / 1023
        return volt

if __name__ == '__main__':
    analog_daq = AnalogDAQ(11201)
    analog_daq.initialise()
    analog_daq.set_voltage(0, 3)
    print(analog_daq.read_voltage(0))
    analog_daq.finalise()

