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

To end-users, NIR is just a declarative format that sits between formats and will hopefully be as invisible as possible.
However, it is possible to export Python objects or NIR files.

python
import nir
# Write to file
nir.write("my_graph.nir", nir_graph) 

# Read file
imported_graph = nir.read("my_graph.nir")


## About NIR
> Read more in our [documentation about NIR primitives](https://neuroir.org/docs/primitives.html)

On top of popular primitives such as convolutional or fully connected/linear computations, we define additional compuational primitives that are specific to neuromorphic computing and hardware implementations thereof. 
Computational units that are not specifically neuromorphic take inspiration from the Pytorch ecosystem in terms of naming and parameters (such as Conv2d that uses groups/strides).


## Frameworks that currently support NIR

| **Framework** | **Write to NIR** | **Read from NIR** | **Examples** |
| --------------- | :--: | :--: | :------: |
| [Lava-DL](https://github.com/lava-nc/lava-dl) | ✓ | ⬚ | [Lava/Loihi examples](https://neuroir.org/docs/examples/lava/nir-conversion.html) |
| [Nengo](https://nengo.ai) | ✓ | ✓ | [Nengo examples](https://neuroir.org/docs/examples/nengo/nir-conversion.html) |
| [Norse](https://github.com/norse/norse) | ✓ | ✓ | [Norse examples](https://neuroir.org/docs/examples/norse/nir-conversion.html) |
| [Rockpool](https://rockpool.ai) ([SynSense Xylo chip](https://www.synsense.ai/products/xylo/)) | ✓ | ✓ | [Rockpool/Xylo examples](https://neuroir.org/docs/examples/rockpool/nir-conversion.html)
| [Sinabs](https://sinabs.readthedocs.io) ([SynSense Speck chip](https://www.synsense.ai/products/speck-2/)) | ✓ | ✓ | [Sinabs/Speck examples](https://neuroir.org/docs/examples/sinabs/nir-conversion.html) |
| [snnTorch](https://github.com/jeshraghian/snntorch/) | ✓ | ✓ | [snnTorch examples](https://neuroir.org/docs/examples/snntorch/nir-conversion.html) |
| [SpiNNaker2](https://spinncloud.com/portfolio/spinnaker2/) | ⬚ | ✓ | [SpiNNaker2 examples](https://neuroir.org/docs/examples/spinnaker2/import.html) |
| [Spyx](https://github.com/kmheckel/spyx) | ✓ | ✓ | [Spyx examples](https://neuroir.org/docs/examples/spyx/conversion.html)


## Acknowledgements
This work was originally conceived at the [Telluride Neuromorphic Workshop 2023](tellurideneuromorphic.org) by the authors below (in alphabetical order):
* [Steven Abreu](https://github.com/stevenabreu7)
* [Felix Bauer](https://github.com/bauerfe)
* [Jason Eshraghian](https://github.com/jeshraghian)
* [Matthias Jobst](https://github.com/matjobst)
* [Gregor Lenz](https://github.com/biphasic)
* [Jens Egholm Pedersen](https://github.com/jegp)
* [Sadique Sheik](https://github.com/sheiksadique)
* [Peng Zhou](https://github.com/pengzhouzp)

If you use NIR in your work, please cite the [following arXiv preprint](https://arxiv.org/abs/2311.14641)

article{NIR2024, 
    title={Neuromorphic intermediate representation: A unified instruction set for interoperable brain-inspired computing}, 
    author={Pedersen, Jens E. and Abreu, Steven and Jobst, Matthias and Lenz, Gregor and Fra, Vittorio and Bauer, Felix Christian and Muir, Dylan Richard and Zhou, Peng and Vogginger, Bernhard and Heckel, Kade and Urgese, Gianvito and Shankar, Sadasivan and Stewart, Terrence C. and Sheik, Sadique and Eshraghian, Jason K.}, 
    rights={2024 The Author(s)},
    DOI={10.1038/s41467-024-52259-9}, 
    number={1},
    journal={Nature Communications}, 
    volume={15},
    year={2024}, 
    month=sep, 
    pages={8122},
}
