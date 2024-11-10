<picture> <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Muratcanisik4/CompJouleS/docs/source/logo_dark.png">



CompJouleS - Comprehensive Energy and Temperature Estimation Tool
CompJouleS is a versatile energy estimation tool designed for detailed analysis of energy consumption and temperature across multiple hardware architectures, including CPUs, GPUs, FPGAs, and ASICs. CompJouleS employs both top-down and bottom-up approaches to deliver precise metrics, optimized for machine learning, data analytics, and custom algorithms.


## Installation
CompJouleS is installable via [pip](https://pypi.org/)
bash 
pip install compjoules


Check your [local framework](((https://compjoules.readthedocs.io/en/latest/support-and-contact.html))) for CompJouleS support.

## Usage
> Read more in our [documentation about CompJouleS usage]((https://compjoules.readthedocs.io/en/latest/index.html))

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


## About NIR
> Read more in our [documentation about NIR primitives](https://neuroir.org/docs/primitives.html)

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
This work was originally conceived at the [Telluride Neuromorphic Workshop 2023](tellurideneuromorphic.org) by the authors below (in alphabetical order):
**

If you use NIR in your work, please cite the [following arXiv preprint](https://arxiv.org/abs/2311.14641)

@unpublished{CompJouleS24,
  title        = {CompJouleS: A Cross-Platform Energy Estimation Tool for Machine Learning Algorithms on Heterogeneous Computing Architectures},
  author       = {SLAC National Laboratory/Stanford University (Sadasivan Shankar Lab)},
  note         = {Manuscript in preparation},
  year         = {2024},
  institution  = {SLAC National Accelerator Laboratory, Stanford University},
}
