Welcome to CompJouleS's documentation!
**************************************

About
=====

**CompJouleS** is a comprehensive tool designed to measure energy consumption and temperature using PyJoules, NVIDIA SMI, Intel Power Gadget, and Xilinx FPGA tools. It offers insights into the performance and efficiency of systems, especially those utilizing NVIDIA GPUs and Xilinx FPGAs.

Limitation
----------

CPU, RAM and integrated GPU
^^^^^^^^^^^^^^^^^^^^^^^^^^^
**CompJouleS** uses the Intel "*Running Average Power Limit*" (RAPL) technology that estimates energy consumption of the CPU, RAM, and integrated GPU. This technology is available on Intel CPU since the `Sandy Bridge generation`__ (2010).

__ https://en.wikipedia.org/wiki/Intel#Sandy_Bridge

For now, **CompJouleS** uses the Linux kernel API to get energy values reported by RAPL technology. Thus, CPU, RAM, and integrated GPU energy monitoring are not available on Windows or MacOS.

As RAPL is not provided by a virtual machine, **CompJouleS** can't use it to monitor energy consumption inside a virtual machine.

Nvidia GPU
^^^^^^^^^^
**CompJouleS** uses the NVIDIA "*Nvidia Management Library*" technology to measure energy consumption of NVIDIA devices. The energy measurement API is only available on NVIDIA GPUs with `Volta architecture`__ (2018).

__ https://en.wikipedia.org/wiki/Volta_(microarchitecture)

Monitor only function energy consumption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**CompJouleS** monitors device energy consumption. The reported energy consumption is not solely the energy consumption of the code you are running. This includes the *global energy consumption* of all the processes running on the machine during this period, including the operating system and other applications.

We recommend eliminating any extra programs that may alter the energy consumption of the machine hosting experiments and keeping only the code under measurement (i.e., no extra applications, such as graphical interfaces, background running tasks). This will give the closest measure to the real energy consumption of the measured code.

Quickstart
==========

Installation
------------

You can install **CompJouleS** with pip:

.. code-block:: bash

   pip install compjoules

Decorate a function to measure its energy consumption
-----------------------------------------------------

To measure the energy consumed by the machine during the execution of a function ``foo()``, use the following code with the :raw-role:`<a href="API/main_api.html#pyJoules.energy_meter.measure_energy">` ``measure_energy`` :raw-role:`</a>` decorator:

.. code-block:: python

   from pyJoules.energy_meter import measure_energy
   from pyJoules.device.rapl_device import RaplPackageDomain, RaplCoreDomain

   @measure_energy(domains=[RaplPackageDomain(0), RaplCoreDomain(0)])
   def foo():
       # Instructions to be evaluated.

   foo()

This will print the recorded energy consumption of all the monitorable devices during the execution of the function ``foo``.

Advanced Features
=================

Custom Configuration
---------------------

CompJouleS allows custom configurations for different hardware setups. Refer to the documentation for configuring CompJouleS for specific use cases.

Integrating with Machine Learning Models
-----------------------------------------

CompJouleS seamlessly integrates with PyTorch-based machine learning models, providing energy and temperature insights during training and inference.

FPGA Integration
----------------

CompJouleS supports power measurement for Xilinx FPGAs using TCL scripts and DCP files. Example usage:

.. code-block:: tcl

   source <path_to_tcl_script>/measure_power.tcl
   open_checkpoint <path_to_dcp_file>/design.dcp

Future Developments
===================

For version 2, we will include:
- Computational complexity calculation
- Neuromorphic architecture integration (Loihi-2, SpiNNaker)
- Hybrid architecture integration
- Bit converter

Critical Aspects and Troubleshooting
====================================

Permission Issues
-----------------

When encountering permission errors such as:

.. code-block:: none

   PermissionError: [Errno 13] Permission denied: '/sys/class/powercap/intel-rapl/intel-rapl:0/intel-rapl:0:2/energy_uj'

Ensure you have sudo or superuser access.

Environment Setup
-----------------

For proper functionality, avoid using virtualized environments like VirtualBox as they do not provide the necessary hardware access. Prefer a native Linux installation or dual-boot setup.

Package Installation
--------------------

To avoid the "externally-managed environment" error, use a virtual environment for isolating project dependencies. Ensure all required packages such as Torch, Pandas, and Scikit-Learn are installed.

Support and Contact
===================

Issue Tracker
-------------

For reporting issues or feature requests, use the issue tracker https://compjoules.slac.stanford.edu.

Community Support
-----------------

Join our community forum for discussions and help https://compjoules.slac.stanford.edu.

Contact Information
-------------------

For direct inquiries, contact us mrtisik@stanford.edu.

Contributing
------------

If you would like to contribute code you can do so via GitHub by forking the repository and sending a pull request.

When submitting code, please make every effort to follow existing coding conventions and style in order to keep the code as readable as possible.


Table of contents
=================

.. toctree::
   :maxdepth: 2

   About <self>
   Compatible Packages/usage
   xx/xxx
   yy/yyy
   zzz/zz
