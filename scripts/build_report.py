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
subtitle = doc.add_paragraph("A Wazuh and syslog-ng single-node laboratory")
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
    "This report documents a reproducible security monitoring laboratory. Five synthetic intrusion indicators travel through syslog-ng to Wazuh, where local rules raise alerts for review in the Wazuh dashboard and indexer. A local email-capture service demonstrates alert notification without sending messages to an external recipient."
)
doc.add_page_break()

doc.add_paragraph("Executive Summary", style="Heading 1")
doc.add_paragraph(
    "The lab implements a complete event path for five network-security scenarios: SSH password guessing, port reconnaissance, web path traversal, SQL injection probing, and a DNS tunneling indicator. The replay script sends labelled sample events to the syslog-ng collector; custom Wazuh decoders and rules identify them; the Wazuh manager writes JSON alerts to its indexer; the dashboard supports search and visualization; and the notifier delivers each matching alert to a local Mailpit inbox."
)
doc.add_paragraph(
    "The assignment recommends Wazuh with Elasticsearch and Kibana. This implementation uses Wazuh's supported single-node stack: its Wazuh indexer is OpenSearch based and its Wazuh dashboard supplies the search and visualization interface. The distinction is recorded here because it affects the product names in the deployment rubric."
)
table(["Deployment component", "Role in this lab"], [
    ("syslog-ng", "Receives UDP syslog events on port 5514 and forwards them to Wazuh on UDP 514."),
    ("Wazuh manager", "Reads remote syslog, decodes Lab 5 fields, applies rules 100501–100505, and writes alerts."),
    ("Wazuh indexer", "Stores searchable alert records for the dashboard."),
    ("Wazuh dashboard", "Searches, filters, and visualizes Wazuh alerts."),
    ("Alert notifier and Mailpit", "Watches new Lab 5 alerts, sends local SMTP messages, and displays them in an inbox."),
], [1.8, 4.6])

doc.add_paragraph("System Architecture", style="Heading 1")
table(["Stage", "Data flow"], [
    ("1. Event source", "scripts/replay_scenarios.py sends synthetic RFC 3164-style events to localhost UDP/5514."),
    ("2. Collection", "syslog-ng accepts the packets and forwards them to wazuh.manager UDP/514."),
    ("3. Analysis", "The Wazuh remote-syslog input and Lab 5 decoder/rules create alert records."),
    ("4. Storage and visualization", "The Wazuh manager forwards alert data to the indexer for dashboard searches and charts."),
    ("5. Notification", "The notifier filters alert rule IDs 100501–100505 and emails Mailpit on the internal Docker network."),
], [1.8, 4.6])
doc.add_paragraph("The three central Wazuh services run as a single-node Docker deployment. syslog-ng, the notifier, and Mailpit join the same Compose network. The manager accepts events only from the lab's Docker subnet, and the collector is published on the local host for replay.")
add_figure("lab5-architecture.png", "Figure 1. Integrated event path from controlled replay through detection, indexing, visualization, and local notification.")

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
doc.add_paragraph("In the Wazuh dashboard, use Threat Hunting to filter for rule.id values 100501–100505. After replaying the five scenarios again, the Last 15 minutes query returned five hits, one for each custom rule ID. The embedded dashboard capture below is from the earlier run and shows four hits; the newer query confirms that rule 100501 is now indexed as well.")
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
    "Wait for the manager, indexer, and dashboard to become ready. Open https://localhost for the Wazuh dashboard and http://localhost:8025 for Mailpit.",
    "Run python3 scripts/replay_scenarios.py to transmit one synthetic event for each scenario.",
    "Search the dashboard for rule.id values 100501–100505 and choose Last 15 minutes after replay. The verified manager log contains one hit per rule; the earlier dashboard capture shows four results and is labelled accordingly.",
    "Stop the stack with docker compose -p lab5 -f vendor/wazuh-docker/single-node/docker-compose.yml -f docker-compose.lab5.yml down. This preserves indexed data; add -v only to remove the lab data volumes.",
]:
    bullet(line)

doc.add_paragraph("Screenshot Evidence", style="Heading 1")
doc.add_paragraph("The following supplied captures document the running environment and the interface. The earlier Threat Hunting capture shows four results; it predates the verified replay represented in Figures 2 and 3. Manager logs from 17 November independently show all five custom rules. The Wazuh overview is the built-in dashboard and is included as product evidence; it is not presented as a separately saved custom dashboard.")
add_figure("wazuh-four-results-earlier.png", "Figure 4. Earlier Wazuh Threat Hunting view with four results; the subsequent verified manager log contains all five custom rule IDs.")
add_figure("mailpit-five-alerts.png", "Figure 5. Mailpit inbox showing five local alert notification messages.")
add_figure("docker-running.png", "Figure 6. Docker Desktop capture supplied with the report, showing the lab containers running.")
add_figure("wazuh-dashboard-default-charts.png", "Figure 7. Supplied Wazuh overview showing built-in alert, severity, and MITRE visualizations; this is the default dashboard view.")
add_figure("wazuh-login.png", "Figure 8. Supplied Wazuh dashboard login page, documenting access to the local web interface.")

