import numpy as np


voltages = np.arange(0, 3.3, 0.13)
print(voltages)

for i, v in enumerate(voltages):
    print(i, v)