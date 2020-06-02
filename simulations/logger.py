#!/usr/bin/python3.8
import time

from rich.console import Console
from rich.table import Table


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
        self.console.print("[yellow bold](%s) - %s - %s" % log[:3])

    def log_table(self, table: Table, title="Tableau"):
        log = self._log('INFO', table, title)
        self.console.print("[yellow bold](%s) - %s - %s :" % log[:3])
        self.console.print(table)

    def _log(self, type: str, val, title=None):
        if title is None:
            title = val
        t = time.strftime('%H:%M:%S')
        log = (type, t, title, val)
        self.logs.append(log)
        return log

