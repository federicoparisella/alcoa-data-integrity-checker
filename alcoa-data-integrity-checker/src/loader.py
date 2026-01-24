import pandas as pd

def load_csv(path):
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["last_modified_at"] = pd.to_datetime(df["last_modified_at"], errors="coerce")
    return df
