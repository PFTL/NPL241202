from PyQt5.QtWidgets import QApplication

from PFTL.model.experiment import Experiment
from PFTL.view.main_window import ScanWindow


exp = Experiment()
exp.load_config('Examples/config.yml')
exp.initialise()

app = QApplication([])
win = ScanWindow(exp)  
win.show()
app.exec()