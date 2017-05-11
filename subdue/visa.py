import pyvisa
import collections
import eventlet
import time
import re

from subdue import HardwareSearch

InstrumentId = collections.namedtuple('InstrumentId',
                                      'Manufacturer,ModelNumber,SerialNumber')


def list_connected():
    """
    List all connected VISA instruments

    :return: a list of connected instruments
    """
    rm = pyvisa.ResourceManager()
    resource_list = rm.list_resources()

    instrument_list = []
    for resource in resource_list:
        try:
            inst = rm.open_resource(resource)
            inst.timeout = 200
            id_str = inst.query('*IDN?').strip()

            fields = id_str.split(',')
            fields = [ident.strip() for ident in fields]
            entry = InstrumentId(fields[0], fields[1], fields[2])
            instrument_list.append(entry._asdict())

        except Exception as e:
            pass

    return instrument_list


class VisaInstrumentSearch(HardwareSearch):
    """
    Used to search all instruments that are connected to the PC
    """

    def __init__(self):
        pass

    def list_devices(self):
        data = list()

        for instrument in list_connected():
            device_data = {
                'reference': instrument.get('ModelNumber'),
                'model': instrument.get('ModelNumber'),
                'serial': instrument.get('SerialNumber')
            }

            data.append(device_data)

        return data

    def list_references(self):
        return [instrument['SerialNumber'] for instrument in list_connected()]

    def list_models(self):
        return [instrument['ModelNumber'] for instrument in list_connected()]

    def list_serial_numbers(self):
        return [instrument['SerialNumber'] for instrument in list_connected()]


class VisaInstrument:
    """
    A class designed to create a common grouping for all VISA instruments
    """

    command_timeout = 1

    def __init__(self, serial_number=None, model_number=None, instrument=None):
        """
        If the instrument is supplied, then this will save the instrument into the
        object for utilization.

        If the model number is supplied, then this will read all instruments available
        and will assign the first instrument with a matching model number.

        :param instrument: an instance of the instrument as returned from pyvisa.ResourceManager.open_resource()
        :param model_number: if the model number is supplied, then the visa instrument would attempt to take
        the resource with the matching model number
        """
        self.instrument = instrument
        self.model_number = model_number
        self.serial_number = serial_number

        self.rm = pyvisa.ResourceManager()
        resource_list = self.rm.list_resources()

        # if the instrument is supplied, then return
        if self.instrument:
            return

        # if the model number is found
        for resource in resource_list:
            try:
                inst = self.rm.open_resource(resource)
                id_str = inst.query('*IDN?').strip()
                ident = id_str.split(',')
                ident = [e.strip() for e in ident]
                entry = InstrumentId(ident[0], ident[1], ident[2])

                if serial_number in ident:
                    self.instrument = inst
                    self.serial_number = entry.SerialNumber
                    self.model_number = entry.ModelNumber
                    break
                elif model_number in ident:
                    self.instrument = inst
                    self.serial_number = entry.SerialNumber
                    self.model_number = entry.ModelNumber
                    break

            except pyvisa.errors.VisaIOError as e:
                pass

    def __repr__(self):
        return 'VisaInstrument {} {} {}'.format(self.instrument, self.model_number, self.serial_number)

    def __exit__(self):
        """
        Releases the hardware
        :return:
        """
        if self.instrument:
            self.instrument.close()

    def get_id(self):
        """
        Returns the identity of the instrument, as supplied by the instrument
        :return: a tuple containing the identity
        """
        if not self.instrument:
            return None

        identity = None
        try:
            id_str = self.instrument.query('*IDN?')
            identity = id_str.split(',')
            identity = [e.strip() for e in identity]
            identity = tuple(identity)

        except pyvisa.errors.VisaIOError as e:
            pass

        return identity