doc.add_paragraph("Rubric Coverage", style="Heading 1")
table(["Assignment requirement", "Implementation and evidence"], [
    ("IDS/IPS and syslog-ng deployment", "Wazuh manager detection plus syslog-ng collector; Compose deployment and syslog configuration."),
    ("Security log collection configuration", "UDP 5514 collection and forwarding to Wazuh remote syslog on UDP 514."),
    ("Elasticsearch/Kibana log management", "Wazuh indexer and dashboard provide equivalent integrated search and visualization; this Wazuh release uses OpenSearch-based indexer components instead of standalone Elasticsearch/Kibana."),
    ("Five real-time scenarios", "Rules 100501–100505 detected five safe, synthetic events; the refreshed 15-minute dashboard query returned one hit per rule, confirmed by the manager log and inbox."),
    ("Priority log collection and justification", "Timestamp, source/destination, service, raw evidence, severity, and rule ID are retained; their triage value is mapped in a dedicated table."),
    ("Visualization and threat explanation", "Wazuh overview screenshot plus two charts of verified custom-event counts and five detailed threat interpretations. The earlier four-result screenshot is explicitly dated as historical."),
    ("Alerts and notifications", "Custom alert rules plus local SMTP notifications in Mailpit; optional external SMTP configuration documented."),
    ("Repository structure and installation guide", "README, config, scripts, sample logs, and docs folders with setup/reproduction steps."),
    ("Custom Kibana dashboard bonus (+5)", "Not yet demonstrated: a separate saved custom dashboard is not present. The included Wazuh screenshot is the built-in overview; the two report charts summarize verified events but do not substitute for a saved dashboard in the live interface."),
    ("Automated notification bonus", "Notifier automatically emails each matching new alert to Mailpit."),
    ("Architecture diagram bonus (+3)", "Integrated architecture diagram in Figure 1 and implementation flow described in the report."),
    ("Additional security tool bonus (+5)", "Wazuh adds centralized rule-based analysis, alert indexing, visualization, and notifications alongside syslog-ng collection; this integration is evidenced by rules 100501–100505 and the running services."),
], [2.4, 4.0])
doc.add_paragraph("The source rubric labels GitHub Documentation as 20 points, while its listed subitems (including visualization and analysis) sum to 30 points. The assignment's four category headings total 100 points. This report covers every listed subitem and preserves the rubric wording rather than guessing how the instructor will reconcile the arithmetic.")

doc.add_paragraph("Limitations and Future Work", style="Heading 1")
doc.add_paragraph("The rules are single-event signatures designed for repeatable demonstrations. They do not aggregate authentication attempts or port connections over a time window; the replay events summarize those patterns in one synthetic message. The rules may produce false positives if used on real traffic. The local Mailpit inbox demonstrates SMTP delivery but is not an external email service. The assignment names Elasticsearch and Kibana, while this implementation uses the Wazuh indexer and dashboard, which are OpenSearch-based; exact product-name compliance may affect grading. A separate custom dashboard was not saved, so the custom-dashboard bonus remains incomplete. The first dashboard capture showed four results, but a later replay and Last 15 minutes query confirmed all five IDs.")
doc.add_paragraph("Next steps include adding time-window correlation, testing benign baselines, forwarding authenticated TLS syslog from a Linux endpoint, adding Suricata or firewall telemetry, setting retention and access policies, and enabling external SMTP delivery with protected credentials. A production deployment should also use a trusted certificate and replace all default credentials.")
doc.add_paragraph("Technology watch", style="Heading 2")
doc.add_paragraph("Future iterations should track Wazuh release notes and rule updates, and evaluate Suricata or Zeek telemetry for richer network context. New detections should be tested against both attack simulations and benign traffic before they are enabled on production networks.")

doc.add_paragraph("Conclusion", style="Heading 1")
doc.add_paragraph("The laboratory design connects syslog-ng collection, Wazuh rule-based analysis, indexed alert search, dashboard visualization, and automated email notification. Its five scenarios are reproducible with safe synthetic events. The report records the implementation choices, evidence, and limits needed to reproduce and assess the lab.")

doc.add_paragraph("References", style="Heading 1")
for ref in [
    "Wazuh documentation, Docker deployment: https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html",
    "Wazuh documentation, local configuration reference: https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/",
    "Wazuh documentation, JSON decoder and log analysis: https://documentation.wazuh.com/current/user-manual/ruleset/",
    "Official Wazuh Docker repository, release v4.14.10: https://github.com/wazuh/wazuh-docker/tree/v4.14.10",
]:
    bullet(ref)

doc.core_properties.title = "Lab 5 Network Anomaly Detection and Log Management"
doc.core_properties.subject = "ESIGELEC Information System Security"
doc.core_properties.author = "Phu Hoang Triet NGO"
doc.save(OUT)
print(OUT)
