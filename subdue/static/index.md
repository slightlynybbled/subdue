# AMS Hardware Server, __version__

The AMS Hardware Server will support the following hardware:

 * NI USB-600x DAQ
 * Pico/Omega TC-08 Thermocouple Reader
 * Agilent N5700 series Power Supplies
 
This package may be imported and utilized directly by a python package or it may be run free-standing
and interfaced with a test suite in any language using standard network traffic.

---

# Communicating with the Server

Requests are sent to the server on port 5001.  For instance, if you were running at 'localhost', then
the base url for all requests would be 'http://localhost:5001'.

All requests are to be sent as a POST request in JSON format.  Requests that "write to" hardware
should expect no returns while requests that "read from" hardware should expect an appropriate return
value.

All data received will be JSON formatted.

---

# Listing Devices

Following the '/attached' url will return a list of currently attached devices.  This will also provide
a guide for determining the url of the specific device.  For instance, if object returned is:

    {
        "daq": [
            "Dev1",
            "Dev4"
        ]
    }
    
then you will know that you can access devices at `/daq/Dev1` and `/daq/Dev4`.  Other options:

    {
        "daq": [
            "Dev1",
            "Dev4"
        ],
        
        "thermocouple": [
        "TC-08"
        ],
        
        "psu": [
            "N5765A"
        ]
    }

---

# Data Acquisition

All data acquisition operations occur on the '/daq/<device name>' url.  For instance, a USB-6001 will
likely populate on the operating system as 'Dev1', so the url would be '/daq/Dev1'.

The 'operation' field will be present on all daq-oriented requests.

 * digital output - writes to a digital output, specified by using operation 'do'
 * digital input - reads from a digital input, specified by using operation 'di'
 * analog output - writes to an analog output, specified by using operation 'ao'
 * analog input = reads from an analog input, specified by using operation 'ai'

## Write Digital Output

For digital writes, the 'value' field shall be a 1 or 0.

 * request:`{"operation": "do", "port": 0, "line": 0, "value": 1}`

 * response: `{}`

## Read Digital Input

 * request:`{"operation": "di", "port": 0, "line": 0}`

 * response:`{"operation": "di", "port": 0, "line": 0, "value": True}`

## Write Analog Output

 * request:`{"operation": "ao", "ao": 0, "value": 1.25}`

 * response:`{}`

## Read Analog Input

 * request:`{"operation": "ai", "ai": 0}`

 * response:`{"operation": "ai", "ai": 0, "value": 1.25}`
 
---

# Thermocouple

Currently, the only thermocouple device supported is the Pico/Omega USB-TC-08, which consists of a USB
device capable of reading up to 8 channels and one additional 'cold junction' channel.  There
should only be *ONE* TC-08 thermocouple reader attached to the PC at any given time.

Channel 0 will give the temperature of the cold junctions while all other channels will give the
corresponding thermocouple temperature.  All values will be in degrees C.  If a thermocouple type is not
supplied, then it will be assumed to be type J.

 * request:`{"channel": 0, "type"="J"}`

 * response:`{"channel": 0, "value": 42.2, "unit": "Celsius"}`
 
If a list of channels is sent, then all will be converted and returned:

 * request:`[{"channel": 0}, {"channel": 4}]`

 * response:`[{"channel": 0, "value": 42.2, "unit": "Celsius"}, {"channel": 4, "value": 28.9, "Celsius"}]`

---

# Power Supply

Power supplies are read/write devices which may be controlled using similar methods to DAQ read/writes.

## Write Voltage

 * request: `{"operation": "write", "parameter": "voltage", "value": 10.0}`
 
 * response: `{}`
 
## Write Current

 * request: `{"operation": "write", "parameter": "current", "value": 10.0}`
 
 * response: `{}`
 
## Write Overcurrent Protection (OCP)

 * request: `{"operation": "write", "parameter": "ocp", "value": true}`
 
 * response: `{}`
 
## Write Output On/Off

 * request: `{"operation": "write", "parameter": "output", "value": true}`
 
 * response: `{}`
 
## Read Voltage

 * request: `{"operation": "read", "parameter": "voltage"}`
 
 * response: `{"operation": "read", "parameter": "voltage", "value": 10.0}`
 
## Read Current

 * request: `{"operation": "read", "parameter": "current"}`
 
 * response: `{"operation": "read", "parameter": "current", "value": 10.0}`
 
## Read Status

Reading the status will return a list of current status indicators.

 * request: `{"operation": "read", "parameter": "status"}`
 
 * response: `{"operation": "read", "parameter": "status", "value": []}`

## Reset

Reset the PSU

 * request: `{"operation": "reset"}`
