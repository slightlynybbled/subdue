import tkinter as tk
from subdue import daqmx
import tk_tools


class DaqController(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent, padx=5, pady=5)

        self.daq = daqmx.NIDAQmx(device_name='Dev1')
        self.font = 'Ariel'

        self.title = tk.Label(self, text='DAQ Controller', font=(self.font, 14, 'bold'))
        self.title.pack(expand=True, fill=tk.X)

        self.ai_frame = AnalogInputFrame(self, self.daq)
        self.ai_frame.pack(expand=True, fill=tk.X)

        self.ao_frame = AnalogOutputFrame(self, self.daq)
        self.ao_frame.pack(expand=True, fill=tk.X)


class AnalogInputFrame(tk.LabelFrame):
    def __init__(self, parent, daq):
        self.parent = parent
        tk.LabelFrame.__init__(self, self.parent, text='Analog Input')

        self.daq = daq

        self.kve = tk_tools.KeyValueEntry(self, ['ai0', 'ai1', 'ai2', 'ai3'])
        self.kve.grid()

        self.retrieve_all()

    def retrieve_all(self):
        values = dict()
        for i in range(4):
            key = 'ai{}'.format(i)
            value = self.daq.sample_analog_in(key)[0]
            values[key] = value

        self.kve.load(values)
        self.parent.after(1000, self.retrieve_all)


class AnalogOutputFrame(tk.LabelFrame):
    def __init__(self, parent, daq):
        self.parent = parent
        tk.LabelFrame.__init__(self, self.parent, text='Analog Output')

        self.daq = daq

        self.kve = tk_tools.KeyValueEntry(self, ['ao0', 'ao1'], on_change_callback=self.on_change)
        self.kve.grid()

    def on_change(self):
        data = self.kve.get()
        try:
            ao0_voltage = float(data['ao0'])
        except ValueError:
            ao0_voltage = 0.0

        try:
            ao1_voltage = float(data['ao1'])
        except ValueError:
            ao1_voltage = 0.0

        self.daq.analog_out('ao0', ao0_voltage)
        self.daq.analog_out('ao1', ao1_voltage)


if __name__ == '__main__':
    root = tk.Tk()

    dc = DaqController(root)
    dc.grid()

    root.mainloop()
