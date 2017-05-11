# Importing

Once the `subdue` is [installed](installation.md), it can be imported and the hardware
directly utilized within your Python program.  The packages available are:

 * `subdue.daqmx`
 * `subdue.visa`
 * `subdue.thermocouple`
 
More packages and functionality may be added as required by the user base.

# Searching for Hardware

Each module of Subdue implements a search functionality which consists of two steps: (1) create
the searcher object and (2) list the attached objects by reference.  For instance, to search for
all attached DAQs:

```python
    daq_searcher = subdue.NIDAQmxSearch()
    references = daq_searcher.list_references()          # list the default references available for daqs
    models = daq_searcher.list_models()                  # list the models available  for daqs
    serial_numbers = daq_searcher.list_serial_numbers()  # list the serial numbers available for daqs
    devices = daq_searcher.list_devices()                # list complete information for daqs (returns list of dicts)
```

On completion, `references` will contain a list of values that correspond to physical devices detected
on that PC.

Currently, there are three searchers available: `subdue.NIDAQmxSearch()`, `subdue.VisaInstrumentSearch()`,
and `subdue.ThermocoupleSearch()`.  Each of these implements the `list_references()`, `list_models()`,
`list_serial_numbers()`, and `list_devices()` methods.

## References

All references may be used for direct device instantiation.  For instance:

```python 
visa_searcher = subdue.VisaInstrumentSearcher()

# store the first available VISA instrument in reference
reference = visa_searcher.list_references()[0]  
psu = PowerSupply(reference)
```

This method is useful if there is only one VISA instrument that is a power supply attached to your PC.
If more than one power supply is attached, you may wish to use the `searcher.list_devices()` method, which
will return a list of dicts, each containing the model number, serial number, and the reference.

```bash
>>> references = subdue.VisaInstrumentSearcher().list_references()
>>> print(references)
[{'serial': 'US08E6445J', 'model': 'N5768A', 'reference': 'N5768A'}]
```

# Controlling the Hardware

Unfortunately, due to the differences in operation between instrument types, it is not possible to
create a perfectly uniform API through which to program all devices in the same way.  Pains have
been taken in order to assure as much consistency as possible while still providing access to all
functionality available on a particular device.

Each piece of hardware will be allocated by associating it with an object of its type.  For instance,
a power supply would be internally represented by an instance of `subdue.PowerSupply`.

It is easiest to allocate the hardware object using the `reference` field, if possible.  Each instrument
has a different 'preferred' reference based on types and drivers.  For instance, National Instruments
hardware often populates as `DevX` whereas Visa instruments may populate using their serial number
as the preferred.

## Data Acquisition (DAQ)

The `subdue.NIDAQmx` object encompasses all of the functionality contained within the
DAQ.  To create an instance of the DAQ, one needs to specify, either, the serial number or the 
device name in the constructor:

```python
daq = subdue.NIDAQmx(device_name='Dev1')
daq = subdue.NIDAQmx(serial_number='123456')
```

Once the object is created, then its methods may be executed in order to manipulate the DAQ

### Digital Output

```python 
daq.digital_out_line(port_name, line_name, value)
```

where `port_name` and `line_name` correspond to National Instruments conventions and each may be specified
as an integer or as a string.  The `value` is `True` or `False` to set or clear the output.

For instance, to set the line labeled "port0 line1" to a high voltage state, either of the following
lines may be used to the same effect:

`daq.digital_out_line(0, 1, True)`
`daq.digital_out_line('port0', 'line1', True)`
 
### Digital Input

```python 
daq.digital_in_line(port_name, line_name)
```

Similar to digital output, `port_name` and `line_name` correspond to National Instruments conventions.
The method simply return `True` or `False` based on the pin state:

```python
if daq.digital_in_line(0, 1):
    print('port0, line0 is high!')
else:
    print('port0, line0 is low!')
```

### Analog Output

```python
daq.analog_out(analog_output, voltage)
```

where `analog_output` corresponds to NI conventions and `voltage` is a floating-point number that
represents the desired voltage.

To set the output of "ao1" to 1.25V, either of the following lines would work:

```python
daq.analog_out('ai1', 1.25)
daq.analog_out(1, 1.25)
```

### Analog Input

```python 
daq.sample_analog_in(analog_input, sample_count=1, rate=1000.0, output_format=None)
```

where:
 * `analog_input` corresponds to NI conventions
 * `sample_count` corresponds to the number of samples the programmer wishes to take
 * `rate` corresponds to the sample rate
 * `output_format` will allow the user to return a Python-native `list`
 
To read one sample of "ai1":

```python 
daq.sample_analog_in('ai1')
```

To read 10 samples of "ai1" at the default 1kHz frequency and return as a numpy array:

```python 
daq.sample_analog_in('ai1', 10)
```

To read 10 samples of "ai1" at 2kHz and return the results as a Python-native list:

```python 
daq.sample_analog_in('ai1', 10, 2000, 'list')
```

## Power Supply

The `subdue.PowerSupply` object encompasses all of the methods and functionality
applicable to power supplies.  To create an instance of the `PowerSupply`, one needs to
specify, the instrument object, the model number, or the serial number in the constructor:

```python
psu = subdue.NIDAQmx(instrument=instrument_instance)
psu = subdue.NIDAQmx(device_name='N5768A')
psu = subdue.NIDAQmx(serial_number='123456')
```

The `instrument_instance` is an instance of the `pyvisa.ResourceManager.open_resource()` object
and will seldom be utilized.

### Read PSU Voltage

```python 
psu.read_voltage()
``` 

will read and return the output voltage of the power supply.

### Read PSU Current

```python 
psu.read_current()
``` 

will read and return the output voltage of the power supply.

### Read PSU Status

```python 
psu.read_status()
``` 

will return a list of all status messages stored in the instrument.

### Reset PSU

```python 
psu.reset()
```

will reset the PSU to its power-on defaults.

### Set PSU Voltage

```python
psu.set_voltage(voltage)
```

where `voltage` is a floating-point number representing the output voltage.
 
### Set PSU Current
 
```python 
psu.set_current(current)
```
 
where `current` is a floating-point number representing the maximum output current.

### PSU on/off

The PSU may be turned on using `psu.on()` and off using `psu.off()`.

### PSU Overcurrent Protection

The overcurrent protection may be set or cleared using `psu.ocp(True)` or `psu.ocp(False)`.

## Thermocouple Reader

To utilize the thermocouple reader, first, the thermocouple reader must be allocated as an object
and the appropriate channels enabled and setup.  Once the channels are functional, then they may be
read individually in a sequence.

```python
tc = subdue.ThermocoupleReader()

tc.enable_channel(channel_number=1, tc_type='K')
tc.enable_channel(channel_number=3, tc_type='K')

while True:
    print('{} {}'.format(tc.read_one(channel_number=1), tc.read_one(channel_number=3)))
    time.sleep(1.0)
```

This code will print channels 1 and 3 to the console every 1.0s + conversion time for both channels.
