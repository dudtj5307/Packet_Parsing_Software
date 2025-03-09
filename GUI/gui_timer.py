import time
import threading


class GuiTimer:
    def __init__(self, parent):
        self.parent = parent
        self.timer_thread = None

    def start(self):
        if self.timer_thread:
            return False
        self.parent.edit_timer.setText("00 : 00 : 00")

        self.timer_thread = threading.Thread(target=self.update, daemon=True, args=(time.time(),))
        self.timer_thread.start()
        return True

    def update(self, start_time):
        while self.parent.parent.is_sniffing:
            duration = int(time.time() - start_time)
            if duration >= 0:
                hour = duration // 3600
                minutes = (duration % 3600) // 60
                seconds = duration % 60
                self.parent.edit_timer.setText(f"{hour:02} : {minutes:02} : {seconds:02}")
            time.sleep(0.2)

    def stop(self):
        self.timer_thread.join()
        self.timer_thread = None