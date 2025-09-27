import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional



def report(msg: str, log_level: str = "info", *, verbose: bool = False, logger: logging.Logger | None = None) -> None:
    '''Log and optionally print'''
    _map = {
        "info": logging.info,
        "warning": logging.warning,
        "error": logging.error,
        "critical": logging.critical,
        "debug": logging.debug,
    }
    log_fn = _map.get(log_level.lower(), logging.info)
    log_fn(msg)
    if verbose or log_level != "info":
        print(msg)

def logging_config(
        level: int = logging.INFO, 
        fmt: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        log_file: Optional[Path] = None,
        max_bytes: int = 5_000_000, # ~5 MB per file
        backup_count: int = 5,
        console: bool = True,
        force: bool = True
        ) -> None:
    
    '''Configure global logging for the application.

    Args:
        level: Logging level (e.g., logging.INFO, logging.DEBUG)
        fmt: Format string for log messages. Defauylt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        log_file: Path object for log file.
        max_bytes: Max size per log file before rotation (default = ~5MB).
        backup_count: Number of rotates log files to keep.
        console: If True, log to console.
        force: If True, recopngireu even if logging was already set up.
    '''

    # Declare empty list of handlers. Possible handlers = StreamHandler (console) and RotatingFileHandler (file)  
    handlers = []

    # File handler if requested
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"       
        )
        file_handler.setFormatter(logging.Formatter(fmt))
        handlers.append(file_handler)

    # Console handler if not surpressed
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(fmt))
        handlers.append(console_handler)

    logging.basicConfig(
        level=level,  
        handlers=handlers,
        force=force
    )
