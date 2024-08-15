Compatible Packages
*********
.. _required-packages:

Required Packages
=================

To use CompJouleS effectively, ensure you have the following packages installed:

* PyJoules
* Torch
* Pandas
* Scikit-Learn
* Transformers
* Thop
* Nvidia Management Library (NVML)
* Intel Power Gadget

These packages provide the necessary functionality to measure energy consumption, monitor device performance, and integrate with machine learning models.

.. _installation:

Installation
============

You can install the necessary packages using ``pip``. Run the following command in your terminal:

.. code-block:: bash

    pip install pyJoules torch pandas scikit-learn transformers thop

This will install the core Python packages required for CompJouleS. Additionally, ensure that NVIDIA SMI and Intel Power Gadget are properly installed on your system, as they are required for GPU and CPU power monitoring.

For Xilinx FPGA integration, make sure you have the necessary TCL scripts and DCP files available.

By following these steps, you'll have all the necessary packages and tools installed for effective use of CompJouleS.
