from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5.QtCore import QTimer
from PyQt5 import uic

from pathlib import Path


class ScanWindow(QMainWindow):
    def __init__(self, experiment):
        super().__init__()
        view_folder = Path(__file__).parent
        uic.loadUi(str(view_folder / 'scan_window.ui'), self)

        self.experiment = experiment
        self.start_button.clicked.connect(self.button_pressed)
        self.stop_button.clicked.connect(self.experiment.stop_scan)
        self.plot_button.clicked.connect(self.experiment.make_plot)

        self.start_line.setText(f"{self.experiment.config['Scan']['start']}")
        self.stop_line.setText(f"{self.experiment.config['Scan']['stop']}")
        self.step_line.setText(f"{self.experiment.config['Scan']['step']}")

        self.channel_in_line.setText(f"{self.experiment.config['Scan']['channel_in']}")
        self.channel_out_line.setText(f"{self.experiment.config['Scan']['channel_out']}")
        
        self.plot = self.plot_widget.plot(self.experiment.voltages, self.experiment.currents)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_plot)
        self.update_timer.timeout.connect(self.update_ui)
        self.update_timer.start(50)

        self.actionStart.triggered.connect(self.button_pressed)
        self.actionSave.triggered.connect(self.save_data)

    def save_data(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Choose Directory", 
            self.experiment.config['Save']['data_folder'])
        
        self.experiment.config['Save'].update({
            'data_folder': directory,
        })
        
        self.experiment.save_data()

    def button_pressed(self):
        print('Button Clicked')
        self.experiment.config['Scan'].update(
            {
                'start': float(self.start_line.text()),
                'stop': float(self.stop_line.text()),
                'step': float(self.step_line.text()),
                'channel_in': int(self.channel_in_line.text()),
                'channel_out': int(self.channel_out_line.text()),
            }
        )
        self.experiment.start_scan()
    
    def update_plot(self):
        self.plot.setData(self.experiment.voltages, self.experiment.currents)

    def update_ui(self):
        if self.experiment.scan_running:
            self.start_button.setEnabled(False)
        else:
            self.start_button.setEnabled(True)
