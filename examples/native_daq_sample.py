from subdue import daqmx

# acquire device by serial number
daq0 = daqmx.NIDAQmx(serial_number='1b5d935')
daq0.analog_out('ao0', 1.5)

# acquire device by name
daq1 = daqmx.NIDAQmx(device_name='Dev1')
daq0.analog_out('ao0', 2.5)

