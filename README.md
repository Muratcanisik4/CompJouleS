<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://github.com/yourusername/CompJouleS/raw/main/docs/logo_dark.png">
<img alt="CompJouleS Logo" src="https://github.com/yourusername/CompJouleS/raw/main/docs/logo_light.png">
</picture>

# CompJouleS - Comprehensive Energy and Temperature Estimation Tool

**CompJouleS** is a versatile energy estimation tool designed for detailed analysis of energy consumption and temperature across multiple hardware architectures, including CPUs, GPUs, FPGAs, and ASICs. CompJouleS employs both top-down and bottom-up approaches to deliver precise metrics, optimized for machine learning, data analytics, and custom algorithms.

## Installation
CompJouleS is available on [pip](https://pypi.org/):
```bash
pip install compjoules
Usage
Read more in our CompJouleS documentation

Below is an example of using CompJouleS to measure energy consumption of a function.

python
Kodu kopyala
from pyJoules.energy_meter import measure_energy
from pyJoules.device.rapl_device import RaplPackageDomain

@measure_energy(domains=[RaplPackageDomain(0)])
def sample_task():
    # Function to measure energy consumption
    pass

sample_task()
Advanced Features
Complexity-Based Energy Estimation
CompJouleS supports complexity-based energy estimations, beneficial for intensive computational tasks:

python
Kodu kopyala
from compjoules import complexity_calculator

def calculate_energy_complexity():
    # Code for complexity-based energy estimation
    pass
Machine Learning Model Integration (PyTorch)
Easily monitor energy consumption for PyTorch-based machine learning models during training and inference:

python
Kodu kopyala
import torch
from pyJoules.energy_meter import measure_energy

@measure_energy(domains=[RaplPackageDomain(0)])
def train_model():
    # PyTorch model training loop
    pass

train_model()
FPGA Power Measurement
For power consumption on Xilinx FPGAs, use the following TCL scripts:

tcl
Kodu kopyala
# TCL Script: measure_power.tcl
source <path_to_tcl_script>/measure_power.tcl
open_checkpoint <path_to_dcp_file>/design.dcp
Supported Architectures
Architecture	Supported Measurement	Example
CPU	Energy (RAPL)	CPU Example
GPU (NVIDIA)	Energy (NVIDIA SMI)	GPU Example
FPGA (Xilinx)	Power (TCL Scripts)	FPGA Example
ASIC	Complexity Estimation	ASIC Example
Future Development
Planned features include:

Neuromorphic architecture support (e.g., Loihi-2, SpiNNaker)
Enhanced complexity calculator
Hybrid architecture support
Troubleshooting
Permission Issues: Run with superuser privileges to avoid permission errors.
Environment Setup: Use a native Linux setup instead of virtualized environments for optimal performance.
Dependency Conflicts: Use a virtual environment to manage dependencies.
Acknowledgements
CompJouleS was developed at SLAC National Accelerator Laboratory in collaboration with Stanford University.

Citation
If you use CompJouleS in your research, please cite:

bibtex
@article{CompJouleS2024,
    title={CompJouleS: Modular Energy and Temperature Estimation Tool},
    author={Your Name and Team},
    journal={SLAC National Accelerator Laboratory},
    year={2024},
}
