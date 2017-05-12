import subdue
import tkinter as tk
import tkinter.ttk as ttk


class BaseFrame(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        # create and initialize the variables required to operate the PSU
        self.psu = subdue.PowerSupply(model_number='N5768A')
        self.psu.reset()

        self.on_off_var = tk.BooleanVar()
        self.on_off_var.set(False)

        self.ocp_var = tk.BooleanVar()
        self.ocp_var.set(True)

        self.title_label = tk.Label(self, text='Power Supply')
        self.title_label.grid(row=0, column=0, columnspan=3)

        # create the widgets
        self.voltage_label = tk.Label(self, text='Voltage')
        self.voltage_entry = tk.Entry(self, text='')
        self.voltage_unit_label = tk.Label(self, text='V')

        self.current_label = tk.Label(self, text='Current')
        self.current_entry = tk.Entry(self, text='')
        self.current_unit_label = tk.Label(self, text='A')

        self.on_off_label = tk.Label(self, text='Output Control')
        self.on_off_cb = ttk.Checkbutton(self, variable=self.on_off_var)

        self.ocp_label = tk.Label(self, text='Overcurrent Protection')
        self.ocp_cb = ttk.Checkbutton(self, variable=self.ocp_var)

        # grid each widget on the gui
        self.voltage_label.grid(row=1, column=0)
        self.voltage_entry.grid(row=1, column=1)
        self.voltage_unit_label.grid(row=1, column=2)

        self.current_label.grid(row=2, column=0)
        self.current_entry.grid(row=2, column=1)
        self.current_unit_label.grid(row=2, column=2)

        self.on_off_label.grid(row=3, column=0)
        self.on_off_cb.grid(row=3, column=1)

        self.ocp_label.grid(row=4, column=0)
        self.ocp_cb.grid(row=4, column=1)

        # create key bindings
        self.voltage_entry.bind('<FocusOut>', self.set_voltage)
        self.current_entry.bind('<FocusOut>', self.set_current)

        # create variable traces
        self.on_off_var.trace('w', self.on_off)
        self.ocp_var.trace('w', self.ocp)

    def __del__(self):
        del self.psu

    def set_voltage(self, event):
        voltage = float(self.voltage_entry.get())
        voltage = round(voltage, 2)
        self.psu.set_voltage(voltage)

    def set_current(self, event):
        current = float(self.current_entry.get())
        current = round(current, 2)
        self.psu.set_current(current)

    def on_off(self, name, index, mode):
        if self.on_off_var.get():
            self.psu.on()
        else:
            self.psu.off()

    def ocp(self, name, index, mode):
        if self.ocp_var.get():
            self.psu.ocp(True)
        else:
            self.psu.ocp(False)

if __name__ == '__main__':
    root = tk.Tk()

    base_frame = BaseFrame(root)
    base_frame.grid()

    root.mainloop()
