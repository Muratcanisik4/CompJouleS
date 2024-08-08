CSV Handler
*******
# Setting Up CompJouleS

## Prerequisites
- Python 3.10 or higher.
- Linux OS for full functionality.
- Tools:
  - NVIDIA SMI
  - Intel Power Gadget
  - Xilinx FPGA tools

## Configuring the Environment
Ensure that the tools (NVIDIA SMI, Intel Power Gadget, etc.) are correctly installed and accessible in your system's PATH.

### Steps to Configure the Environment

1. **Install Python 3.10 or higher:**
    ```bash
    sudo apt update
    sudo apt install python3.10
    ```

2. **Install NVIDIA SMI:**
    - NVIDIA SMI comes with the NVIDIA driver. Ensure you have the latest NVIDIA driver installed:
      ```bash
      sudo apt-get install nvidia-driver-460
      ```

3. **Install Intel Power Gadget:**
    - Download the Intel Power Gadget from the [Intel website](https://software.intel.com/content/www/us/en/develop/articles/intel-power-gadget.html).
    - Follow the installation instructions provided on the site.

4. **Install Xilinx FPGA tools:**
    - Download and install Vivado from the [Xilinx website](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools.html).
    - Ensure the necessary TCL scripts and DCP files are available for FPGA integration.

5. **Set the PATH environment variable:**
    ```bash
    export PATH=$PATH:/usr/local/cuda/bin:/opt/intel/power_gadget
    ```

6. **Install necessary Python packages:**
    ```bash
    pip install pyJoules torch pandas scikit-learn transformers thop
    ```

By following these steps, you will ensure that your environment is correctly configured to use CompJouleS effectively.
from energy_measurement import measure_energy, CSVHandler

csv_handler = CSVHandler('energy_log.csv')

@measure_energy(handler=csv_handler)
def my_function():
    # Fonksiyonunuzun implementasyonu
    pass

my_function()


