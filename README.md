# Lab 5 — Network Anomaly Detection and Log Management

This lab uses syslog-ng to collect five safe, synthetic security events and forward them to Wazuh. Wazuh applies local detection rules; matching alert JSON is indexed by both the Wazuh indexer and a separate Elasticsearch service for a custom Kibana dashboard. The notifier also emails the local Mailpit inbox. The scenarios demonstrate detection logic; they do not exploit a real host or generate network scans.

## Architecture

```mermaid
flowchart LR
  replay[Scenario replay script] -->|UDP 5514| relay[syslog-ng]
  relay -->|UDP 514| manager[Wazuh manager and rules]
  manager -->|alerts| indexer[Wazuh indexer (OpenSearch)]
  indexer --> dashboard[Wazuh dashboard]
  manager -->|alerts.json| notifier[Alert notifier]
  notifier -->|SMTP| mailpit[Mailpit inbox]
  notifier -->|HTTP JSON| elastic[Elasticsearch 8.19.25]
  elastic -->|lab5-alerts index| kibana[Kibana 8.19.25 dashboard]
```

Wazuh's own indexer remains OpenSearch-based for its native dashboard. The additional official Elastic containers provide the standalone Elasticsearch and Kibana products requested by the assignment. The alert notifier forwards the same five custom-rule alert records to both Mailpit and Elasticsearch. Kibana is available at `http://localhost:5601`; Elasticsearch is published at `http://localhost:9201` because Wazuh already uses host port 9200. Both Elastic host ports are bound to loopback only.

## Five detection scenarios

| Rule | Scenario | Signal and interpretation |
|---|---|---|
| 100501 | SSH password guessing | Several authentication failures from one source; possible credential attack |
| 100502 | Port sweep | One source probes multiple destination ports; possible reconnaissance |
| 100503 | Web path traversal | Request includes `../`; possible attempt to read files outside the web root |
| 100504 | SQL injection probe | Request contains a SQL tautology marker; possible injection attempt |
| 100505 | DNS tunneling indicator | Unusually long encoded-looking DNS label; possible covert channel |

Each replayed message is explicitly labelled `LAB5` and contains synthetic evidence. These simple rules are teaching examples and need tuning before use on real networks.

## Requirements

- Linux VM or Docker host with Docker Compose, at least 4 CPU cores, 8 GB RAM, and 50 GB free disk for the Wazuh single-node stack.
- Set `vm.max_map_count` to `262144` on Linux hosts before starting the indexer.
- Internet access for the first run to retrieve the pinned Wazuh stack and container images.
- Approximately 3.5 GB of Docker memory for the added single-node Elasticsearch and Kibana containers.

## Deploy

From the project directory:

```sh
./scripts/setup.sh
```

The setup script obtains the official Wazuh Docker single-node deployment at version 4.14.10, generates its self-signed certificates, adds the lab's remote-syslog listener and custom rules, and starts the stack. The syslog-ng relay listens on UDP 5514. The dashboard is at `https://localhost` (first sign-in: `admin` / `SecretPassword`). Change the default credentials for any network-accessible deployment.

The project Compose command also starts Elasticsearch and Kibana. Create the Elasticsearch index and Kibana data view once:

```sh
docker compose -p lab5 -f vendor/wazuh-docker/single-node/docker-compose.yml \
  -f docker-compose.lab5.yml -f docker-compose.kibana.yml up -d
python3 scripts/setup_kibana.py
```

The data view is named **Lab 5 Security Alerts** and uses `lab5-alerts*` with `timestamp` as its time field. The Elasticsearch container stores data in a named Docker volume. The Elastic services have authentication and TLS disabled to keep the classroom setup simple, so Compose binds both web/API ports to `127.0.0.1` only. Do not change these bindings or expose the services to an untrusted network.

Allow a few minutes for startup. Check status with:

```sh
docker compose -p lab5 -f vendor/wazuh-docker/single-node/docker-compose.yml -f docker-compose.lab5.yml ps
```

## Replay and inspect

```sh
python3 scripts/replay_scenarios.py
```

In the Wazuh dashboard, open **Threat Hunting → Events** and enter this query:

```text
rule.id: 100501 or rule.id: 100502 or rule.id: 100503 or rule.id: 100504 or rule.id: 100505
```

Choose **Last 15 minutes** after replay and click **Update**. The lab query should return one event for each rule. Display `timestamp`, `agent.name`, `rule.description`, `rule.level`, and `rule.id`; open an event to inspect its full log, including source and destination. In this configuration the IP values are preserved in `full_log` rather than confirmed as separate parsed fields. `sample-logs/scenarios.jsonl` lists the exact events replayed.

### Custom Kibana dashboard

The standalone Kibana service has a saved dashboard named **Lab 5 Security Anomaly Dashboard**. It is separate from both the Wazuh overview and the default Kibana landing page, and is scoped by this KQL filter:

```text
rule.id: (100501 OR 100502 OR 100503 OR 100504 OR 100505)
```

It contains two saved visualizations backed by Elasticsearch's `lab5-alerts` index:

- **Lab 5 alerts by rule ID** — horizontal bar chart grouped by `rule.id`, showing all five scenarios.
- **Lab 5 alerts by severity** — donut chart grouped by `rule.level`, showing levels 8 and 10.

Open **Dashboards → Lab 5 Security Anomaly Dashboard** at `http://localhost:5601`. After replay, the dashboard's **Last 15 minutes** range shows one event for each of rules 100501–100505. The severity visualization shows two level-8 events and three level-10 events when all five sample alerts are present.

Replay a new batch to verify end-to-end detection, indexing, and notification:

```sh
python3 scripts/replay_scenarios.py
curl -s http://localhost:9201/lab5-alerts/_count
```

The `scripts/notify_alerts.py` worker indexes each matching JSON alert and sends its administrator-facing email to Mailpit. The notification includes timestamp, rule ID/description/level, and raw event context. Local screenshots of the Docker services, Wazuh alert search, Kibana dashboard, and Mailpit inbox are included in the report.

Check manager alert output with:

```sh
docker compose -p lab5 -f vendor/wazuh-docker/single-node/docker-compose.yml -f docker-compose.lab5.yml exec wazuh.manager sh -c 'tail -n 30 /var/ossec/logs/alerts/alerts.json'
```

## Email alerts

The alert notifier watches the manager's JSON alert log and sends Lab 5 alerts to the local Mailpit inbox at `http://localhost:8025`. This demonstrates email delivery without sending messages outside the lab. Optional external SMTP setup is in `docs/NOTIFICATIONS.md`; do not put credentials in source control.

## Stop and clean up

```sh
docker compose -p lab5 -f vendor/wazuh-docker/single-node/docker-compose.yml -f docker-compose.lab5.yml -f docker-compose.kibana.yml down
```

The command preserves indexed data. Add `-v` only when you intentionally want to delete all lab data.

## Repository map

- `config/syslog-ng/syslog-ng.conf` — UDP collection and forwarding
- `config/wazuh/rules/local_rules.xml` — five lab detection rules
- `sample-logs/scenarios.jsonl` — synthetic event fixtures
- `scripts/` — setup and replay helpers
- `docs/` — scenario analysis and notification setup

## Limitations and next steps

These signatures detect known strings in intentionally labelled sample logs; they do not establish that an intrusion succeeded. A production design should use endpoint and network telemetry, richer parsing, time-window correlation, thresholding, authenticated/encrypted log transport, access controls, retention policies, and alert triage. Further work could map detections to MITRE ATT&CK, add Suricata events, and test precision/false-positive rates against a benign baseline.
