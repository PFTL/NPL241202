import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from PFTL.model.analog_daq import AnalogDAQ
import yaml

from threading import Thread


class Experiment:
    def __init__(self):
        self.config = {}
        self.daq = None
        self.voltages = np.empty((1, ))
        self.currents = np.empty((1, ))

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def initialise(self):
        self.daq = AnalogDAQ(self.config['DAQ']['port_number'])
        self.daq.initialise()

    def finalise(self):
        self.daq.finalise()

    def start_scan(self):
        self.scan_thread = Thread(target=self.scan_voltages)
        self.scan_thread.start()

    def scan_voltages(self):
        self.voltages = np.arange(
            self.config['Scan']['start'],
            self.config['Scan']['stop'],
            self.config['Scan']['step']
        )

        self.currents = np.zeros_like(self.voltages)

        i = 0
        for v in self.voltages:
            self.daq.set_voltage(
                self.config['Scan']['channel_out'], 
                v
            )
            self.currents[i] = self.daq.read_voltage(self.config['Scan']['channel_in']) / self.config['DAQ']['resistance']
            i += 1

    def make_plot(self):
        plt.plot(self.voltages, self.currents, '.')
        plt.xlabel('Voltages (V)')
        plt.ylabel('Currents (A)')
        plt.title('IV of an LED')
        plt.show()

    def save_data(self):
        folder = Path(self.config['Save']['data_folder'])
        folder.mkdir(exist_ok=True, parents=True)

        full_path = folder / self.config['Save']['filename']

        np.savetxt(full_path, np.stack((self.voltages, self.currents)))

    def save_metadata(self):
        folder = Path(self.config['Save']['data_folder'])
        folder.mkdir(exist_ok=True, parents=True)

        filename = Path(self.config['Save']['filename'])

        full_path = folder / filename.with_suffix('.yml')

        with open(full_path, 'w') as f:
            yaml.dump(self.config, f)



if __name__ == '__main__':
    exp = Experiment()
    exp.load_config('Examples/config.yml')
    exp.initialise()
    exp.config['Scan']['start'] = 2.4
    exp.scan_voltages()
    exp.save_data()
    exp.save_metadata()
    exp.finalise()
    exp.make_plot()