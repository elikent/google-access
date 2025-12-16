import pandas as pd
import logging

# get logger
logger = logging.getLogger(__name__)

def df_from_gsheet(url: str, sheet_name: str | int | list) -> pd.DataFrame:
    try:
        df = pd.read_excel(url, sheet_name=sheet_name)
    except Exception as e:


