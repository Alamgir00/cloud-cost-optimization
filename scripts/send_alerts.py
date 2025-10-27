#!/usr/bin/env python3
"""send_alerts.py

Simple examples to post message to Slack or send email via SMTP. Use secrets in CI or environment variables.
"""
import argparse, os, requests, smtplib
from email.mime.text import MIMEText

def send_slack(webhook_url, message):
    payload = {'text': message}
    r = requests.post(webhook_url, json=payload, timeout=10)
    r.raise_for_status()

def send_email(smtp_server, smtp_port, username, password, to_email, subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = to_email
    with smtplib.SMTP(smtp_server, smtp_port) as s:
        s.starttls()
        s.login(username, password)
        s.sendmail(username, [to_email], msg.as_string())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--html', required=True)
    parser.add_argument('--slack-webhook', default=None)
    parser.add_argument('--smtp-server', default=None)
    parser.add_argument('--smtp-port', type=int, default=587)
    parser.add_argument('--smtp-user', default=None)
    parser.add_argument('--smtp-pass', default=None)
    parser.add_argument('--to', default=None)
    args = parser.parse_args()
    with open(args.html) as f:
        content = f.read()
    if args.slack_webhook:
        send_slack(args.slack_webhook, 'Weekly Cost Optimization report:\n' + 'See summary attached.')
        print('Slack notification sent.')
    if args.smtp_server and args.smtp_user and args.smtp_pass and args.to:
        send_email(args.smtp_server, args.smtp_port, args.smtp_user, args.smtp_pass, args.to, 'Cost Optimization Report', content)
        print('Email sent.')

if __name__ == '__main__':
    main()

