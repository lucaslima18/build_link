import coloredlogs
import logging


class LogHandler(coloredlogs.ColoredFormatter):
    """
    Custom log handler that formats and logs messages with colored output
    using the `coloredlogs` library.

    Inherits from `coloredlogs.ColoredFormatter` to enable colorized logging
    output, allowing logs to be more readable in the terminal. This handler
    provides methods to log messages at different levels (INFO, ERROR, DEBUG,
    WARNING) with customizable formatting.

    Attributes:
        logger (logging.Logger): Logger instance used for logging messages.
        format (str): Log format string to control the appearance of log messages.
        level (str): Logging level to control the verbosity of the logs.

    Methods:
        info(msg, extra=None): Logs a message with level INFO.
        error(msg, extra=None): Logs a message with level ERROR.
        debug(msg, extra=None): Logs a message with level DEBUG.
        warning(msg, extra=None): Logs a message with level WARNING.
    """

    def __init__(
        self,
        format="[%(levelname)s] - %(asctime)s, [%(name)s] %(message)s",
        level="INFO",
    ):
        super().__init__(format, level)
        self.logger = logging.getLogger()
        coloredlogs.install(level=level, fmt=format)

    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)

    def warning(self, msg, extra=None):
        self.logger.warning(msg, extra=extra)
