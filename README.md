<p align="center">
  <img src="https://raw.githubusercontent.com/Muratcanisik4/CompJouleS/main/docs/source/compjoules_logo.png" alt="CompJouleS Logo">
</p>




# CompJouleS - Comprehensive Energy and Temperature Estimation Tool

CompJouleS is a versatile energy estimation tool designed for detailed analysis of energy consumption and temperature across multiple hardware architectures, including CPUs, GPUs, FPGAs, and ASICs. CompJouleS employs both top-down and bottom-up approaches to deliver precise metrics, optimized for machine learning, data analytics, and custom algorithms.

## Installation
CompJouleS is installable via [pip](https://pypi.org/):
bash
pip install compjoules



Check your local framework [(https://compjoules.readthedocs)](https://compjoules.readthedocs.io/en/latest/index.html)

## Required Packages

To use CompJouleS effectively, ensure you have the following packages installed:

- **PyJoules**
- **Torch**
- **Pandas**
- **Scikit-Learn**
- **Transformers**
- **Thop**
- **NVIDIA Management Library (NVML)**
- **Intel Power Gadget**

## Usage

> Read more in our [documentation about CompJouleS usage](https://compjoules.readthedocs.io/en/latest/index.html)


To end-users, CompJouleS is just a declarative format that sits between formats and will hopefully be as invisible as possible.
However, it is possible to export Python objects or CompJouleS files.

python
from pyJoules.energy_meter import measure_energy
from pyJoules.device.rapl_device import RaplPackageDomain

@measure_energy(domains=[RaplPackageDomain(0)])
def sample_task():
    # Function to measure energy consumption
    pass

sample_task()




# TCL Script: measure_power.tcl
source <path_to_tcl_script>/measure_power.tcl
open_checkpoint <path_to_dcp_file>/design.dcp

---

## About CompJouleS
> Read more in our [documentation about CompJouleS primitives](https://compjoules.readthedocs.io/en/latest/troubleshooting-and-tips.html)

On top of popular primitives such as convolutional or fully connected/linear computations, we define additional compuational primitives that are specific to neuromorphic computing and hardware implementations thereof. 
Computational units that are not specifically neuromorphic take inspiration from the Pytorch ecosystem in terms of naming and parameters (such as Conv2d that uses groups/strides).


## Supported Architectures

| **Architecture** | **Supported Measurement**      | **Examples** |
|------------------|:-----------------------------:|:------------:|
| [CPU](https://compjoules.slac.stanford.edu/docs/examples/cpu)          | Energy (RAPL)              | [CPU Example](https://compjoules.slac.stanford.edu/docs/examples/cpu) |
| [GPU (NVIDIA)](https://compjoules.slac.stanford.edu/docs/examples/gpu) | Energy (NVIDIA SMI)        | [GPU Example](https://compjoules.slac.stanford.edu/docs/examples/gpu) |
| [FPGA (Xilinx)](https://compjoules.slac.stanford.edu/docs/examples/fpga) | Power (TCL Scripts)      | [FPGA Example](https://compjoules.slac.stanford.edu/docs/examples/fpga) |
| [ASIC](https://compjoules.slac.stanford.edu/docs/examples/asic)        | Complexity Estimation      | [ASIC Example](https://compjoules.slac.stanford.edu/docs/examples/asic) |


## Future Development

Planned features include:
Neuromorphic architecture support (e.g., Loihi-2, SpiNNaker)
Enhanced complexity calculator
Hybrid architecture support


## Acknowledgements
This work was originally conceived at the [Telluride Neuromorphic Workshop 2023](https://tellurideneuromorphic.org) by the following contributors:

- Author 1
- Author 2


## Citation
If you use CompJouleS in your work, please cite the following:

```bibtex
@article{CompJouleS2024,
    title={CompJouleS: Modular Energy and Temperature Estimation Tool},
    author={SLAC National Accelerator Laboratory},
    journal={Manuscript in preparation},
    year={2024},
}
