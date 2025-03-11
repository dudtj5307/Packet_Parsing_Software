import time
from threading import Event


class A:
    def __init__(self):
        self.flag = False
        self.eFlag = Event()
        self.iter = 20000000

    def just_flag(self):
        start = time.time()
        for i in range(self.iter):
            if self.flag:
                break
            continue
        print(time.time() - start)

    def event_flag(self):
        start = time.time()
        for i in range(self.iter):
            if self.eFlag.is_set():
                break
            continue
        print(time.time() - start)

if __name__ == "__main__":
    a = A()
    a.just_flag()
    a.event_flag()





