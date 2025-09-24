import logging

def logging_config(
        level: int = logging.INFO, 
        format: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        ):
    logging.basicConfig(
        level=level,  
        format=format,
    )
