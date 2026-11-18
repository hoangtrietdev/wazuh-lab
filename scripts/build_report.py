#!/usr/bin/env python3
"""Build the Lab 5 submission report from verified evidence files."""
from pathlib import Path
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Lab5_Report.docx"
EVIDENCE = ROOT / "evidence"

NAVY = "000000"
BLUE = "2F75B5"
LIGHT = "EAF1F8"
GRAY = "5B6573"

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.7)
sec.bottom_margin = Inches(0.65)
sec.left_margin = Inches(0.78)
sec.right_margin = Inches(0.78)

styles = doc.styles
styles["Normal"].font.name = "Aptos"
styles["Normal"].font.size = Pt(10)
styles["Normal"].font.color.rgb = RGBColor.from_string("263238")
styles["Normal"].paragraph_format.space_after = Pt(6)
for name, size, color in [("Title", 27, NAVY), ("Heading 1", 17, NAVY), ("Heading 2", 12, BLUE)]:
    style = styles[name]
    style.font.name = "Aptos Display"
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor.from_string(color)
    style.paragraph_format.space_before = Pt(12)
    style.paragraph_format.space_after = Pt(5)

def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)

def set_cell_text(cell, text, bold=False, color=None, size=9):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Aptos"
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    for idx, value in enumerate(headers):
        set_cell_text(t.rows[0].cells[idx], value, True, "FFFFFF", 9)
        shade(t.rows[0].cells[idx], NAVY)
    for row in rows:
        cells = t.add_row().cells
        for idx, value in enumerate(row):
            set_cell_text(cells[idx], str(value), size=8.5)
            if len(t.rows) % 2 == 0:
                shade(cells[idx], "F4F7FA")
    if widths:
        for row in t.rows:
            for i, width in enumerate(widths):
                row.cells[i].width = Inches(width)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return t

def bullet(text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    p.add_run(text)
    return p

def add_screenshot(name, caption, expected=False):
    path = EVIDENCE / name
    if path.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(str(path), width=Inches(6.4))
        c = doc.add_paragraph(caption)
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.runs[0].italic = True
        c.runs[0].font.size = Pt(8)
        c.runs[0].font.color.rgb = RGBColor.from_string(GRAY)
    else:
        doc.add_paragraph(f"Evidence image pending: {caption} ({name})")

def add_figure(name, caption, width=6.35):
    path = EVIDENCE / name
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(path), width=Inches(width))
    c = doc.add_paragraph(caption)
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.keep_together = True
    c.runs[0].italic = True
    c.runs[0].font.size = Pt(8)
    c.runs[0].font.color.rgb = RGBColor.from_string(GRAY)

# Header and page number footer
header = sec.header.paragraphs[0]
header.text = "ESIGELEC  |  Information System Security  |  Lab 5"
header.runs[0].font.size = Pt(8)
header.runs[0].font.color.rgb = RGBColor.from_string(GRAY)
footer = sec.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
rr = footer.add_run("Phu Hoang Triet NGO  •  Page ")
rr.font.size = Pt(8)
fld = OxmlElement("w:fldSimple")
fld.set(qn("w:instr"), "PAGE")
footer._p.append(fld)

