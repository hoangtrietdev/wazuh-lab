#!/usr/bin/env python3
"""Poll Wazuh alerts and email only the five Lab 5 rule IDs when SMTP is set."""
import json
import os
import smtplib
import time
import urllib.error
import urllib.request
from email.message import EmailMessage
from pathlib import Path

LOG = Path("/var/ossec/logs/alerts/alerts.json")
RULES = {f"10050{i}" for i in range(1, 6)}

def notify(alert):
    rule = alert.get("rule", {})
    title = f"Lab 5 alert {rule.get('id')}: {rule.get('description', 'Detection')}"
    body = json.dumps(alert, indent=2, ensure_ascii=False)
    host = os.getenv("SMTP_HOST")
    sender, recipient = os.getenv("ALERT_FROM"), os.getenv("ALERT_TO")
    if not (host and sender and recipient):
        print(f"DETECTED (email not configured): {title}", flush=True)
    else:
        message = EmailMessage()
        message["Subject"], message["From"], message["To"] = title, sender, recipient
        message.set_content(body)
        with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", "587")), timeout=15) as smtp:
            if os.getenv("SMTP_USE_TLS", "true").lower() in {"1", "true", "yes"}:
                smtp.starttls()
            user, password = os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD")
            if user and password:
                smtp.login(user, password)
            smtp.send_message(message)
        print(f"Email sent: {title}", flush=True)

    # Mirror the same detected alert into Elasticsearch for the custom Kibana view.
    elasticsearch = os.getenv("ELASTICSEARCH_URL")
    if elasticsearch:
        request = urllib.request.Request(
            f"{elasticsearch.rstrip('/')}/lab5-alerts/_doc",
            data=json.dumps(alert, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                print(f"Indexed alert in Elasticsearch: {response.status}", flush=True)
        except (urllib.error.URLError, TimeoutError) as error:
            print(f"Elasticsearch indexing failed: {error}", flush=True)

while not LOG.exists():
    time.sleep(2)
with LOG.open(encoding="utf-8") as stream:
    stream.seek(0, 2)  # Ignore old alerts; notify only about new events.
    while True:
        line = stream.readline()
        if not line:
            time.sleep(1)
            continue
        try:
            alert = json.loads(line)
        except json.JSONDecodeError:
            continue
        if str(alert.get("rule", {}).get("id")) in RULES:
            try:
                notify(alert)
            except Exception as error:
                print(f"Notification failed: {error}", flush=True)
