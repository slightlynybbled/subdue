import time
from subdue import PowerSupply

psu = PowerSupply(model_number='N5768A')

# power supply control commands

# write to PSU voltage
psu.set_voltage(10.0)
psu.set_current(3.0)
psu.ocp(True)
psu.on()

time.sleep(0.5)  # wait for output to stabilize before attempting a read

print(psu.read_voltage())
print(psu.read_current())
print(psu.read_status())

psu.reset()
