#!/usr/bin/env python3
"""Add the lab's isolated UDP syslog input to the official manager config."""
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
if "lab5-syslog" not in text:
    addition = '''
<!-- lab5-syslog: lab-only unauthenticated UDP input; keep this stack isolated -->
<ossec_config>
  <remote>
    <connection>syslog</connection>
    <port>514</port>
    <protocol>udp</protocol>
    <allowed-ips>172.16.0.0/12</allowed-ips>
    <local_ip>0.0.0.0</local_ip>
  </remote>
</ossec_config>
'''
    text = text.rstrip() + "\n" + addition

# The default Wazuh vulnerability feed downloads a large database that is not
# used by these five network-event scenarios. Keep the teaching stack within
# the Docker disk budget; rule-based detection remains enabled.
import re
pattern = r"(<vulnerability-detection>\s*<enabled>)yes(</enabled>)"
text, count = re.subn(pattern, r"\1no\2", text, count=1)
if count == 0 and "<vulnerability-detection>" in text:
    text = text.replace("<vulnerability-detection>", "<vulnerability-detection>\n    <enabled>no</enabled>", 1)

path.write_text(text, encoding="utf-8")
print(f"Configured lab syslog input in {path}")
