import threading
import datetime
import gzip
import os
import logging
import logging.handlers


class _GZipRotator:
    def __call__(self, source, dest):
        os.rename(source, dest)
        f_in = open(dest, "rb")
        f_out = gzip.open("%s.gz" % dest, "wb")
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(dest)


class ControlledLogger:
    """
    A simple logger that only writes to file when the 'write' method is called.
    """

    def __init__(self, logger_name, log_dir, backup_count=5):
        """
        :param logger_name: The name of the logger and logfile
        :param log_dir: The directory in which to save this log file (can be abs or relative).
        """
        if log_dir.endswith("/"):
            log_dir = log_dir[:-1]
        log_dir = os.path.realpath(log_dir)
        os.makedirs(log_dir, exist_ok=True)
        handler = logging.handlers.TimedRotatingFileHandler(
            f"{log_dir}/{logger_name}.log", "midnight", 1, backupCount=backup_count
        )
        handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        handler.rotator = _GZipRotator()

        self.filename = handler.baseFilename
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(handler)
        self._lock = threading.Lock()
        self.filepath = f"{log_dir}/{logger_name}.log"
        self.info_buffer = []
        self.debug_buffer = []
        self.warning_buffer = []
        self.error_buffer = []

    def __repr__(self):
        return f"<ControlledLogger @ {self.filepath} : {self.logger}>"

    def _clear(self):
        """
        Internal method to clear the log buffer.
        """
        self.info_buffer.clear()
        self.debug_buffer.clear()
        self.warning_buffer.clear()
        self.error_buffer.clear()

    def info(self, msg):
        """
        :param msg: The info message to log
        """
        self._lock.acquire()
        self.info_buffer.append(
            f"[{threading.get_ident()}] " f"{datetime.datetime.utcnow()} : {msg}"
        )
        self._lock.release()

    def debug(self, msg):
        """
        :param msg: The debug message to log
        """
        self._lock.acquire()
        self.debug_buffer.append(
            f"[{threading.get_ident()}] " f"{datetime.datetime.utcnow()} : {msg}"
        )
        self._lock.release()

    def warning(self, msg):
        """
        :param msg: The warning message to log
        """
        self._lock.acquire()
        self.warning_buffer.append(
            f"[{threading.get_ident()}] " f"{datetime.datetime.utcnow()} : {msg}"
        )
        self._lock.release()

    def error(self, msg):
        """
        :param msg: The error message to log
        """
        self._lock.acquire()
        self.error_buffer.append(
            f"[{threading.get_ident()}] " f"{datetime.datetime.utcnow()} : {msg}"
        )
        self._lock.release()

    def print_info(self):
        """
        Prints the current info buffer but does not flush it to log file.
        """
        print("\n".join(self.info_buffer))

    def print_debug(self):
        """
        Prints the current debug buffer but does not flush it to log file.
        """
        print("\n".join(self.debug_buffer))

    def print_warning(self):
        """
        Prints the current warning buffer but does not flush it to log file.
        """
        print("\n".join(self.warning_buffer))

    def print_error(self):
        """
        Prints the current error buffer but does not flush it to log file.
        """
        print("\n".join(self.error_buffer))

    def write(self):
        """
        Flushes ALL of the log buffers to the log file via the logger.

        Note that directly after this method call, the respective prints will print
        nothing since all log messages are flushed to file.
        """
        self._lock.acquire()
        self.logger.setLevel(logging.DEBUG)
        for line in self.debug_buffer:
            self.logger.debug(line)
        self.logger.setLevel(logging.WARNING)
        for line in self.warning_buffer:
            self.logger.warning(line)
        self.logger.setLevel(logging.ERROR)
        for line in self.error_buffer:
            self.logger.error(line)
        self.logger.setLevel(logging.INFO)
        for line in self.info_buffer:
            self.logger.info(line)
        self._clear()
        self._lock.release()
