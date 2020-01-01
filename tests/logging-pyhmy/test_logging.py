import os

import pytest

from pyhmy import logging


def test_basic_logger():
    if os.path.exists(f"{os.getcwd()}/logs/pytest.log"):
        os.remove(f"{os.getcwd()}/logs/pytest.log")
    logger = logging.ControlledLogger("pytest", "logs/")
    assert os.path.exists(f"{os.getcwd()}/logs/pytest.log")
    logger.info("test info")
    logger.debug("test debug")
    logger.error("test error")
    logger.warning("test warning")
    with open(f"{os.getcwd()}/logs/pytest.log", 'r') as f:
        log_file_contents = f.readlines()
    assert not log_file_contents
    logger.write()
    with open(f"{os.getcwd()}/logs/pytest.log", 'r') as f:
        log_file_contents = f.readlines()
    for line in log_file_contents:
        if "INFO" in line:
            assert "test info" in line
        if "DEBUG" in line:
            assert "test debug" in line
        if "WARNING" in line:
            assert "test warning" in line
        if "ERROR" in line:
            assert "test error" in line
