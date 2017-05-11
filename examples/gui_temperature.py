import subdue
import tkinter as tk


class BaseFrame(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.title_label = tk.Label(self, text='Temperature')
        self.title_label.grid(row=0, column=0, columnspan=3)

        self.tc_reader = subdue.ThermocoupleReader()

        self.tc_channel = 1
        self.tc_reader.enable_channel(self.tc_channel, 'K')

        self.tc_label = tk.Label(self, text='TC {}'.format(self.tc_channel))
        self.tc_value = tk.Label(self, text=''.format(self.tc_channel))
        self.tc_unit = tk.Label(self, text='\u2103')

        self.tc_label.grid(row=1, column=0)
        self.tc_value.grid(row=1, column=1)
        self.tc_unit.grid(row=1, column=2)

        self.update()

    def update(self):
        self.display_values()
        self.parent.after(1000, self.update)

    def display_values(self):
        self.tc_value['text'] = self.tc_reader.read_one(self.tc_channel)


if __name__ == '__main__':
    root = tk.Tk()

    base_frame = BaseFrame(root)
    base_frame.grid()

    root.mainloop()
