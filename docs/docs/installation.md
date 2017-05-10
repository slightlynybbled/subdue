# Overview

The user must first install all hardware/software drivers which are required to interface with the hardware.  In
addition, it is advantageous for the user to install the build packages necessary for numpy and other modules that
require compilation.

A future goal of the project is to provide a full installation.  For now, there are several files that must be
individually installed in order to complete the full functionality.

# Minimum Installation Requirements

These installation files are required for all distributions.

 * [Python 3.5.2](https://www.python.org/downloads/) or greater
 * [Visual C++ Build Tools](http://landinghub.visualstudio.com/visual-cpp-build-tools)

# DC Power Supplies

Currently, the Agilent N5700 series and the Aim TTi CPX400SP are fully
supported within the AMS Test Suite.  The user must install the appropriate
drivers for the hardware.

## N5700 Drivers

 * [NI-VISA](http://www.ni.com/download/ni-visa-16.0/6184/en/)
 
## CPX400SP Drivers

 * [AMI TTI CPX400SP drivers](http://www.aimtti.us/support)

# Data Acquisition Modules (DAQ)

Currently, only the National Instruments USB-6001 is supported and tested.  To run this module, the user must install:

 * [NI-DAQmx](http://www.ni.com/download/ni-daqmx-16.0/6120/en/)

# Thermocouple Reader

Currently, only the Omega/Pico TC-08 thermocouple reader/amplifier is supported and tested.  To run this module, the
user must install:

 * [PicoLog](https://www.picotech.com/data-logger/tc-08/usb-tc-08-software)

# Subdue

After all other dependencies are satisfied, simply:

`pip install subdue`

