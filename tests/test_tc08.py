"""
Run these tests with *only* TC-08 attached.

"""

import pytest
import subdue.thermocouple as tc08


@pytest.fixture
def reader():
    yield tc08.Tc08Usb()


def test_allocate_reader(reader):
    assert reader

