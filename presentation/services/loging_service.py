import logging

class LoggingService:
    def __init__(self, log_file='cotizador_backend.log'):
        self.logger = logging.getLogger('CotizadorLogger')
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.hasHandlers():
            file_handler = logging.FileHandler(log_file, mode='a')
            formatter = logging.Formatter(
                fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
