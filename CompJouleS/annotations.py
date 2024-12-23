import dataclasses

@dataclasses.dataclass
class CompJoulesParameters:

  cpu: bool = True
  gpu: bool = True
  fpga: bool = True

  output_file: str


def energy(parameters: CompJoulesParameters):
  # Set everything up
  if parameters.cpu:
    # Initialize CPU...
    pass

  if parameters.gpu:
    # Initialize GPU...
    pass

  if parameters.fpga:
    # Initialize FPGA...
    pass

  # Test that the hardware is accessible
  # - if not, raise an exception