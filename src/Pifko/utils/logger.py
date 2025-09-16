import logging


def get_logger(name: str = "Pifko") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


logger = get_logger()
