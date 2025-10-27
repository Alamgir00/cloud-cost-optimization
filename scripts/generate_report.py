#!/usr/bin/env python3
"""generate_report.py

Convert CSV to HTML report with Jinja2 template and add basic summary.
"""
import csv, sys, argparse
from jinja2 import Template

HTML_TMPL = """
<html>
<head><title>Cost Optimization Report</title></head>
<body>
<h1>Cost Optimization Report</h1>
<p>Generated: {{ generated }}</p>
<h2>Summary</h2>
<ul>
  <li>Total instances: {{ total }}</li>
  <li>Downsize suggestions: {{ downsize }}</li>
  <li>Upgrade suggestions: {{ upgrade }}</li>
</ul>
<h2>Details</h2>
<table border="1" cellpadding="4" cellspacing="0">
<tr><th>InstanceId</th><th>Type</th><th>AZ</th><th>AvgCPU</th><th>Recommendation</th><th>EstHourlyPrice</th></tr>
{% for r in rows %}
<tr><td>{{ r.InstanceId }}</td><td>{{ r.InstanceType }}</td><td>{{ r.AZ }}</td><td>{{ r.AvgCPU }}</td><td>{{ r.Recommendation }}</td><td>{{ r.EstimatedHourlyPrice }}</td></tr>
{% endfor %}
</table>
</body>
</html>
"""

def main():
    parser = argparse.ArgumentParser(description='Generate HTML report from CSV')
    parser.add_argument('csvfile')
    parser.add_argument('htmlfile')
    args = parser.parse_args()
    rows = []
    with open(args.csvfile) as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    total = len(rows)
    down = sum(1 for r in rows if r['Recommendation']=='downsize')
    up = sum(1 for r in rows if r['Recommendation']=='upgrade')
    tpl = Template(HTML_TMPL)
    out = tpl.render(generated=__import__('datetime').datetime.utcnow().isoformat(), total=total, downsize=down, upgrade=up, rows=rows)
    with open(args.htmlfile,'w') as f:
        f.write(out)
    print(f"Wrote HTML report to {args.htmlfile}")

if __name__ == '__main__':
    main()

