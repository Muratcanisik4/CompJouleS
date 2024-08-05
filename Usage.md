# Usage Examples

## Basic Usage
Example of measuring energy consumption with a basic function.

```python
@measure_energy
def basic_function():
    # Your code here
    pass
from energy_logger import CSVHandler

@measure_energy(handler=CSVHandler('energy_log.csv'))
def function_with_logging():
    # Your code here
    pass
with EnergyContext(tag='example'):
    # Your code here
    pass
