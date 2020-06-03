#!/usr/bin/python3.8
import time

from rich.console import Console
from rich.table import Table

DISABLE_LOGGER_OUTPUT=False


class Logger:
    _singleton = None

    def __init__(self):
        if Logger._singleton is None:
            Logger. _singleton = self
            self.console = Console()
            self.logs = []

    @staticmethod
    def getInstance():
        return Logger._singleton

    @staticmethod
    def getTime():
        return time.strftime('%H:%M:%S')

    def info(self, string: str) -> None:
        log = self._log('INFO', string)
        self.print("[yellow bold](%s) - %s - %s" % log[:3])

    def debug(self, string: str) -> None:
        log = self._log('DEBUG', string)
        self.print("[cyan bold i](%s) - %s - %s" % log[:3])

    def log_table(self, table: Table, title="Tableau"):
        log = self._log('INFO', table, title)
        self.print("[yellow bold](%s) - %s - %s :" % log[:3])
        self.print(table)

    def force(self, string: str):
        log = self._log('FORCED', string)
        self.print("[purple bold i](%s) - %s - %s" % log[:3], True)

    def _log(self, type: str, val, title=None):
        if title is None:
            title = val
        t = time.strftime('%H:%M:%S')
        log = (type, t, title, val)
        self.logs.append(log)
        return log

    def print(self, value, force=False):
        if 'DISABLE_LOGGER_OUTPUT' not in globals() or not DISABLE_LOGGER_OUTPUT or force:
            self.console.print(value)


