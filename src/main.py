import pandas as pd
from checker import run_checks
from report_html import generate_html_report

DATA_FILE = "data/sample_test_data.csv"

def main():
    df = pd.read_csv(DATA_FILE)
    anomalies = run_checks(df)
    generate_html_report(anomalies)

if __name__ == "__main__":
    main()




