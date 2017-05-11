import subdue

# list all thermocouple devices
print('--------------------------------')
search = subdue.ThermocoupleSearch()
print('thermocouple references: ', search.list_references())
print('thermocouple model numbers: ', search.list_models())
print('thermocouple serial numbers: ', search.list_serial_numbers())
print('thermocouple complete information: ', search.list_devices())

# list all visa devices
print('--------------------------------')
search = subdue.VisaInstrumentSearch()
print('visa references: ', search.list_references())
print('visa model numbers: ', search.list_models())
print('visa serial numbers: ', search.list_serial_numbers())
print('visa complete information: ', search.list_devices())

# list all NI DAQmx devices
print('--------------------------------')
search = subdue.NIDAQmxSearch()
print('NI DAQmx references: ', search.list_references())
print('NI DAQmx model numbers: ', search.list_models())
print('NI DAQmx serial numbers: ', search.list_serial_numbers())
print('NI DAQmx complete information: ', search.list_devices())
