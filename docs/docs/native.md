# Importing

Once the `subdue` is [installed](installation.md), it can be imported and the hardware
directly utilized within your Python program.  The packages available are:

 * `subdue.daqmx`
 * `subdue.visa`
 * `subdue.tc08`
 
More packages and functionality may be added as required by the user base.

# Searching for Hardware

Each module of the AMS Hardware Suite implements a search functionality which consists of two
steps: (1) create the searcher object and (2) list the attached objects.  For instance, to search
for all attached DAQs:

```python
    s = subdue.daqmx.NIDAQmxSearch()
    devices = s.list_devices()
```

On completion, `devices` will contain a list of values that correspond to physical devices detected
on that PC.

# Controlling the Hardware

Unfortunately, due to the differences in operation between instrument types, it is not possible to
create a perfectly uniform API through which to program all devices in the same way.  Pains have
been taken in order to assure as much consistency as possible while still providing access to all
functionality available on a particular device.

Each piece of hardware will be allocated by associating it with an object of its type.  For instance,
a power supply would be internally represented by an instance of `ams_hw_suite.visa.PowerSupply`.

## Data Acquisition (DAQ)

The `ams_hw_suite.daqmx.NIDAQmx` object encompasses all of the functionality contained within the
DAQ.  To create an instance of the DAQ, one needs to specify, either, the serial number or the 
device name in the constructor:

```python
daq = subdue.daqmx.NIDAQmx(device_name='Dev1')
daq = subdue.daqmx.NIDAQmx(serial_number='123456')
```

Once the object is created, then its methods may be executed in order to manipulate the DAQ

### Digital Output

`daq.digital_out_line(port_name, line_name, value)`

where `port_name` and `line_name` correspond to National Instruments conventions and each may be specified
as an integer or as a string.  The `value` is `True` or `False` to set or clear the output.

For instance, to set the line labeled "port0 line1" to a high voltage state, either of the following
lines may be used to the same effect:

`daq.digital_out_line(0, 1, True)`
`daq.digital_out_line('port0', 'line1', True)`
 
### Digital Input

`daq.digital_in_line(port_name, line_name)`

Similar to digital output, `port_name` and `line_name` correspond to National Instruments conventions.
The method simply return `True` or `False` based on the pin state:

```python
if daq.digital_in_line(0, 1):
    print('port0, line0 is high!')
else:
    print('port0, line0 is low!')
```

### Analog Output

`daq.analog_out(analog_output, voltage)`

where `analog_output` corresponds to NI conventions and `voltage` is a floating-point number that
represents the desired voltage.

To set the output of "ao1" to 1.25V, either of the following lines would work:

```python
daq.analog_out('ai1', 1.25)
daq.analog_out(1, 1.25)
```

### Analog Input

`daq.sample_analog_in(analog_input, sample_count=1, rate=1000.0, output_format=None)`

where:
 * `analog_input` corresponds to NI conventions
 * `sample_count` corresponds to the number of samples the programmer wishes to take
 * `rate` corresponds to the sample rate
 * `output_format` will allow the user to return a Python-native `list`
 
To read one sample of "ai1":

`daq.sample_analog_in('ai1')`

To read 10 samples of "ai1" at the default 1kHz frequency and return as a numpy array:

`daq.sample_analog_in('ai1', 10)`

To read 10 samples of "ai1" at 2kHz and return the results as a Python-native list:

`daq.sample_analog_in('ai1', 10, 2000, 'list')`

## Power Supply

The `ams_hw_suite.visa.PowerSupply` object encompasses all of the methods and functionality
applicable to power supplies.  To create an instance of the `PowerSupply`, one needs to
specify, the instrument object, the model number, or the serial number in the constructor:

```python
psu = subdue.visa.NIDAQmx(instrument=instrument_instance)
psu = subdue.visa.NIDAQmx(device_name='N5768A')
psu = subdue.visa.NIDAQmx(serial_number='123456')
```

The `instrument_instance` is an instance of the `pyvisa.ResourceManager.open_resource()` object
and will seldom be utilized.

### Read PSU Voltage

`psu.read_voltage()` will read and return the output voltage of the power supply.

### Read PSU Current

`psu.read_current()` will read and return the output voltage of the power supply.

### Read PSU Status

`psu.read_status()` will return a list of all status messages stored in the instrument.

### Reset PSU

`psu.reset()` will reset the PSU to its power-on defaults.

### Set PSU Voltage

`psu.set_voltage(voltage)`

where `voltage` is a floating-point number representing the output voltage.
 
### Set PSU Current
 
`psu.set_current(current)`
 
where `current` is a floating-point number representing the maximum output current.

### PSU on/off

The PSU may be turned on using `psu.on()` and off using `psu.off()`.

### PSU Overcurrent Protection

The overcurrent protection may be set or cleared using `psu.ocp(True)` or `psu.ocp(False)`.

## Thermocouple Reader

tc stuff
