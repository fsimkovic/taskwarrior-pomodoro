__author__ = 'Felix Simkovic'
__date__ = '2019-05-18'
__license__ = 'MIT License'

import heapq
import io
import json
import os
import subprocess
import typing


class Task(typing.NamedTuple):
    description: str
    project: str
    uuid: str
    urgency: float

    def __lt__(self, other):
        # Note: not strictly less than but sufficient to create Max-Heap
        return (-1 * self.urgency) < (-1 * other.urgency)

    def __hash__(self):
        return hash(self.uuid)

    def __eq__(self, other):
        return self.uuid == other.uuid


class TaskWarrior:
    def __init__(self):
        self.tasks = []
        self._is_running = False

    @property
    def is_running(self):
        return self._is_running

    def refresh(self):
        cmd = [
            'task',
            'rc:{}'.format(os.path.expanduser('~/.taskrc')),
            'rc.confirmation=no',
            'rc.dependency.confirmation=no',
            'rc.recurrence.confirmation=no',
            'rc.json.array=off',
            'rc.bulk=0',
            'export',
            '+UNBLOCKED',
            'status:pending'
        ]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=1, universal_newlines=True)

        self.tasks = []
        for line in proc.stdout:
            data = json.loads(line)
            heapq.heappush(self.tasks, Task(**{k: (data[k] if k in data else '') for k in Task._fields}))

    def complete_task(self, task):
        subprocess.call(['task', task.uuid, 'done'])
        self._is_running = False

    def start_task(self, task):
        subprocess.call(['task', task.uuid, 'start'])
        self._is_running = True

    def stop_task(self, task):
        subprocess.call(['task', task.uuid, 'stop'])
        self._is_running = False
