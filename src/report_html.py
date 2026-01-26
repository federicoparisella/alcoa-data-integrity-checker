import pandas as pd
import json
from pathlib import Path

def generate_html_report(df: pd.DataFrame, output_path="output/report.html"):
    Path("output").mkdir(exist_ok=True)

    severity_counts = df["severity"].value_counts().reindex(
        ["HIGH", "MEDIUM", "LOW"], fill_value=0
    )

    batch_counts = (
        df["batch_id"]
        .fillna("UNKNOWN")
        .value_counts()
        .sort_index()
    )

    severity_fig = {
        "data": [{
            "x": severity_counts.index.tolist(),
            "y": severity_counts.values.tolist(),
            "type": "bar"
        }],
        "layout": {
            "title": "Anomalie per Severità",
            "yaxis": {"dtick": 1, "rangemode": "tozero"}
        }
    }

    batch_fig = {
        "data": [{
            "x": batch_counts.index.tolist(),
            "y": batch_counts.values.tolist(),
            "type": "bar"
        }],
        "layout": {
            "title": "Anomalie per Batch ID",
            "yaxis": {"dtick": 1, "rangemode": "tozero"}
        }
    }

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>ALCOA+ Data Integrity Report</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
<style>
.high {{ background-color: #ffcccc; }}
.medium {{ background-color: #ffe699; }}
.low {{ background-color: #e6ffcc; }}
</style>
</head>
<body>

<h1>ALCOA+ Data Integrity Report</h1>

<div id="severity-chart"></div>
<div id="batch-chart"></div>

<table id="report" class="display">
<thead>
<tr>
<th>Batch ID</th>
<th>Rule</th>
<th>ALCOA+</th>
<th>Severity</th>
<th>Description</th>
</tr>
</thead>
<tbody>
"""

    for _, r in df.iterrows():
        cls = r["severity"].lower()
        html += f"""
<tr class="{cls}">
<td>{r['batch_id']}</td>
<td>{r['rule']}</td>
<td>{r['alcoa']}</td>
<td>{r['severity']}</td>
<td>{r['description']}</td>
</tr>
"""

    html += f"""
</tbody>
</table>

<script>
Plotly.newPlot('severity-chart', {json.dumps(severity_fig["data"])}, {json.dumps(severity_fig["layout"])});
Plotly.newPlot('batch-chart', {json.dumps(batch_fig["data"])}, {json.dumps(batch_fig["layout"])});

$(document).ready(function() {{
    $('#report').DataTable();
}});
</script>

</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)