# Cover
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(90)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("LAB 5 PROJECT REPORT")
r.bold = True
r.font.name = "Aptos Display"
r.font.size = Pt(12)
r.font.color.rgb = RGBColor.from_string(BLUE)
title = doc.add_paragraph("Network Anomaly Detection and Log Management")
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_after = Pt(4)
title_run = title.runs[0]
title_run.font.name = "Aptos Display"
title_run.font.size = Pt(27)
title_run.font.bold = True
title_run.font.color.rgb = RGBColor.from_string(NAVY)
subtitle = doc.add_paragraph("A Docker lab with custom Kibana dashboards and Wazuh detection")
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.runs[0].font.size = Pt(13)
subtitle.runs[0].font.color.rgb = RGBColor.from_string(GRAY)
doc.add_paragraph(" ")
table(["Course information", "Submission details"], [
    ("School", "ESIGELEC"),
    ("Course", "Information System Security"),
    ("Student", "Phu Hoang Triet NGO"),
    ("Project", "Lab 5 — anomaly detection and log management"),
    ("Date", "17 November 2026"),
], [2.2, 4.2])
doc.add_paragraph("Purpose", style="Heading 2")
doc.add_paragraph(
    "This report documents a reproducible security monitoring laboratory. Five synthetic intrusion indicators travel through syslog-ng to Wazuh, where local rules raise alerts. Each alert is searchable in the Wazuh indexer and mirrored by the notifier into a standalone Elasticsearch index for the custom Kibana dashboard. A local email-capture service demonstrates alert notification without sending messages to an external recipient."
)
doc.add_page_break()

doc.add_paragraph("Executive Summary", style="Heading 1")
doc.add_paragraph(
    "The lab implements a complete event path for five network-security scenarios: SSH password guessing, port reconnaissance, web path traversal, SQL injection probing, and a DNS tunneling indicator. The replay script sends labelled sample events to the syslog-ng collector; custom Wazuh decoders and rules identify them; the Wazuh manager writes JSON alerts to its indexer; the dashboard supports search and visualization; and the notifier delivers each matching alert to a local Mailpit inbox."
)
doc.add_paragraph(
    "The deployment includes the requested standalone Elasticsearch and Kibana containers alongside Wazuh. Wazuh's own indexer remains OpenSearch-based for the native Wazuh dashboard; the notifier mirrors each new Lab 5 alert to the Elasticsearch service used by Kibana. This keeps Wazuh rule analysis and the exact Elastic products in one integrated local lab."
)
table(["Deployment component", "Role in this lab"], [
    ("syslog-ng", "Receives UDP syslog events on port 5514 and forwards them to Wazuh on UDP 514."),
    ("Wazuh manager", "Reads remote syslog, decodes Lab 5 fields, applies rules 100501–100505, and writes alerts."),
    ("Wazuh indexer", "Stores searchable alert records for the dashboard."),
    ("Wazuh dashboard", "Searches, filters, and visualizes Wazuh alerts."),
    ("Elasticsearch and Kibana", "Elasticsearch 8.19.25 stores mirrored alerts in lab5-alerts; Kibana 8.19.25 provides the custom Lab 5 dashboard."),
    ("Alert notifier and Mailpit", "Watches new Lab 5 alerts, mirrors them to Elasticsearch, sends local SMTP messages, and displays them in an inbox."),
], [1.8, 4.6])

doc.add_paragraph("System Architecture", style="Heading 1")
table(["Stage", "Data flow"], [
    ("1. Event source", "scripts/replay_scenarios.py sends synthetic RFC 3164-style events to localhost UDP/5514."),
    ("2. Collection", "syslog-ng accepts the packets and forwards them to wazuh.manager UDP/514."),
    ("3. Analysis", "The Wazuh remote-syslog input and Lab 5 decoder/rules create alert records."),
    ("4. Storage and visualization", "Wazuh keeps its native copy in the Wazuh indexer. The notifier also posts matching JSON alert documents to Elasticsearch index lab5-alerts; Kibana queries that index through the Lab 5 Security Alerts data view."),
    ("5. Notification", "The notifier filters rule IDs 100501–100505, mirrors them to Elasticsearch, and emails Mailpit on the internal Docker network."),
], [1.8, 4.6])
doc.add_paragraph("The Wazuh services, syslog-ng, notifier, and Mailpit run on the lab Docker network. Elasticsearch and Kibana are added with a second Compose file and share the project network. Host ports are 5514/UDP for replay, 8025 for Mailpit, 9201 for Elasticsearch, and 5601 for Kibana; Wazuh keeps its existing 9200 and 443 ports.")
add_figure("lab5-architecture.png", "Figure 1. Integrated event path: Wazuh detection feeds both the Wazuh indexer and a custom Elasticsearch/Kibana view, while the notifier sends local email.")

