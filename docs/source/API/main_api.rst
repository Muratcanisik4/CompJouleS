from energy_measurement import measure_energy

@measure_energy
def example_function():
    # Function logic here
    for _ in range(1000000):
        pass

example_function()
