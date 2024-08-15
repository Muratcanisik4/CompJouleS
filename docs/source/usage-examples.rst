Usage Examples
*********

.. _basic-usage:

Basic Usage
===========

In this section, we demonstrate how to measure energy consumption with a basic function using CompJouleS.

.. _measuring-energy-basic:

Measuring Energy Consumption with a Basic Function
--------------------------------------------------

To measure the energy consumption of a function, you can use the ``measure_energy`` decorator. This decorator allows you to specify the devices to monitor during the execution of your function.

.. code-block:: python

    from pyJoules.energy_meter import measure_energy
    from pyJoules.device.rapl_device import RaplPackageDomain, RaplCoreDomain
    from pyJoules.device.nvidia_device import NvidiaGPUDomain

    @measure_energy(domains=[RaplPackageDomain(0), RaplCoreDomain(0), NvidiaGPUDomain(0)])
    def example_function():
        # Function implementation
        pass

    example_function()

In this example, the ``measure_energy`` decorator is applied to ``example_function``, monitoring the energy consumption of the CPU package, CPU core, and NVIDIA GPU.

.. _logging-energy-consumption:

Logging Energy Consumption
==========================

In addition to measuring energy consumption, you can log the data to a CSV file for further analysis.

.. _using-csvhandler:

Using CSVHandler to Log Energy Data
-----------------------------------

To log energy consumption data, you can use the ``CSVHandler`` class. This allows you to save the energy measurements into a CSV file.

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

In this example, the energy consumption of the ``foo`` function is measured and logged to the ``energy_log.csv`` file after 100 iterations.

.. _using-context-manager:

Using Context Manager
=====================

To add more flexibility to your measurements, such as tagging specific points within your code, you can use the ``EnergyContext`` context manager.

.. _adding-tagged-breakpoints:

Adding Tagged "Breakpoints" in Measurement
------------------------------------------

Using the ``EnergyContext`` allows you to tag different parts of your code to measure energy consumption between specific points.

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

In this example, the energy consumption is measured from the start of the ``EnergyContext`` to the ``ctx.record`` call (tagged as 'foo') and then from the ``ctx.record`` call to the end (tagged as 'bar'). The results are saved in the ``result.csv`` file.
