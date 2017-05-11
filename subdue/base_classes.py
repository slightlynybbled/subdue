

class HardwareSearch:

    def list_devices(self):
        """
        This function should return a list of suitable references with which the device can 
        be initialized.  For instance, Visa Instruments may require model numbers while DAQmx
        devices may require OS references such as 'Dev1'.
        
        :return: list containing all detected hardware of this class
        """
        raise NotImplementedError
