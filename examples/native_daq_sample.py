from subdue import daqmx

# acquire device by serial number (should be printed on the back label)
daq1 = daqmx.NIDAQmx(serial_number='1b5d8aa')
daq1.analog_out('ao0', 1.5)

# acquire device by name
daq0 = daqmx.NIDAQmx(device_name='Dev8')
daq0.analog_out('ao0', 2.5)



