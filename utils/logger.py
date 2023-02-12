import logging

logger = logging.getLogger('Logger')
logger.setLevel(logging.INFO)


handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s',
    '%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

logger.addHandler(handler)
