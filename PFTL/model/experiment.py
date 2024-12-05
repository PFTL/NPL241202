import copy
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from PFTL.model.analog_daq import AnalogDAQ
from PFTL.model.dummy_daq import DummyDAQ
from threading import Thread
from time import sleep
import yaml


class Experiment:
    def __init__(self):
        self.config = {}
        self.daq = None
        self.voltages = np.empty((1, ))
        self.currents = np.empty((1, ))
        self.scan_running = False
        self.keep_running = True

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def initialise(self):
        if self.config['DAQ']['model'] == 'RealDAQ':
            self.daq = AnalogDAQ(self.config['DAQ']['port_number'])
        elif self.config['DAQ']['model'] == 'DummyDAQ':
            self.daq = DummyDAQ(self.config['DAQ']['port_number'])

        self.daq.initialise()

    def finalise(self):
        if self.scan_running:
            self.stop_scan()
        
        while self.scan_running:
            sleep(0.01)

        self.daq.finalise()

    def start_scan(self):
        self.scan_thread = Thread(target=self.scan_voltages)
        self.scan_thread.start()

    def stop_scan(self):
        self.keep_running = False

    def scan_voltages(self):
        if self.scan_running: 
            raise Exception('Scan already running')

        self.scan_running = True

        self.config_bkp = copy.deepcopy(self.config)

        self.voltages = np.arange(
            self.config_bkp['Scan']['start'],
            self.config_bkp['Scan']['stop'],
            self.config_bkp['Scan']['step']
        )

        self.currents = np.zeros_like(self.voltages)

        i = 0
        self.keep_running = True
        for v in self.voltages:
            self.daq.set_voltage(
                self.config_bkp['Scan']['channel_out'], 
                v
            )
            self.currents[i] = self.daq.read_voltage(self.config_bkp['Scan']['channel_in']) / self.config['DAQ']['resistance']
            i += 1
            if not self.keep_running:
                break

        self.scan_running = False

    def make_plot(self):
        plt.plot(self.voltages, self.currents, '.')
        plt.xlabel('Voltages (V)')
        plt.ylabel('Currents (A)')
        plt.title('IV of an LED')
        plt.show()

    def save_data(self):
        folder = Path(self.config['Save']['data_folder'])
        folder = folder / f'{datetime.now():%Y-%m-%d}'
        folder.mkdir(exist_ok=True, parents=True)

        full_path = folder / self.config['Save']['filename']
        i = 0
        while full_path.exists():
            i += 1
            filename = Path(self.config['Save']['filename'])
            filename = f'{filename.stem}_{i}{filename.suffix}'
            full_path = folder / filename

        np.savetxt(full_path, np.stack((self.voltages, self.currents)))
        self.save_metadata(full_path)

    def save_metadata(self, full_path):
        full_path = full_path.with_suffix('.yml')

        with open(full_path, 'w') as f:
            yaml.dump(self.config_bkp, f)


if __name__ == '__main__':
    exp = Experiment()
    exp.load_config('Examples/config.yml')
    exp.initialise()
    exp.start_scan()
    exp.config['Scan']['start'] = 2.4
    exp.save_data()
    exp.finalise()
    exp.make_plot()