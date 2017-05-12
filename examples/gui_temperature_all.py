import subdue
import tkinter as tk


class BaseFrame(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.title_label = tk.Label(self, text='Temperature')
        self.title_label.grid(row=0, column=0, columnspan=3)

        self.tc_labels = []
        self.tc_value_labels = []
        self.tc_unit_labels = []

        self.tc_reader = subdue.ThermocoupleReader()

        for i in range(len(self.tc_reader.available_channels())):
            self.tc_reader.enable_channel(i, 'K')

            label = tk.Label(self, text='TC {}'.format(i))
            value = tk.Label(self, text='')
            unit = tk.Label(self, text='\u2103')

            label.grid(row=1+i, column=0)
            value.grid(row=1+i, column=1)
            unit.grid(row=1+i, column=2)

            self.tc_labels.append(label)
            self.tc_value_labels.append(value)
            self.tc_unit_labels.append(unit)

        self.update()

    def update(self):
        self.display_values()
        self.parent.after(1000, self.update)

    def display_values(self):
        values = self.tc_reader.read_all()

        for i in range(len(self.tc_reader.available_channels())):
            self.tc_value_labels[i]['text'] = values[i]


if __name__ == '__main__':
    root = tk.Tk()

    base_frame = BaseFrame(root)
    base_frame.grid()

    root.mainloop()
