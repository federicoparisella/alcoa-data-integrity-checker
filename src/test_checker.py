import pandas as pd
from checker import run_checks

# Carica CSV fittizio
df = pd.read_csv("data/sample_test_data.csv")

# Esegui controlli ALCOA+
anomalies = run_checks(df)

# Mostra tutte le anomalie trovate
print(f"Trovate {len(anomalies)} anomalie:\n")
for a in anomalies:
    print(f"Riga {a['row']}: {a['rule']} ({a['alcoa']}, {a['severity']}) -> {a['description']}")
