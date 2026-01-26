import pandas as pd

def generate_report(anomalies, output_path):
    df = pd.DataFrame(anomalies)
    df.to_csv(output_path, index=False)
