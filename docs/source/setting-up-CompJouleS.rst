Setting Up CompJouleS Page
***********

.. _prerequisites:

Prerequisites
=============

To ensure that CompJouleS operates smoothly, the following prerequisites are necessary:

* **Python 3.10 or higher**: CompJouleS is built to work with Python 3.10 or newer versions. Ensure that you have the correct Python version installed on your system.
* **Linux Operating System**: For full functionality, CompJouleS requires a Linux OS. This is because tools like PyJoules rely on Linux-specific APIs to retrieve energy consumption data. Using CompJouleS on Windows or macOS may result in limited functionality.
* **Required Tools**:
  
  * **NVIDIA SMI**: The NVIDIA System Management Interface (SMI) is essential for monitoring GPU performance and energy consumption. Ensure you have it installed if you're using an NVIDIA GPU.
  * **Intel Power Gadget**: This tool is necessary for monitoring CPU power consumption on Intel CPUs. It's especially useful for energy measurement on systems with Intel processors.
  * **Xilinx FPGA Tools**: If you plan to use CompJouleS for energy measurement on FPGAs, you need to have the necessary Xilinx tools installed, including TCL scripts and DCP files.

.. _configuring-environment:

Configuring the Environment
===========================

Proper environment configuration is key to ensuring that CompJouleS can interact with the necessary hardware and tools. Follow these steps to configure your environment:

* **System PATH Configuration**: Ensure that tools like NVIDIA SMI, Intel Power Gadget, and Xilinx FPGA tools are added to your system’s PATH. This allows CompJouleS to locate and utilize these tools during energy measurements.
* **Verify Installations**: After adding the tools to your PATH, verify that they are accessible by running the respective commands (e.g., ``nvidia-smi``, ``powergadget``, and relevant Xilinx commands) in your terminal.
* **Virtual Environments**: It’s recommended to use a Python virtual environment to manage dependencies and avoid conflicts. Ensure that all required Python packages, such as PyJoules, Torch, Pandas, and Scikit-Learn, are installed within the virtual environment.

With these prerequisites and configurations, your environment should be ready to run CompJouleS effectively.
