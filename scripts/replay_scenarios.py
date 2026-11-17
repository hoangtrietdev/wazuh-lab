#!/usr/bin/env python3
"""Replay synthetic lab events to the local syslog-ng UDP collector."""
import json
import socket
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
events = [json.loads(line) for line in (ROOT / "sample-logs/scenarios.jsonl").read_text().splitlines() if line]

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    for event in events:
        # RFC 3164 style envelope; LAB5 payload is intentionally synthetic.
        payload = f"<134>Nov 16 12:00:00 lab5-replay lab5: {event['evidence']}"
        sock.sendto(payload.encode(), ("127.0.0.1", 5514))
        print(f"Sent scenario: {event['scenario']}")
        time.sleep(0.25)

print(f"Replayed {len(events)} events to syslog-ng at 127.0.0.1:5514/udp")
