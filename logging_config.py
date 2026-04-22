import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
AUDIT_LOG_FILE = os.path.join(LOG_DIR, "audit.log")


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    app_handler = RotatingFileHandler(
        APP_LOG_FILE,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    app_handler.setFormatter(formatter)
    app_handler.setLevel(logging.INFO)

    audit_handler = RotatingFileHandler(
        AUDIT_LOG_FILE,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )
    audit_handler.setFormatter(formatter)
    audit_handler.setLevel(logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if not root_logger.handlers:
        root_logger.addHandler(app_handler)

    app_logger = logging.getLogger("smartspend.app")
    audit_logger = logging.getLogger("smartspend.audit")

    app_logger.setLevel(logging.INFO)
    audit_logger.setLevel(logging.INFO)

    if not app_logger.handlers:
        app_logger.addHandler(app_handler)

    if not audit_logger.handlers:
        audit_logger.addHandler(audit_handler)

    return app_logger, audit_logger