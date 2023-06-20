from loguru import logger


def test_info_function():
    logger.info("info message")


def test_warning_function():
    logger.warning("warning message")


def test_error_function():
    logger.error("error message")


if __name__ == "__main__":
    test_info_function()
    test_warning_function()
    test_error_function()
