# Purpose

The purpose of the AMS Hardware Suite is to provide access to hardware from various vendors for
which National Instruments LabView drivers are typically provided.
 
This access is written using Python, a dynamic textual language.  One goal of this project is
to allow the author to utilize the language of their choosing by exposing an interface via http
so that any language may be utilized for the control of attached instrumentation.

# Modes

There are two modes in which this software package may execute: `native python` and `standalone`.  These
modes are not mutually exclusive on a particular machine, but a particular instrument may not
be allocated to two executing processes.

## Native Python

When utilized as a native Python library, the user need only perform the proper imports to gain
access to all hardware functionality directly:

```python
from subdue import *
```

This gives the executing native process direct access to the hardware and will result in the most
dynamic use of the hardware.

## Standalone

The software will also execute in standalone mode.  Standalone mode will start an http server on
the local host and simply wait for commands to be sent to it.  Each command will result in the
server returning an appropriate response depending on the command executed.

Standalone mode allows the software author to write the program in any language without necessarily
having ports to that language for hardware control.  So long as the language has the base capacity
to send http requests, then the hardware may be controlled through the interface.  There is a typical
15ms to 40ms delay between command and response, depending on a multitude of factors, but the basic
functionality remains much the same as the native mode.

The URL is `http://127.0.0.1:5001`.  When standalone mode is active, a `GET` request (open a browser)
to this url will result in a brief documentation package being printed to the screen. Polling the
`/attached` path will result in returning details about all attached hardware.  For instance:

request:
```
"GET /attached HTTP/1.1"
```

response:
```json
{
  "daq": [
    ""
  ], 
  "visa": [
    {
      "Manufacturer": "TEKTRONIX", 
      "ModelNumber": "MSO4034", 
      "SerialNumber": "C020160"
    }
  ]
}
```

The above response indicates that there is no DAQ attached and one VISA instrument attached.
