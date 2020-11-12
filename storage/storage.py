from typing import List
import time
import heapq
from contextlib import suppress
from storage.settings import storage_settings


class LogEntry:

    def __init__(self, data):
        self.timestamp = float(data['timestamp'])
        self.type = data.get('type')
        self.status = data.get('status')
        self.connection = data.get('connection')

    def __gt__(self, other):
        return self.timestamp > other.timestamp


class Storage:

    log_collection: List[dict] = []

    def __new__(cls, *args, **kwargs) -> "Storage":
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def _is_too_old(self, log_entry: dict):
        return (
           time.time() - float(log_entry['timestamp'])
       ) > storage_settings.LOG_TTL

    def _clean_collection(self):
        with suppress(IndexError):
            while self._is_too_old(self.log_collection[0]):
                heapq.heappop(self.log_collection)

    def save(self, data):
        if self._is_too_old(data):
            return
        self._clean_collection()
        heapq.heappush(
            self.log_collection,
            data
        )

    def load(self):
        return self.log_collection[:]