doc.add_paragraph("Scenario Design and Detection", style="Heading 1")
doc.add_paragraph("The scenarios model suspicious indicators, not successful compromise. The replay data uses RFC 5737 documentation addresses and reserved test domains. It does not connect to a real target, execute an exploit, attempt a login, or scan ports.")
scenarios = [
    ("100501 — SSH password guessing", "Signal and rationale: a single event summarizes 12 failed SSH authentication attempts from 192.0.2.44 against 192.0.2.10. Repeated failures against one service can indicate credential guessing; this replay represents the pattern in one synthetic message, not 12 live login attempts. Rule level 10 maps to MITRE ATT&CK T1110 (Brute Force).", "Priority fields: source and destination, failures=12, service=sshd, timestamp, rule.id=100501, level=10, and full_log. Response: validate whether the source is an approved scanner, identify the targeted account in authentication logs, check for a later successful login, then apply rate limiting or block the source if malicious activity is confirmed."),
    ("100502 — Port sweep and service reconnaissance", "Signal and rationale: source 192.0.2.45 probes ports 21, 22, 23, 80, 443, 445, and 3389 on 192.0.2.10. A broad service-port pattern can precede exploitation, but an authorized inventory scanner can look similar. Rule level 8 maps to T1046 (Network Service Discovery).", "Priority fields: source and destination, ports, protocol when available, timestamp, rule.id=100502, and firewall/flow-log correlation. Response: compare timing and source ownership with the approved scan schedule; inspect firewall decisions and destination services; isolate or rate-limit only after confirming the source is unauthorized."),
    ("100503 — Web path traversal probe", "Signal and rationale: the HTTP request uses encoded parent-directory markers in a file parameter and targets a sensitive path. If decoded unsafely, traversal sequences may escape the web root. The synthetic request does not contact an application. Rule level 10 maps to T1190 (Exploit Public-Facing Application).", "Priority fields: source and destination, HTTP method, URI, decoded path indicator, status/response bytes if available, timestamp, and rule.id=100503. Response: preserve the request, check the web response and nearby access logs, review file-access telemetry, and verify canonical path validation and web-root restrictions."),
    ("100504 — SQL injection probe", "Signal and rationale: an encoded quote followed by an OR 1=1 tautology appears in a login parameter. This resembles an attempt to change query logic. A matched request is evidence of probing, not proof of compromise. Rule level 10 maps to T1190.", "Priority fields: source and destination, method, endpoint, parameter name, decoded payload marker, HTTP status, timestamp, and rule.id=100504. Response: correlate the request with application and database logs, look for errors or unusual returned records, and confirm parameterized queries and safe error handling."),
    ("100505 — DNS tunneling indicator", "Signal and rationale: a long encoded-looking label with a TXT query to attacker.invalid is a possible covert-channel indicator. Long labels and TXT records also have legitimate uses, so this is a triage signal rather than a conclusion. Rule level 8 maps to T1048 (Exfiltration Over Alternative Protocol).", "Priority fields: queried name, query type, source endpoint, resolver, timestamp, rule.id=100505, and DNS response/volume context. Response: inspect query frequency and label entropy over time, map the endpoint to a process or user, inspect resolver answers, and compare with approved tunneling tests."),
]
for heading, rationale, response in scenarios:
    doc.add_paragraph(heading, style="Heading 2")
    doc.add_paragraph(rationale)
    doc.add_paragraph(response)

table(["Rule ID", "Scenario", "Level", "ATT&CK", "Evidence key"], [
    ("100501", "SSH password guessing", "10", "T1110", "failures=12; service=sshd"),
    ("100502", "Port sweep", "8", "T1046", "ports=21,22,23,80,443,445,3389"),
    ("100503", "Path traversal", "10", "T1190", "encoded ../ path"),
    ("100504", "SQL injection", "10", "T1190", "encoded quote and OR 1=1"),
    ("100505", "DNS tunnel indicator", "8", "T1048", "long label; TXT query"),
], [0.8, 1.5, 0.55, 0.75, 2.8])

