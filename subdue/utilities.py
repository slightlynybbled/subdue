from pkg_resources import get_distribution

import subdue

daqs = []
thermocouples = []
power_supplies = []


def parse_daq_command(device_name, command):
    global daqs

    # make a list of current device names
    current_devices = [daq.device for daq in daqs]
    if device_name not in current_devices:
        daq = subdue.NIDAQmx(device_name)
        daqs.append(daq)
    else:
        index = current_devices.index(device_name)
        daq = daqs[index]

    if command['operation'] == 'do':
        value = True if command['value'] in [1, '1', True, 'high', 'hi'] else False
        daq.digital_out_line(
            port_name=command['port'],
            line_name=command['line'],
            value=value)
        return {}
    elif command['operation'] == 'di':
        value = daq.digital_in_line(command['port'], command['line'])
        return {
            'operation': 'di',
            'port': command['port'],
            'line': command['line'],
            'value': value}
    elif command['operation'] == 'ao':
        daq.analog_out(analog_output=command['ao'], voltage=command['value'])
        return {}
    elif command['operation'] == 'ai':
        specs = dict()
        specs['analog_input'] = command['ai']

        try:
            specs['sample_count'] = int(command['samples'])
        except KeyError:
            pass

        try:
            specs['rate'] = float(command['sample rate'])
        except KeyError:
            pass

        specs['output_format'] = 'list'

        value = daq.sample_analog_in(**specs)
        if len(value) == 1:
            value = value[0]

        return {'operation': 'ai', 'ai': command['ai'], 'value': value}


def parse_thermocouple_command(device_name, commands):
    global thermocouples

    # make a list of current device names
    current_devices = [tc.model for tc in thermocouples]
    if device_name not in current_devices:
        channel = commands[0]['channel'] if isinstance(commands, list) else commands['channel']
        tc = subdue.ThermocoupleReader(types=channel)
        thermocouples.append(tc)
    else:
        index = current_devices.index(device_name)
        tc = thermocouples[index]

    if isinstance(commands, list):
        for command in commands:
            tc_type = command['type'] if 'type' in command.keys() else 'J'
            tc.enable_channel(command['channel'], tc_type)
    else:
        command = commands
        tc_type = command['type'] if 'type' in command.keys() else 'J'
        tc.enable_channel(command['channel'], tc_type)

    raw_values = tc.read_all(output_format='float')

    if len(raw_values) > 1:
        values = []
        for channel, temperature in raw_values.items():
            values.append({'channel': channel, 'value': temperature, 'unit': 'Celsius'})

        return values

    else:
        channel = list(raw_values.keys())[0]
        return {'channel': channel, 'value': raw_values[channel], 'unit': 'Celsius'}


def parse_visa_command(command, serial_number=None):
    global power_supplies

    serial_numbers = [psu.serial_number for psu in power_supplies]

    # retrieve a previously-utilized power supply or allocate a new one
    psu = None
    if serial_number in serial_numbers:
        # get a reference to the serial number here
        for power_supply in power_supplies:
            if power_supply.serial_number == serial_number:
                psu = power_supply

    else:
        searcher = subdue.VisaInstrumentSearch()
        connected = searcher.list_serial_numbers()

        for psu_sn in connected:
            if psu_sn == serial_number:
                print('power supply found!')
                psu = subdue.PowerSupply(serial_number=serial_number)
                power_supplies.append(psu)
                break

    if not psu:
        return {'error': 'psu not found'}

    if command['operation'] == 'write':
        # parse the write command into the appropriate visa request
        if command['parameter'] == 'voltage':
            print('attempting to set voltage...')
            v = command['value']
            psu.set_voltage(float(v))
            print('voltage is set to ', v)
        elif command['parameter'] == 'current':
            c = command['value']
            psu.set_current(float(c))
        elif command['parameter'] == 'ocp':
            psu.ocp(command['value'])
        elif command['parameter'] == 'output':
            if command['value'] is True:
                psu.on()
            else:
                psu.off()
        else:
            return {'error': 'parameter not recognized'}

        return {}

    elif command['operation'] == 'read':
        # parse the read command into the appropriate visa request
        if command['parameter'] == 'voltage':
            command['value'] = psu.read_voltage()
            return command
        elif command['parameter'] == 'current':
            command['value'] = psu.read_current()
            return command
        elif command['parameter'] == 'status':
            command['value'] = psu.read_status()
            return command

        return {'error': 'parameter not recognized'}

    elif command['operation'] == 'reset':
        psu.reset()
        return {}

    else:
        return {'error': 'operation not recognized'}


def get_package_version():
    return get_distribution('subdue').version
