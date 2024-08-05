Compatible Packages
*******************
To use CompJouleS effectively, ensure you have the following packages installed:

- PyJoules
- Torch
- Pandas
- Scikit-Learn
- Transformers
- Thop
- Nvidia Management Library (NVML)
- Intel Power Gadget

Installation
============
You can install the necessary packages using pip:

```bash
pip install pyJoules torch pandas scikit-learn transformers thop

Setting Up CompJouleS
Prerequisites
Python 3.10 or higher: Ensure you are using Python 3.10 or higher.
Linux OS: PyJoules requires Linux for full functionality.
NVIDIA SMI: Install NVIDIA SMI for GPU monitoring.
Intel Power Gadget: Install Intel Power Gadget for CPU power monitoring.
Xilinx FPGA tools: Ensure the necessary TCL scripts and DCP files are available for FPGA integration.
Configuring the Environment
Ensure that the tools (NVIDIA SMI, Intel Power Gadget, etc.) are correctly installed and accessible in your system's PATH.

Usage Examples
Basic Usage
To use CompJouleS, import the necessary modules and initialize the tool as per your requirements. The tool supports energy and temperature measurement for machine learning models running on either CPU, GPU, or FPGA.

.. code-block:: python
from pyJoules.energy_meter import measure_energy
from pyJoules.device.rapl_device import RaplPackageDomain, RaplCoreDomain
from pyJoules.device.nvidia_device import NvidiaGPUDomain
from pyJoules.handler.csv_handler import CSVHandler
import torch

# Example function to measure
@measure_energy(domains=[RaplPackageDomain(0), RaplCoreDomain(0), NvidiaGPUDomain(0)])
def example_function():
    # Function implementation
    pass

# Call the function
example_function()
Logging Energy Consumption
You can log energy consumption data to a CSV file:

.. code-block:: python
from pyJoules.energy_meter import measure_energy
from pyJoules.handler.csv_handler import CSVHandler
from pyJoules.device.rapl_device import RaplPackageDomain
from pyJoules.device.nvidia_device import NvidiaGPUDomain

csv_handler = CSVHandler('energy_log.csv')

@measure_energy(handler=csv_handler, domains=[RaplPackageDomain(0), NvidiaGPUDomain(0)])
def foo():
    # Instructions to be evaluated
    pass

for _ in range(100):
    foo()

csv_handler.save_data()
Using Context Manager
To add tagged "breakpoints" in your measurement, use the context manager:

.. code-block:: python
from pyJoules.energy_meter import EnergyContext
from pyJoules.device.rapl_device import RaplPackageDomain
from pyJoules.device.nvidia_device import NvidiaGPUDomain
from pyJoules.handler.csv_handler import CSVHandler

csv_handler = CSVHandler('result.csv')

with EnergyContext(handler=csv_handler, domains=[RaplPackageDomain(1), NvidiaGPUDomain(0)], start_tag='foo') as ctx:
    # First part of the function
    ctx.record(tag='bar')
    # Second part of the function

csv_handler.save_data()
