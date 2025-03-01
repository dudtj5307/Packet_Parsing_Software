import tkinter as tk

from GUI import widget

VERSION = "v0.0"


class PacketParser:
    def __init__(self, root):
        self.root = root

        widget.create_widgets(self)



if __name__ == "__main__":
    root = tk.Tk()
    pss = PacketParser(root)

    root.title(f"Packet Parsing Software {VERSION}")


    root.mainloop()