doc.add_paragraph("Log Collection and Management", style="Heading 1")
doc.add_paragraph("The priority fields are timestamp, source IP, destination IP, service or protocol, scenario identifier, evidence text, Wazuh rule ID, rule description, severity, and full event. They support time correlation, source attribution, target scoping, triage prioritization, and review of the exact indicator. In the current alert documents, source and destination are preserved inside full_log; a separately parsed srcip field was not confirmed, so filtering by source IP requires opening the event details.")
table(["Priority field", "Why the analyst needs it", "Current evidence"], [
    ("timestamp", "Correlate activity and order events.", "Wazuh alert timestamp"),
    ("source and destination IP", "Attribute the source and identify affected services or hosts.", "Preserved in full_log"),
    ("rule ID, description, and level", "Identify the detection and prioritize triage.", "100501–100505; levels 8 or 10"),
    ("service, protocol, and indicator", "Understand the behavior that triggered the rule.", "sshd, ports, HTTP request, or DNS query in full_log"),
], [1.35, 2.7, 2.35])
doc.add_paragraph("In Kibana Discover, select the Lab 5 Security Alerts data view and filter for rule IDs 100501–100505. After replaying the five scenarios, the Last 15 minutes query returned five documents, one for each rule. The supplied Wazuh Threat Hunting capture is an earlier four-row view; the five-alert replay is independently demonstrated by the current Kibana counts, the five-message Mailpit inbox, and the manager timestamps recorded above.")
doc.add_paragraph("The manager timestamps for rules 100501–100505 are 20:43:26.553, 20:43:26.767, 20:43:27.016, 20:43:27.267, and 20:43:27.523 UTC on 17 November 2026. The first-to-last span is 0.97 seconds, demonstrating near-real-time processing for this controlled replay. Each custom rule fired once. This is a demonstration result, not a normal-traffic baseline or a capacity test.")
add_figure("scenario-counts.png", "Figure 2. One replay alert was observed for each of the five custom scenarios.")
add_figure("severity-counts.png", "Figure 3. The replay produced three level 10 alerts and two level 8 alerts.")
doc.add_paragraph("Parsing limitation: Wazuh's predecoder identified the syslog program and hostname, but the custom decoder object is empty in the observed alert JSON. Therefore srcip and dstip are retained in full_log and are not claimed as normalized searchable fields. The next iteration should parse these key/value pairs into dedicated fields, validate them with sample events, and then build source-IP aggregations.")

doc.add_paragraph("Alert Notification", style="Heading 1")
doc.add_paragraph("The notifier tails the shared Wazuh alerts.json file and selects only the five custom rule IDs. It creates one email per newly observed matching alert. The message includes the rule description, level, alert timestamp, and raw JSON event context, so an administrator can see what triggered the notification and pivot to the dashboard. This report pairs each rule with a recommended triage response. SMTP remains inside the Docker network and the messages appear in Mailpit at http://localhost:8025; no email is sent to an external account. The supplied inbox screenshot shows five messages. External email can be configured with protected SMTP settings; credentials are not included in this submission.")

