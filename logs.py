import logging
import os
import redis
from io import StringIO


class Logger:
    def __init__(self, name, level=logging.DEBUG, chanify=False):
        self.chanify =  chanify
        self.logger = logging.getLogger(name)
        logger_format = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
        self.log_stream = StringIO()
        logging.basicConfig(stream=self.log_stream, format=logger_format)
        self.logger.setLevel(level)
        console_output_handler = logging.StreamHandler()
        console_output_handler.setFormatter(logging.Formatter(logger_format))
        self.logger.addHandler(console_output_handler)
        try:
            self.redis_host = os.environ['REDIS_HOST']
            self.redis_channel = os.environ['REDIS_CHANIFY_CHANNEL']
            self.r = redis.Redis(
                host=self.redis_host,
                port=6379,
                decode_responses=True
            )
        except KeyError:
            self.logger.info('REDIS_HOST or REDIS_CHANIFY_CHANNEL not set. Setting with default values')
            self.redis_host = 'redis-pub-sub'
            self.redis_channel = 'chanify-notification'

            self.r = redis.Redis(
                host=self.redis_host,
                port=6379,
                decode_responses=True
            )
        try:
            if self.r is not None:
                self.r.ping()
                self.logger.info('Redis connection successful')
                self.r.publish(self.redis_channel, self.log_stream.getvalue())
        except redis.exceptions.ConnectionError as e :
            print('Redis connection error')
            self.logger.critical(f'Redis connection error for chanify logging: {e}')
            self.r = None

    def info(self, message):
        self.logger.info(message, stacklevel=2)
        if self.r and self.logger.level == logging.DEBUG and self.chanify:
            self.r.publish(self.redis_channel, self.log_stream.getvalue())

    def error(self, message):
        self.logger.error(message, stacklevel=2)
        if self.r and self.chanify:
            self.r.publish(self.redis_channel, self.log_stream.getvalue())

    def debug(self, message):
        self.logger.debug(message, stacklevel=2)
        if self.r and self.chanify:
            self.r.publish(self.redis_channel, self.log_stream.getvalue())

    def warning(self, message):
        self.logger.warning(message, stacklevel=2)
        if self.r and self.logger.level == logging.DEBUG and self.chanify:
            self.r.publish(self.redis_channel, self.log_stream.getvalue())

    def fatal(self, message):
        self.logger.fatal(message, stacklevel=2)
        if self.r and self.logger.level == logging.DEBUG:
            self.r.publish(self.redis_channel, self.log_stream.getvalue())


if __name__ == "__main__":
    # os.environ['REDIS_HOST'] = 'localhost'
    # os.environ['REDIS_CHANIFY_CHANNEL'] = 'chanify-notification'
    LOG = Logger('test', logging.WARNING)
    LOG.warning('test')
    LOG.error('test2')
