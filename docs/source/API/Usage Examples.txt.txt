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
