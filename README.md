# Cloud Cost Optimization — Automated Rightsizing & Reporting

**Author:** Sk Alamgir Ali
**Goal:** Reduce AWS compute costs by automating EC2 metrics collection, rightsizing recommendations, and periodic reporting using Python, Terraform (optional), and GitHub Actions.

## What you get
- `scripts/collect_metrics.py` — collects EC2 metrics from CloudWatch and generates CSV report
- `scripts/generate_report.py` — converts CSV to HTML report with summary
- `scripts/send_alerts.py` — sample script to send email or Slack (uses webhook/SMTP)
- `.github/workflows/cost-optimizer.yml` — scheduled GitHub Actions workflow to run analysis
- `infra/` — optional Terraform skeleton for IAM role and S3 bucket
- `reports/` — example output reports (empty by default)
- `README.md` — this file

## Quickstart (local)
1. Clone or download this repo.
2. Ensure AWS credentials are configured (or use GitHub Actions secrets):
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION` (e.g., `us-east-1`)
3. Install dependencies:
```bash
python -m venv venv && source venv/bin/activate
pip install -r scripts/requirements.txt
```
4. Run the analysis locally:
```bash
python scripts/collect_metrics.py --days 7 --output reports/cost_optimization_report.csv
python scripts/generate_report.py reports/cost_optimization_report.csv reports/cost_optimization_report.html
```
5. (Optional) Send alert/report:
```bash
python scripts/send_alerts.py --html reports/cost_optimization_report.html --slack-webhook "<WEBHOOK_URL>"
```

## Files overview
- `scripts/collect_metrics.py` collects CPU and Network metrics for running EC2 instances and writes a CSV with recommendations.
- `scripts/generate_report.py` turns CSV into a readable HTML report and summary statistics.
- `.github/workflows/cost-optimizer.yml` runs the analysis on a schedule and uploads the report as an artifact.
- `infra/` contains optional Terraform to create an S3 bucket and IAM role for running the analysis in AWS if needed.

## Notes & Production tips
- For production, use AWS Compute Optimizer and Trusted Advisor as additional sources.
- Store reports in S3 and visualize trends with Athena/QuickSight or Grafana.
- Use GitHub OIDC (preferred) rather than long-lived AWS keys in CI.
- Add throttling, retries, and robust error handling to scripts in larger environments.

---

