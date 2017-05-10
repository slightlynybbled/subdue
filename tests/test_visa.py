"""
Run these tests with a power supply attached, but no load.

Be sure to specify that the power supply model that is attached
is specified in the 'test_model_number' string variable.
"""

import time

import subdue.hardware.hw_visa as visa

test_model_number = 'N5768A'
voltage_tolerance = 0.1


def test_psu_default_state():
    psu = visa.PowerSupply(model_number=test_model_number)

    status = psu.read_status()

    assert status == () or status == ('UNREGULATED', )


def test_psu_voltage_out():
    psu = visa.PowerSupply(model_number=test_model_number)

    desired_voltage = 5.0
    desired_current = 1.0

    psu.set_voltage(desired_voltage)
    psu.set_current(desired_current)
    psu.on()
    time.sleep(0.2)

    status = psu.read_status()
    voltage = psu.read_voltage()

    assert status == () or status == ('UNREGULATED', )
    assert voltage < (desired_voltage + voltage_tolerance)
    assert voltage > (desired_voltage - voltage_tolerance)


def test_psu_status():
    psu = visa.PowerSupply(model_number=test_model_number)

    psu.off()
    psu.ocp()
    time.sleep(0.2)

    status = psu.read_status()

    assert status == () or status == ('UNREGULATED',)

