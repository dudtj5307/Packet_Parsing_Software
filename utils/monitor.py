
# Singleton progress monitoring class
class ProgressMonitor:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, backend=None):
        if backend:
            self._backend = backend
            self._progress = {'idl': 0, 'parse': 0, 'csv': 0}   # (int: range 0~100)
            self._status   = {'work_idx': 0, 'work_num': float('inf'), 'task_idx': 0, 'task_num': float('inf')}

    # Updates Progress to GUI
    def update(self, key, work_idx=None, work_num=None, task_idx=None, task_num=None, only_work=False):
        # Update Working Status
        self._status['work_idx'] = work_idx or self._status['work_idx']
        self._status['work_num'] = work_num or self._status['work_num']
        self._status['task_idx'] = task_idx or self._status['task_idx']
        self._status['task_num'] = task_num or self._status['task_num']
        # Save old value & Calculate new value from working status
        old_value = self._progress[key]
        if only_work: new_value =  (self._status['work_idx'] + 1) / self._status['work_num'] * 100
        else: new_value =  (self._status['work_idx'] / self._status['work_num']
                         + (1 / self._status['work_num']) * (self._status['task_idx'] + 1) / self._status['task_num']) * 100
        if new_value - old_value >= 2 or new_value == 100:
            self._progress[key] = min(int(new_value + 0.5), 100)
            self._backend.progress_update.emit(
                [self._progress['idl'], self._progress['parse'], self._progress['csv']])

    # Check if backend is stopped
    def backend_stopped(self):
        return self._backend.stopped