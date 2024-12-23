import dataclasses

@dataclasses.dataclass
class CompJoulesParameters:

  cpu: bool = True
  gpu: bool = True
  fpga: bool = True


def energy(parameters: CompJoulesParameters):
  # Set everything up
  # Test that the hardware is accessible
  # - if not, raise an exception