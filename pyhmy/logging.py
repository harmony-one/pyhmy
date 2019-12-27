import os
import threading
import datetime
import logging


class ControlledLogger:
    """
    A simple logger that only writes to file when the 'write' method is called.
    """

    def __init__(self, logger_name, log_dir):
        """
        :param logger_name: The name of the logger and logfile
        :param log_dir: The directory in which to save this log file (can be abs or relative).
        """
        if log_dir.endswith('/'):
            log_dir = log_dir[:-1]
        os.makedirs(log_dir, exist_ok=True)
        handler = logging.FileHandler(f"{log_dir}/{logger_name}.log")
        handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(handler)
        self._clear()

    def _clear(self):
        """
        Internal method to clear the log buffer.

        Note that log buffers are lists to be thread safe.
        """
        self.info_buffer = []
        self.debug_buffer = []
        self.warning_buffer = []
        self.error_buffer = []

    def info(self, msg):
        """
        :param msg: The info message to log
        """
        self.info_buffer.append(f"[{threading.get_ident()}] "
                                f"{datetime.datetime.utcnow()} : {msg}")

    def debug(self, msg):
        """
        :param msg: The debug message to log
        """
        self.debug_buffer.append(f"[{threading.get_ident()}] "
                                 f"{datetime.datetime.utcnow()} : {msg}")

    def warning(self, msg):
        """
        :param msg: The warning message to log
        """
        self.warning_buffer.append(f"[{threading.get_ident()}] "
                                   f"{datetime.datetime.utcnow()} : {msg}")

    def error(self, msg):
        """
        :param msg: The error message to log
        """
        self.error_buffer.append(f"[{threading.get_ident()}] "
                                 f"{datetime.datetime.utcnow()} : {msg}")

    def print_info(self):
        """
        Prints the current info buffer but does not flush it to log file.
        """
        print('\n'.join(self.info_buffer))

    def print_debug(self):
        """
        Prints the current debug buffer but does not flush it to log file.
        """
        print('\n'.join(self.debug_buffer))

    def print_warning(self):
        """
        Prints the current warning buffer but does not flush it to log file.
        """
        print('\n'.join(self.warning_buffer))

    def print_error(self):
        """
        Prints the current error buffer but does not flush it to log file.
        """
        print('\n'.join(self.error_buffer))

    def write(self):
        """
        Flushes ALL of the log buffers to the log file via the logger.

        Note that directly after this method call, the respective prints will print
        nothing since all log messages are flushed to file.
        """
        if self.info_buffer:
            self.logger.setLevel(logging.INFO)
            self.logger.info('\n'.join(self.info_buffer))
        if self.debug_buffer:
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug('\n'.join(self.debug_buffer))
        if self.warning_buffer:
            self.logger.setLevel(logging.WARNING)
            self.logger.warning('\n'.join(self.warning_buffer))
        if self.error_buffer:
            self.logger.setLevel(logging.ERROR)
            self.logger.error('\n'.join(self.error_buffer))
        self._clear()
