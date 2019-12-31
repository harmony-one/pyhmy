import os

import pytest

from pyhmy import logging


def test_basic_logger():
    logger = logging.ControlledLogger("test", "logs/")
    logger.info("test info")
    logger.debug("test debug")
    logger.error("test error")
    logger.warning("test warning")
    logger.write()
    # TODO: finish this test
