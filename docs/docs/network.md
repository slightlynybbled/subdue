# Running on the Command Line

To begin execution, go to the command line and execute

    C:> subdue
    
If the `subdue` is installed in a virtual environment, that environment may need to be
activated before this command will function properly.  If you wish to ensure that the server
is up and running, then you may open a browser and navigate to the 
[subdue web server](http://127.0.0.1:5001) and you will see a brief summary of
capabilities.

Navigate to [/attached](http://127.0.0.1:5001/attached) to see all attached hardware.

# Data Acquisition (DAQ)

All data acquisition operations occur on the '/daq/<device_name>' url. For instance, a 
USB-6001 will likely populate on the operating system as 'Dev1', so the url would be
'/daq/Dev1'.

The 'operation' field will be present on all daq-oriented requests.

 - `digital output` - writes to a digital output, specified by using operation 'do'
 - `digital input` - reads from a digital input, specified by using operation 'di'
 - `analog output` - writes to an analog output, specified by using operation 'ao'
 - `analog input` = reads from an analog input, specified by using operation 'ai'
 
All operations that specify a particular input or output of harware will, where possible,
adhere to conventions established by National Instruments.  For instance, some vendors
might call a DAQ digital input a 'pin' while national instruments calls a DAQ digital
input by `port` and `line`, so we will use the `port` and `line` conventions.  Generally,
the field `value` will be utilized to communicate state of the pin.

## Write Digital Output

For digital writes, a `value` of `1`, `true`, `"hi"`, or `"high"` will result in the pin
being set.  Otherwise, it will be cleared.  

 - request:`{"operation": "do", "port": 0, "line": 0, "value": 1}`
 - response: `{}`

## Read Digital Input

Reads of the port will return a `value` of `true` or `false`.

 - request: `{"operation": "di", "port": 0, "line": 0}`
 - response: `{"operation": "di", "port": 0, "line": 0, "value": true}`

## Write Analog Output

 - request: `{"operation": "ao", "ao": 0, "value": 1.25}`
 - response: `{}`

## Read Analog Input

If `samples` is `1` or not specified, then the hardware will gather a single sample
and return it in the `value`:

 - request: `{"operation": "ai", "ai": 0}`
 - response: `{"operation": "ai", "ai": 0, "value": 1.25}`

If `samples` is greater than `1`, then the hardware will gather the number of samples
specified.  In addition, the `sample rate` may be specified, in Hertz, in order to determine
the sample rate.  The `sample rate` defaults to `1000`.  When the number of samples is
greater than 1, then the value returned will be a JSON array:

 - request: `{"operation": "ai", "ai": 0, "samples": 4 "sample rate": 1000}`
 - response: `{"operation": "ai", "ai": 0, "value": [1.24, 1.25, 1.245, 1.25]}`

# Power Supply

Power supplies are read/write devices which may be controlled using similar methods 
to DAQ read/writes.

The general sequence for setting up power supplies:

 1. write to the voltage
 2. write to the current
 3. write to the OCP (optional)
 4. write to on/off
 
This is much like setting up the PSU using the front panel.  Be aware that if the current
protection is triggered during operation, user software will have to poll the status or the 
voltage output in order to detect the error.

## Write Voltage

 - request: `{"operation": "write", "parameter": "voltage", "value": 10.0}`
 - response: `{}`

## Write Current

 - request: `{"operation": "write", "parameter": "current", "value": 10.0}`
 - response: `{}`

## Write Overcurrent Protection (OCP)

 - request: `{"operation": "write", "parameter": "ocp", "value": true}`
 - response: `{}`

## Write Output On/Off

A `value` of `true` will result in the power supply output being turned on while `false` will
result in the power supply output being turned off.

 - request: `{"operation": "write", "parameter": "output", "value": true}`
 - response: `{}`

## Read Voltage

 - request: `{"operation": "read", "parameter": "voltage"}`
 - response: `{"operation": "read", "parameter": "voltage", "value": 10.0}`

## Read Current

 - request: `{"operation": "read", "parameter": "current"}`
 - response: `{"operation": "read", "parameter": "current", "value": 10.0}`

## Read Status

Reading the status will return a list of current status indicators.

 - request: `{"operation": "read", "parameter": "status"}`
 - response: `{"operation": "read", "parameter": "status", "value": []}`

## Reset

Reset the PSU.

 - request: `{"operation": "reset"}`
 - response: `{}`