class PowerSupply(VisaInstrument):
    """
    A class intended for power supplies that conform to VISA/SCPI standards.
    """

    def __init__(self, serial_number=None, model_number=None, instrument=None):
        """
        Initializes the class

        :param instrument: an instance of the instrument as returned from pyvisa.ResourceManager.open_resource()
        :param model_number: if the model number is supplied, then the visa instrument would attempt to take
        the resource with the matching model number
        """
        self.vi = super().__init__(serial_number=serial_number, model_number=model_number, instrument=instrument)

    def read_voltage(self):
        """
        Reads the output PSU voltage

        :return: the output PSU voltage or 'None' if unsuccessful
        """
        if not self.instrument:
            return None

        start_time = time.clock()
        success = False

        while not success:
            voltage = None
            try:
                if self.model_number == 'CPX400SP':
                    voltage_str = self.instrument.query('V1O?').strip()
                    voltage_str = re.findall(r'\d+\.*\d*', voltage_str)[0]
                else:
                    voltage_str = self.instrument.query(':MEASure:VOLTage?').strip()

                voltage = float(voltage_str)
                success = True
            except pyvisa.errors.VisaIOError as e:
                print('ERROR: ', e)
                if (time.clock() - start_time) > self.command_timeout:
                    break

                eventlet.sleep(0.01)

        return voltage

    def read_current(self):
        """
        Reads the output PSU current

        :return: the output PSU current or 'None' if unsuccessful
        """
        if not self.instrument:
            return None

        start_time = time.clock()
        success = False

        while not success:
            current = None
            try:
                if self.model_number == 'CPX400SP':
                    current_str = self.instrument.query('I1O?').strip()
                    current_str = re.findall(r'\d+\.*\d*', current_str)[0]
                else:
                    current_str = self.instrument.query(':MEASure:CURRent?').strip()

                current = float(current_str)
                success = True
            except pyvisa.errors.VisaIOError as e:
                if (time.clock() - start_time) > self.command_timeout:
                    break

                eventlet.sleep(0.01)

        return current

    def read_status(self):
        """
        Reads the PSU status

        :return: a list containing strings that represent the PSU status or 'False' if unsuccessful
        """
        if not self.instrument:
            return False

        start_time = time.clock()
        success = False

        while not success:
            status = []
            if self.model_number == 'CPX400SP':
                q = 'LSR1?'
                status_str = self.instrument.query(q).strip()
                status_num = int(status_str)

                print('status: {}'.format(status_str))

                if status_num >= 128:
                    status_num -= 128

                if status_num >= 64:
                    status.append('RESET_FRONT_PANEL')
                    status_num -= 64

                if status_num >= 32:
                    status_num -= 32

                if status_num >= 16:
                    status.append('UNREGULATED')
                    status_num -= 16

                if status_num >= 8:
                    status.append('OVERCURRENT')
                    status_num -= 8

                if status_num >= 4:
                    status.append('OVERVOLTAGE')
                    status_num -= 4

                if status_num >= 2:
                    #status.append('MODE: CURRENT_LIMIT')
                    status_num -= 2

                if status_num >= 1:
                    #status.append('MODE: VOLTAGE_LIMIT')
                    status_num -= 1

                return tuple(status)
            else:
                try:
                    q = ':STATus:QUEStionable?'
                    status_str = self.instrument.query(q).strip()
                    status_num = int(status_str)

                    # determine which events have occurred
                    if status_num >= 1024:
                        status.append('UNREGULATED')
                        status_num -= 1024

                    if status_num >= 512:
                        status.append('INHIBITED')
                        status_num -= 512

                    if status_num >= 16:
                        status.append('OVERTEMP')
                        status_num -= 16

                    if status_num >= 4:
                        status.append('PWR_FAIL')
                        status_num -= 4

                    if status_num >= 2:
                        status.append('OVERCURRENT')
                        status_num -= 2

                    if status_num >= 1:
                        status.append('OVERVOLTAGE')
                        status_num -= 1

                    success = True
                    return tuple(status)

                except pyvisa.errors.VisaIOError as e:
                    if (time.clock() - start_time) > self.command_timeout:
                        return tuple()

                    eventlet.sleep(0.01)

    def reset(self):
        """
        Resets the PSU

        :return: True if successful, else False
        """
        if not self.instrument:
            return False

        start_time = time.clock()
        success = False

        while not success:
            try:
                q = '*RST'
                self.instrument.write(q)
                success = True

            except pyvisa.errors.VisaIOError as e:
                if (time.clock() - start_time) > self.command_timeout:
                    break

                eventlet.sleep(0.01)

        return success

    def set_voltage(self, voltage=0.0):
        """
        Sets the output voltage of the PSU, but doesn't turn on the output

        :param voltage: the voltage, in volts
        :return: True if successful, else False
        """
        if not self.instrument:
            return False

        start_time = time.clock()
        success = False

        while not success:
            try:
                if self.model_number == 'CPX400SP':
                    q = 'V1 {}'.format(voltage)
                else:
                    q = ':SOURce:VOLTage {}'.format(voltage)

                self.instrument.write(q)
                success = True

            except pyvisa.errors.VisaIOError as e:
                if (time.clock() - start_time) > self.command_timeout:
                    break

                eventlet.sleep(0.01)

        return success

    def set_current(self, current=0.0):
        """
        Sets the output current of the PSU, but doesn't turn on the output

        :param current: the current, in Amps
        :return: True if successful, else False
        """
        if not self.instrument:
            return False

        start_time = time.clock()
        success = False

        while not success:
            try:
                if self.model_number == 'CPX400SP':
                    q = 'I1 {}'.format(current)
                else:
                    q = ':SOURce:CURRent {}'.format(current)

                self.instrument.write(q)
                success = True

            except pyvisa.errors.VisaIOError as e:
                if (time.clock() - start_time) > self.command_timeout:
                    break

                eventlet.sleep(0.01)

        return success

    def on(self):
        """
        Turns on the output

        :return: True if successful, else False
        """
        if not self.instrument:
            return False

        start_time = time.clock()
        success = False

        while not success:
            try:
                if self.model_number == 'CPX400SP':
                    q = 'OP1 1'
                else:
                    q = ':OUTPut:STATe ON'

                self.instrument.write(q)
                success = True

            except pyvisa.errors.VisaIOError as e:
                if (time.clock() - start_time) > self.command_timeout:
                    break

                eventlet.sleep(0.01)

        return success

    def off(self):
        """
        Turns off the output

        :return: True if successful, else False
        """
        if not self.instrument:
            return False

        start_time = time.clock()
        success = False

        while not success:
            try:
                if self.model_number == 'CPX400SP':
                    q = 'OP1 0'
                else:
                    q = ':OUTPut:STATe OFF'

                self.instrument.write(q)
                success = True

            except pyvisa.errors.VisaIOError as e:
                if (time.clock() - start_time) > self.command_timeout:
                    break

                eventlet.sleep(0.01)

        return success

    def ocp(self, state=True):
        """
        Sets or clears the overcurrent protection

        :param state: True for OCP on, else False
        :return: True if successful, else False
        """
        if not self.instrument:
            return False

        start_time = time.clock()
        success = False

        while not success:

            try:
                if self.model_number == 'CPX400SP':
                    # read the current, then set the OCP based on that
                    q = 'I1?'
                    current_setting = self.instrument.query(q).strip()
                    current_setting = re.findall(r'\d+\.*\d*', current_setting)[0]

                    q = 'OCP1 {}'.format(current_setting)

                else:
                    if state:
                        q = ':CURRent:PROTection:STATe ON'
                    else:
                        q = ':CURRent:PROTection:STATe OFF'

                self.instrument.write(q)
                success = True

            except pyvisa.errors.VisaIOError as e:
                if (time.clock() - start_time) > self.command_timeout:
                    break

                eventlet.sleep(0.01)

        return success


def main():
    psu = PowerSupply(serial_number='US08E6445J')
    #print('starting status: ', psu.read_status())
    print(psu.get_id())

    print(psu.read_voltage())
    print(psu.read_current())
    print(psu.read_status())

    psu.on()
    psu.set_voltage(1)
    psu.set_current(1)
    psu.ocp(True)

    eventlet.sleep(2)

    psu.off()
    psu.ocp()

    #print(psu.read_status())
    #print('errors: ', psu.get_errors())

    #print(list_connected())


if __name__ == '__main__':
    main()