doc.add_paragraph("Deployment and Reproduction", style="Heading 1")
for line in [
    "Requirements: Docker Compose, at least 4 CPU cores, 8 GB RAM, and 50 GB free storage; on Linux, set vm.max_map_count to 262144.",
    "Run ./scripts/setup.sh from the project root. The script retrieves the official Wazuh Docker stack pinned to v4.14.10, generates local certificates, applies the syslog listener, and starts the lab services.",
    "Optional vulnerability detection was disabled to keep the local stack within the available disk budget; this module is not required for the custom signature scenarios.",
    "Wait for the manager, indexer, and dashboards to become ready. Open https://localhost for Wazuh, http://localhost:5601 for Kibana, and http://localhost:8025 for Mailpit.",
    "Start the standalone Elastic services with docker compose -p lab5 -f vendor/wazuh-docker/single-node/docker-compose.yml -f docker-compose.lab5.yml -f docker-compose.kibana.yml up -d. Elasticsearch is published on localhost:9201 because Wazuh already uses port 9200.",
    "Run python3 scripts/setup_kibana.py once to create the lab5-alerts index template and the Lab 5 Security Alerts Kibana data view (timestamp field: timestamp). The notifier automatically mirrors every new matching Wazuh alert to Elasticsearch and Mailpit.",
    "Run python3 scripts/replay_scenarios.py to transmit one synthetic event for each scenario.",
    "Open Dashboards > Lab 5 Security Anomaly Dashboard in Kibana. The persistent KQL filter is rule.id: (100501 OR 100502 OR 100503 OR 100504 OR 100505). The panels show count by rule ID and severity. Set Last 15 minutes immediately after replay; expand the range if inspecting older data.",
    "Stop all services with docker compose -p lab5 -f vendor/wazuh-docker/single-node/docker-compose.yml -f docker-compose.lab5.yml -f docker-compose.kibana.yml down. This preserves indexed data; add -v only when intentionally deleting lab volumes.",
]:
    bullet(line)

doc.add_paragraph("Screenshot Evidence", style="Heading 1")
doc.add_paragraph("The evidence sequence includes supplied screenshots of Docker services, Wazuh's alert search and built-in overview, and all five local email alerts. The saved standalone Kibana dashboard filters the same five rule IDs. The companion visual below summarizes the verified Elasticsearch panel results: one document for each rule and a severity split of two level-8 and three level-10 alerts.")
add_figure("incoming/image1.png", "Figure 4. Earlier Wazuh Threat Hunting capture showing four matching event rows (rules 100502–100505); it predates the verified five-alert replay.")
add_figure("mailpit-five-alerts.png", "Figure 5. Mailpit inbox showing five local alert notification messages.")
add_figure("docker-running.png", "Figure 6. Supplied Docker Desktop capture of the Wazuh base stack running before the standalone Elastic services were added; current Elasticsearch and Kibana container status was separately verified during this revision.")
add_figure("wazuh-dashboard-default-charts.png", "Figure 7. Supplied Wazuh overview showing built-in alert, severity, and MITRE visualizations; this is the default dashboard view.")
add_figure("wazuh-login.png", "Figure 8. Supplied Wazuh dashboard login page, documenting access to the local web interface.")
add_figure("kibana-data-visualizations.png", "Figure 9. Report visualization of live Kibana panel values after five alert documents were verified in Elasticsearch; one record appears for each rule ID.")
doc.add_paragraph("The saved Kibana dashboard applies a persistent KQL filter across all five rule IDs. The rule panel shows one record for each scenario. Severity is a separate triage view: levels 8 and 10 are counts grouped by Wazuh rule level, not a measure of attack success. The 15-minute time picker keeps the dashboard focused on recent events and refreshes automatically. Figure 9 is a report visualization of those live values, not a screenshot of the browser interface.")

