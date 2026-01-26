import pandas as pd
from severity import *

def check_missing_mandatory_fields(df):
    anomalies = []
    mandatory = ["batch_id", "step", "timestamp", "user_id", "value"]

    for idx, row in df.iterrows():
        for field in mandatory:
            if pd.isna(row[field]):
                anomalies.append({
                    "row": idx,
                    "rule": "Missing mandatory field",
                    "alcoa": "Complete",
                    "severity": SEVERITY_HIGH,
                    "description": f"Campo obbligatorio mancante: {field}"
                })
    return anomalies
