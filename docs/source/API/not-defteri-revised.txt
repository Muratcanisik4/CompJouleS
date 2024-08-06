
# CompJouleS

## Usage Examples

### Basic Usage

#### Example of measuring energy consumption with a basic function

```python
from compjoules import measure_energy

@measure_energy
def my_function():
    # Your function logic here
    pass

my_function()
```

#### Explanation of the `measure_energy` decorator

The `measure_energy` decorator is used to measure the energy consumption of a function. When applied to a function, it automatically logs the energy usage during the function's execution.

### Logging Energy Consumption

#### Example of logging energy data to a CSV file

```python
from compjoules import measure_energy, CSVHandler

csv_handler = CSVHandler('energy_log.csv')

@measure_energy(handler=csv_handler)
def my_function():
    # Your function logic here
    pass

my_function()
```

#### Explanation of `CSVHandler` and its usage

`CSVHandler` is used to log energy consumption data to a CSV file. By passing an instance of `CSVHandler` to the `measure_energy` decorator, you can automatically record energy data in the specified CSV file.

### Using Context Manager

#### Adding tagged "breakpoints" in measurement

```python
from compjoules import EnergyContext

with EnergyContext() as context:
    # Code block 1
    context.tag('block1')
    # Code block 2
    context.tag('block2')
```

#### Example of using `EnergyContext`

The `EnergyContext` class allows for more granular energy measurements within a block of code. By using the `tag` method, you can add tagged breakpoints to differentiate between different parts of the code being measured.
