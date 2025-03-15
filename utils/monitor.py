
""" Singleton progress monitoring class

    - work1         - work2         - work3
      - task1         - task1         - task1
      - task2         - task2         - task2
      - task3         - task3         - task3

"""
from scapy.layers.kerberos import krb_as_and_tgs


class ProgressMonitor:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance._progress = {'idl': 0, 'parse': 0, 'csv': 0}
        return cls.__instance

    def __init__(self, backend=None):
        if backend:
            self._backend = backend
            self._progress = {'idl': 0, 'parse': 0, 'csv': 0}   # (int: range 0~100)

        self._status = {'idl'  : {'work_idx': 0, 'work_num': float('inf'), 'task_idx': 0, 'task_num': float('inf')},
                        'parse': {'work_idx': 0, 'work_num': float('inf'), 'task_idx': 0, 'task_num': float('inf')},
                        'csv'  : {'work_idx': 0, 'work_num': float('inf'), 'task_idx': 0, 'task_num': float('inf')}}

    # Updates Progress
    def update(self, key, **kwargs):
        return self.update_and_check_stop(key, **kwargs)

    # Updates Progress to GUI and Check if backend stopped
    def update_and_check_stop(self, key, work_idx=None, work_total=None, task_idx=None, task_total=None, prior_status=0):
        # Update Working Status
        status = self._status[key]
        updates = {'work_idx': work_idx, 'work_num': work_total, 'task_idx': task_idx, 'task_num': task_total}
        for k, val in updates.items():
            if val is not None:
                status[k] = val

        # Save old value & Calculate new value from working status
        work_progress = status['work_idx']/status['work_num']
        task_progress = min(1, ((status['task_idx']+1) / status['task_num'])*(1-prior_status) + prior_status)   # TODO: check if ration is correct

        old_value = self._progress[key]
        new_value = (work_progress + (1/status['work_num']) * task_progress) * 100

        print(new_value)

        # Update if interval bigger than 2%
        if new_value - old_value >= 2 or new_value == 100:
            self._progress[key] = min(int(new_value + 0.5), 100)
            self._backend.progress_update.emit([self._progress['idl'], self._progress['parse'], self._progress['csv']])

        # Returns flag if GUI stopped backend
        return self._backend.stopped
