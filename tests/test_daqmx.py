"""
Run these tests with *only* USB-6001 attached.  No other NI DAQmx
devices should be attached to the PC at the time of test.

Connect ao0 to ai0+ and GND to ai0-
Connect port0, line0 to ai1
Connect port0, line1 to port0, line2

"""
import pytest
import time

import subdue.daqmx as daqmx

analog_tolerance = 0.20    # this is the analog tolerance for the test


@pytest.fixture
def device():
    s = daqmx.NIDAQmxSearch()
    devices = s.list_devices()
    yield devices[0]


@pytest.fixture
def search():
    yield daqmx.NIDAQmxSearch()


@pytest.fixture
def daq():
    s = daqmx.NIDAQmxSearch()
    device = s.list_devices()[0]

    yield daqmx.NIDAQmx(device)


def test_search_attached_devices(device):
    assert isinstance(device, str)


def test_search_digital_lines(search, device):
    test_str = '{}/port0/line0'.format(device)

    assert test_str in search.list_do_lines(device)


def test_ao_1volt(daq):
    voltage_setting = 1.0

    daq.analog_out('ao0', voltage_setting)
    time.sleep(0.1)

    samples = daq.sample_analog_in('ai0', sample_count=10)
    total = sum(samples)
    avg = total/len(samples)

    assert avg > (voltage_setting - analog_tolerance)
    assert avg < (voltage_setting + analog_tolerance)


def test_ao_3volt(daq):
    voltage_setting = 3.0

    daq.analog_out('ao0', voltage_setting)
    time.sleep(0.1)

    samples = daq.sample_analog_in('ai0', sample_count=10)
    total = sum(samples)
    avg = total/len(samples)

    assert avg > (voltage_setting - analog_tolerance)
    assert avg < (voltage_setting + analog_tolerance)


def test_do_low(daq):
    daq.digital_out_line('port0', 'line0', False)
    time.sleep(0.1)

    sample = daq.digital_in_line('port0', 'line0')

    assert sample is False


def test_do_high(daq):
    daq.digital_out_line('port0', 'line1', True)
    time.sleep(0.1)

    sample = daq.digital_in_line('port0', 'line2')

    assert sample is True


def test_by_serial_number():
    daq = daqmx.NIDAQmx(serial_number='1b5d935')
    daq.analog_out('ao0', 1.5)  # try to do something with it

    assert daq.device == 'Dev1'
