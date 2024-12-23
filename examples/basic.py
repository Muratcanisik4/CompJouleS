# Basic example
import compjoules as cj

@cj.energy(cj.CompJoulesParameters(cpu=False), outputfile="test.csv")
def my_model():
  ...

cj.measure_train_start()
# Train model
cj.measure_train_stop()

cj.measure_inference_start()
# Run inference
cj.measure_inference_stop()