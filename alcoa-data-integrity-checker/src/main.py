from loader import load_csv
from checker import run_checks
from report import generate_report

INPUT = "data/sample_data.csv"
OUTPUT = "output/report.csv"

df = load_csv(INPUT)
anomalies = run_checks(df)
generate_report(anomalies, OUTPUT)

print("Report generato")
