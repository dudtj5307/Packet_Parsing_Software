import os, sys
import tkinter as tk
from tkinter import ttk, Frame, messagebox

def create_widgets(self):
    # Window Size
    self.root.geometry("1200x600")
    self.root.resizable(False, False)
    # Icon directory
    icon_path = os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else os.getcwd(), 'GUI', 'PPS.ico')
    self.root.iconbitmap(icon_path)
    '''https://www.flaticon.com/kr/free-icons/ /"파싱 아이콘" > 파싱 아이콘 / zero_wing - Flaticon '''
