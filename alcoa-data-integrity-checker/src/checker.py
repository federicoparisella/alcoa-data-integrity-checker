from rules import *

def run_checks(df):
    anomalies = []
    anomalies += check_missing_mandatory_fields(df)
    return anomalies