doc.add_paragraph("Rubric Coverage", style="Heading 1")
table(["Assignment requirement", "Implementation and evidence"], [
    ("IDS/IPS and syslog-ng deployment", "Wazuh manager detection plus syslog-ng collector; Compose deployment and syslog configuration."),
    ("Security log collection configuration", "UDP 5514 collection and forwarding to Wazuh remote syslog on UDP 514."),
    ("Elasticsearch/Kibana log management", "Standalone Elasticsearch 8.19.25 stores each matching Wazuh alert in lab5-alerts; Kibana 8.19.25 uses a saved data view and custom dashboard. Wazuh's native OpenSearch indexer remains in parallel."),
    ("Five real-time scenarios", "Rules 100501–100505 detected five safe, synthetic events; the refreshed 15-minute dashboard query returned one hit per rule, confirmed by the manager log and inbox."),
    ("Priority log collection and justification", "Timestamp, source/destination, service, raw evidence, severity, and rule ID are retained; their triage value is mapped in a dedicated table."),
    ("Visualization and threat explanation", "Custom Kibana panel values are shown in Figure 9; scenario-count and severity charts, five threat explanations, risk context, and analyst response steps are also included."),
    ("Alerts and notifications", "Custom alert rules plus local SMTP notifications in Mailpit; optional external SMTP configuration documented."),
    ("Repository structure and installation guide", "README, config, scripts, sample logs, and docs folders with setup/reproduction steps."),
    ("Custom Kibana dashboard bonus (+5)", "Completed: saved Lab 5 Security Anomaly Dashboard in standalone Kibana, with a persistent KQL filter and custom panels for counts by rule ID and severity."),
    ("Automated notification bonus", "Notifier automatically emails each matching new alert to Mailpit."),
    ("Architecture diagram bonus (+3)", "Integrated architecture diagram in Figure 1 and implementation flow described in the report."),
    ("Additional security tool bonus (+5)", "Wazuh adds centralized rule-based analysis, alert indexing, visualization, and notifications alongside syslog-ng collection; this integration is evidenced by rules 100501–100505 and the running services."),
], [2.4, 4.0])
doc.add_paragraph("The source rubric labels GitHub Documentation as 20 points, while its listed subitems (including visualization and analysis) sum to 30 points. The assignment's four category headings total 100 points. This report covers every listed subitem and preserves the rubric wording rather than guessing how the instructor will reconcile the arithmetic.")

doc.add_paragraph("Limitations and Future Work", style="Heading 1")
doc.add_paragraph("The rules are single-event signatures designed for repeatable demonstrations. They do not aggregate authentication attempts or port connections over a time window; the replay events summarize those patterns in one synthetic message. The rules may produce false positives if used on real traffic. Mailpit captures email locally and is not an external email service. Elasticsearch and Kibana run with authentication and TLS disabled on plain HTTP for this isolated classroom lab; do not expose ports 9201 or 5601 to untrusted networks. Production use requires authentication, TLS, restricted network access, retention settings, and protected credentials.")
doc.add_paragraph("Next steps include adding time-window correlation, testing benign baselines, forwarding authenticated TLS syslog from a Linux endpoint, adding Suricata or firewall telemetry, setting retention and access policies, and enabling external SMTP delivery with protected credentials. A production deployment should use trusted certificates and replace all default credentials.")
doc.add_paragraph("Technology watch", style="Heading 2")
doc.add_paragraph("Future iterations should track Wazuh release notes and rule updates, and evaluate Suricata or Zeek telemetry for richer network context. New detections should be tested against both attack simulations and benign traffic before they are enabled on production networks.")

doc.add_paragraph("Conclusion", style="Heading 1")
doc.add_paragraph("The laboratory connects syslog-ng collection, Wazuh rule-based analysis, the Wazuh indexer, standalone Elasticsearch and Kibana, and automated local email notification. Its five scenarios are reproducible with safe synthetic events. The report records the implementation, evidence, and constraints needed to reproduce and assess the lab.")

doc.add_paragraph("References", style="Heading 1")
for ref in [
    "Wazuh documentation, Docker deployment: https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html",
    "Wazuh documentation, local configuration reference: https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/",
    "Wazuh documentation, JSON decoder and log analysis: https://documentation.wazuh.com/current/user-manual/ruleset/",
    "Official Wazuh Docker repository, release v4.14.10: https://github.com/wazuh/wazuh-docker/tree/v4.14.10",
    "Elastic documentation, Run Kibana on Docker: https://www.elastic.co/guide/en/kibana/current/docker.html",
    "Elastic documentation, Elasticsearch Docker image: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html",
]:
    bullet(ref)

doc.core_properties.title = "Lab 5 Network Anomaly Detection and Log Management"
doc.core_properties.subject = "ESIGELEC Information System Security"
doc.core_properties.author = "Phu Hoang Triet NGO"
doc.save(OUT)
print(OUT)
