import subdue

# list all thermocouple devices
search = subdue.ThermocoupleSearch()
print('thermocouple readers: ', search.list_devices())

# list all visa devices
search = subdue.VisaInstrumentSearch()
print('visa instruments: ', search.list_devices())

# list all NI DAQmx devices
search = subdue.NIDAQmxSearch()
print('NI DAQmx devices: ', search.list_devices())
