import pandas as pd

MANDATORY_FIELDS = [
    "batch_id",
    "step",
    "timestamp",
    "user_id",
    "value"
]

def run_checks(df: pd.DataFrame) -> pd.DataFrame:
    anomalies = []

    # --- Complete: mandatory fields ---
    for idx, row in df.iterrows():
        for field in MANDATORY_FIELDS:
            if field not in df.columns or pd.isna(row.get(field)):
                anomalies.append({
                    "batch_id": row.get("batch_id", "UNKNOWN"),
                    "rule": "Missing mandatory field",
                    "alcoa": "Complete",
                    "severity": "HIGH",
                    "description": f"Campo obbligatorio mancante: {field}"
                })

    # --- Attributable ---
    if "user_id" in df.columns:
        for idx, row in df[df["user_id"].isna()].iterrows():
            anomalies.append({
                "batch_id": row.get("batch_id", "UNKNOWN"),
                "rule": "Missing operator",
                "alcoa": "Attributable",
                "severity": "HIGH",
                "description": "Registro non attribuibile a un utente"
            })

    # --- Accurate: numeric values ---
    if "value" in df.columns:
        for idx, row in df.iterrows():
            try:
                val = float(row["value"])
                if val < 0 or val > 1000:
                    anomalies.append({
                        "batch_id": row.get("batch_id", "UNKNOWN"),
                        "rule": "Value out of range",
                        "alcoa": "Accurate",
                        "severity": "HIGH",
                        "description": f"Valore fuori range: {val}"
                    })
            except Exception:
                anomalies.append({
                    "batch_id": row.get("batch_id", "UNKNOWN"),
                    "rule": "Non-numeric value",
                    "alcoa": "Accurate",
                    "severity": "HIGH",
                    "description": f"Valore non numerico: {row['value']}"
                })

    # --- Consistent: duplicate steps per batch ---
    if {"batch_id", "step"}.issubset(df.columns):
        dup = df[df.duplicated(subset=["batch_id", "step"], keep=False)]
        for idx, row in dup.iterrows():
            anomalies.append({
                "batch_id": row["batch_id"],
                "rule": "Inconsistent steps",
                "alcoa": "Consistent",
                "severity": "MEDIUM",
                "description": f"Step duplicato o incoerente in batch {row['batch_id']}"
            })

    # --- Original ---
    if "batch_id" in df.columns:
        dup_records = df[df.duplicated()]
        for idx, row in dup_records.iterrows():
            anomalies.append({
                "batch_id": row["batch_id"],
                "rule": "Untracked duplicate",
                "alcoa": "Original",
                "severity": "MEDIUM",
                "description": "Record duplicato senza tracciabilità"
            })

    return pd.DataFrame(anomalies)

