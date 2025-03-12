import time
import threading

from PyQt6.QtCore import QObject, pyqtSignal

class ClockTime(QObject):
    set_clock_time = pyqtSignal(str, name="set_clock_time")
    def __init__(self, parent):
        super().__init__()
        # Parent Objects
        self.parent = parent  # parent            (gui_main.py)
        self.clock_thread = None

    def start(self):
        if self.clock_thread:
            return False
        self.set_clock_time.emit("00 : 00 : 00")
        self.clock_thread = threading.Thread(target=self.update, daemon=True, args=(time.time(),))
        self.clock_thread.start()
        return True

    def update(self, start_time):
        while self.parent.parent.is_sniffing:
            duration = int(time.time() - start_time)
            if duration >= 0:
                hour = duration // 3600
                minutes = (duration % 3600) // 60
                seconds = duration % 60
                self.set_clock_time.emit(f"{hour:02} : {minutes:02} : {seconds:02}")
            time.sleep(0.25)

    def stop(self):
        self.clock_thread.join()
        self.clock_thread = None