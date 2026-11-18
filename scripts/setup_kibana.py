#!/usr/bin/env python3
"""Create the Lab 5 Elasticsearch index and Kibana data view."""
import json
import time
import urllib.error
import urllib.request

ES = "http://localhost:9201"
KIBANA = "http://localhost:5601"


def request(url, method="GET", body=None, kibana=False):
    headers = {"Content-Type": "application/json"}
    if kibana:
        headers["kbn-xsrf"] = "true"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=10) as response:
        return json.loads(response.read() or b"{}")


for _ in range(120):
    try:
        request(f"{ES}/")
        break
    except (urllib.error.URLError, TimeoutError):
        time.sleep(2)
else:
    raise SystemExit("Elasticsearch did not become ready at http://localhost:9201")

request(
    f"{ES}/_index_template/lab5-alerts-template",
    "PUT",
    {
        "index_patterns": ["lab5-alerts*"],
        "template": {
            "mappings": {
                "properties": {
                    "timestamp": {"type": "date"},
                    "rule": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "level": {"type": "integer"},
                            "description": {"type": "keyword"},
                        }
                    },
                    "full_log": {"type": "match_only_text"},
                }
            }
        },
    },
)
try:
    request(f"{ES}/lab5-alerts", "PUT")
except urllib.error.HTTPError as error:
    if error.code != 400:
        raise

for _ in range(120):
    try:
        request(f"{KIBANA}/api/status")
        break
    except (urllib.error.URLError, TimeoutError):
        time.sleep(2)
else:
    raise SystemExit("Kibana did not become ready at http://localhost:5601")

views = request(f"{KIBANA}/api/data_views", kibana=True).get("data_view", [])
if not any(view.get("title") == "lab5-alerts*" for view in views):
    request(
        f"{KIBANA}/api/data_views/data_view",
        "POST",
        {
            "data_view": {
                "title": "lab5-alerts*",
                "name": "Lab 5 Security Alerts",
                "timeFieldName": "timestamp",
            }
        },
        kibana=True,
    )
print("Created index template, lab5-alerts index, and Lab 5 Security Alerts data view.")
