

class HardwareSearch:

    def list_devices(self):
        """
        Returns all available data regarding attached hardware
        :return: list of dicts containing data
        """
        raise NotImplementedError

    def list_references(self):
        """
        This function should return a list of suitable references with which the device can 
        be initialized.  For instance, Visa Instruments may require model numbers while DAQmx
        devices may require OS references such as 'Dev1'.
        
        :return: list containing all detected hardware references of this class
        """
        raise NotImplementedError

    def list_models(self):
        """
        For hardware which can be polled for the model number, list the model numbers

        :return: list containing all detected model numbers of this class
        """
        raise NotImplementedError

    def list_serial_numbers(self):
        """
        For hardware which can be polled for the serial number, list the model numbers

        :return: list containing all detected serial numbers of this class
        """
        raise NotImplementedError


