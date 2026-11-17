# Scenario analysis

All addresses use documentation-only IPv4 ranges (RFC 5737). Event payloads are produced by `scripts/replay_scenarios.py` and sent to the local collector; they do not execute an attack.

| ID | Detection goal | Logged evidence | Why it matters / response |
|---|---|---|---|
| 100501 | Repeated SSH authentication failures | `failures=12 service=sshd` | Check source reputation, account exposure, and authentication policy; block only after validation. |
| 100502 | Multi-port reconnaissance | Seven common service ports in one event | Correlate with firewall and flow records; verify whether the source is an authorized scanner. |
| 100503 | Path traversal attempt | URL-encoded `../` path toward `/etc/passwd` | Inspect web server request and response; patch path handling and check for file access. |
| 100504 | SQL injection attempt | Encoded quote and `OR 1=1` marker | Review application logs and query handling; use parameterized queries and assess data exposure. |
| 100505 | DNS tunnel indicator | Long label and TXT query to reserved `.invalid` domain | Check DNS query volume and endpoint process; a long label alone is not proof of tunneling. |

The current rules are single-event signatures. The SSH and port-sweep fixtures summarize patterns instead of generating repeated login attempts or network probes, which keeps replay deterministic and safe. A realistic follow-up would aggregate endpoint events over a time window and evaluate false positives using benign traffic.
