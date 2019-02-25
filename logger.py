#!/usr/bin/env python3
"""
We may only have one instance of the class.
"""


class Logger(object):
    class _SingletonLogger:
        def __init__(self, file_name):
            self.file_name = file_name

        def __str__(self):
            return "{0!r} {1}".format(self, self.file_name)

        def _write_log(self, level, msg):
            """Writes a message to the file_name for a Logger instance"""
            with open(self.file_name, "a") as log_file:
                log_file.write("[{0}] {1}\n".format(level, msg))

        def critical(self, msg):
            self._write_log("CRITICAL", msg)

        def error(self, msg):
            self._write_log("ERROR", msg)

        def warn(self, msg):
            self._write_log("WARN", msg)

        def info(self, msg):
            self._write_log("INFO", msg)

        def debug(self, msg):
            self._write_log("DEBUG", msg)

    instance = None

    def __new__(cls, file_name):

        """Constructor is a class method, receives the class as parameter.
        If there is an existing instance, contructor will return it."""

        if not Logger.instance:
            Logger.instance = Logger._SingletonLogger(file_name)

        return Logger.instance
