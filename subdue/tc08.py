"""
This file will interface with the TC-08 thermocouple reader from Pico Technologies
(or the clone from Omega).
"""

from enum import Enum
import ctypes
import numpy as np
import os
import time

from subdue.base_classes import HardwareSearch


class TemperatureUnits(Enum):
    """
    An enumeration for the temperature units
    """
    CENTIGRADE = 0
    FAHRENHEIT = 1
    KELVIN = 2
    RANKINE = 3


class TcType(Enum):
    """
    An enumeration for the thermocouple type
    """
    DISABLED = " "
    B = "B"
    E = "E"
    J = "J"
    K = "K"
    N = "N"
    R = "R"
    S = "S"
    T = "T"

    @classmethod
    def ordinal(cls, tc_type):
        """
        Retrieves enumeration
        :param tc_type: the thermocouple type
        :return: the thermocouple type
        """
        if isinstance(tc_type, Enum):
            tc_type = tc_type.value

        return ord(tc_type)


class ThermocoupleSearch(HardwareSearch):
    def __init__(self):
        pass

    def list_devices(self):
        try:
            reader = ThermocoupleReader()
            return [reader.model]
        except AttributeError:
            return []


class ThermocoupleReader:
    def __init__(self, model_number='TC-08', types=None):
        self.reader = Tc08Usb()
        self.model = model_number

    def available_channels(self):
        return [str(i) for i in range(9)]

    def enable_channel(self, channel_number, tc_type):
        if channel_number not in range(9):
            raise ValueError('channel number must be between 0 and 8 (inclusive)')
        if not isinstance(tc_type, TcType):
            if not isinstance(tc_type, str):
                raise ValueError('tc_type must be of type TcType')
            else:
                tc_type = TcType(tc_type)

        self.reader.set_channel(channel_number, tc_type)

    def read_all(self, output_format=None):
        self.reader.get_single()

        # return a dict of values keyed using the channel numbers
        if not output_format:
            return {i: self.reader[i] for i in range(9) if not np.isnan(self.reader[i])}
        elif output_format == 'float':
            return {i: float(self.reader[i]) for i in range(9) if not np.isnan(self.reader[i])}

    def read_one(self, channel_number):
        self.reader.get_single()
        return self.reader[channel_number]


class Tc08Error(Enum):
    """
    Enumeration for determining the error codes
    """
    OK = 0
    OS_NOT_SUPPORTED = 1
    NO_CHANNELS_SET = 2
    INVALID_PARAMETER = 3
    VARIANT_NOT_SUPPORTED = 4
    INCORRECT_MODE = 5
    ENUMERATION_INCOMPLETE = 6
    NOT_RESPONDING = 7
    FW_FAIL = 8
    CONFIG_FAIL = 9
    NOT_FOUND = 10
    THREAD_FAIL = 11
    PIPE_INFO_FAIL = 12
    NOT_CALIBRATED = 13
    PICOPP_TOO_OLD = 14
    COMMUNICATION = 15

    @classmethod
    def help(cls, error):
        """
        Returns a string that corresponds to the error

        :param error: the error number
        :return: a string representing the error
        """
        d = {
            Tc08Error.OK: "No error occurred.",
            Tc08Error.OS_NOT_SUPPORTED: "The driver supports Windows XP SP3, Windows Vista, Windows 7 and Windows 8.",
            Tc08Error.NO_CHANNELS_SET: "A call to usb_tc08_set_channel() is required.",
            Tc08Error.INVALID_PARAMETER: "One or more of the function arguments were invalid.",
            Tc08Error.VARIANT_NOT_SUPPORTED: "The hardware version is not supported. Download the latest driver.",
            Tc08Error.INCORRECT_MODE: "An incompatible mix of legacy and non-legacy functions was called (or usb_tc08_get_single() was called while in streaming mode.)",
            Tc08Error.ENUMERATION_INCOMPLETE: "usb_tc08_open_unit_async() was called again while a background enumeration was already in progress.",
            Tc08Error.NOT_RESPONDING: "Cannot get a reply from a USB TC-08.",
            Tc08Error.FW_FAIL: "Unable to download firmware.",
            Tc08Error.CONFIG_FAIL: "Missing or corrupted EEPROM.",
            Tc08Error.NOT_FOUND: "Cannot find enumerated device.",
            Tc08Error.THREAD_FAIL: "A threading function failed.",
            Tc08Error.PIPE_INFO_FAIL: "Can not get USB pipe information.",
            Tc08Error.NOT_CALIBRATED: "No calibration date was found.",
            Tc08Error.PICOPP_TOO_OLD: "An old picopp.sys driver was found on the system.",
            Tc08Error.COMMUNICATION: "The PC has lost communication with the device."
        }
        return d[error]


class Tc08Usb(object):
    """
    Used to open an instance and interact with the TC-08 device
    """

    def __init__(self, dll_path="", mains_freq=60):
        """
        Initializes the device drivers
        :param dll_path: the path to the dll (default should detect)
        :param mains_freq: the mains frequency
        """
        dll_filename = os.path.join(dll_path, 'usbtc08.dll')

        self._dll = ctypes.windll.LoadLibrary(dll_filename)

        self._handle = None  # handle for device

        self._temp = np.zeros((9,), dtype=np.float32)
        self._overflow_flags = np.zeros((1,), dtype=np.int16)

        self._units = TemperatureUnits.CENTIGRADE  # 0:C 1:F 2:K 3:RK

        if self._dll:
            self._handle = self._dll.usb_tc08_open_unit()

            if self._handle == 0:
                raise AttributeError('Error: USB-TC08 unit not found on system')
            elif self._handle == -1:
                raise AttributeError('Error: {}'.format(self.get_error()))

            self._dll.usb_tc08_set_mains(self._handle, mains_freq)

    def get_error(self):
        return Tc08Error(self._dll.usb_tc08_get_last_error())

    def set_channel(self, channel, tc_type):
        """
        Sets the channel hardware parameters

        :param channel: the channel number (0 for the thermocouple cold junction)
        :param tc_type: the thermocouple type
        :return: None
        """
        tc_type = TcType.ordinal(tc_type)
        self._dll.usb_tc08_set_channel(self._handle, channel, tc_type)

    def get_single(self):
        """
        Sets the mode to 'single measurement' mode

        :return: None
        """
        self._dll.usb_tc08_get_single(self._handle,
                                      self._temp.ctypes.data,
                                      self._overflow_flags.ctypes.data,
                                      self._units.value)

    def __getitem__(self, channel):
        """
        Retrieves the temperature for a particular channel

        :param channel: the channel number
        :return: the temperature
        """
        return self._temp[channel]

    def __del__(self):
        """
        When the memory reference is removed, then close the instrument

        :return: None
        """
        self._dll.usb_tc08_close_unit(self._handle)


if __name__ == '__main__':
    tc = ThermocoupleReader([TcType.J])
    for i in range(10):
        print(time.clock(), tc.read_all())
