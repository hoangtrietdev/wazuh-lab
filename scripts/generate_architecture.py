from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

out = Path(__file__).resolve().parents[1] / 'evidence/lab5-architecture.png'
W, H = 2000, 1060
im = Image.new('RGB', (W, H), '#f5f8fc')
d = ImageDraw.Draw(im)
font_path = '/System/Library/Fonts/Supplemental/Arial.ttf'
font_bold = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
F_TITLE = ImageFont.truetype(font_bold, 42)
F_SUB = ImageFont.truetype(font_path, 25)
F_HEAD = ImageFont.truetype(font_bold, 25)
F_BODY = ImageFont.truetype(font_path, 21)
F_TAG = ImageFont.truetype(font_path, 17)
F_ARROW = ImageFont.truetype(font_bold, 18)

d.text((72, 48), 'LAB 5 SECURITY MONITORING ARCHITECTURE', font=F_TITLE, fill='#172f50')
d.text((74, 108), 'Five synthetic scenarios | Docker Compose | Wazuh + standalone Elasticsearch and Kibana', font=F_SUB, fill='#566a82')

def box(x, y, w, h, title, lines, footer, fill, stroke='#bdc9d8'):
    d.rounded_rectangle((x, y, x+w, y+h), radius=18, fill=fill, outline=stroke, width=3)
    d.text((x+22, y+18), title, font=F_HEAD, fill='#173b61')
    yy = y+67
    for line in lines:
        d.text((x+22, yy), line, font=F_BODY, fill='#263746')
        yy += 34
    d.text((x+22, y+h-34), footer, font=F_TAG, fill='#526b84')

def arrow(points, label, label_xy):
    d.line(points, fill='#3279bf', width=7, joint='curve')
    x1,y1=points[-2]; x2,y2=points[-1]
    if abs(x2-x1) >= abs(y2-y1):
        head=[(x2,y2),(x2-18,y2-12),(x2-18,y2+12)]
    else:
        head=[(x2,y2),(x2-12,y2-18),(x2+12,y2-18)]
    d.polygon(head, fill='#3279bf')
    d.text(label_xy, label, font=F_ARROW, fill='#345a80')

# Collection and detection path
box(65, 270, 300, 205, 'Event replay', ['5 labelled RFC 3164 events', 'one synthetic event / rule'], 'scripts/replay_scenarios.py', '#eaf2fb')
box(455, 270, 300, 205, 'Collection', ['UDP 5514 → UDP 514', 'syslog-ng relay'], 'Docker service: syslog-ng', '#e8f5f1')
box(845, 270, 330, 205, 'Detection', ['Remote syslog input', 'custom rules 100501–100505'], 'Wazuh manager', '#fff4df')
box(1270, 210, 300, 205, 'Wazuh search', ['Indexed alerts', 'native dashboard and search'], 'Wazuh indexer (OpenSearch)', '#eeeafa')
box(1650, 210, 285, 205, 'Wazuh dashboard', ['Threat Hunting', 'native alert views'], 'HTTPS :443', '#edf2fa')
arrow([(365,372),(455,372)], 'UDP 5514', (372,338))
arrow([(755,372),(845,372)], 'UDP 514', (766,338))
arrow([(1175,330),(1270,330)], 'Wazuh alerts', (1180,294))
arrow([(1570,310),(1650,310)], 'search', (1583,274))

# Enrichment and notifications
box(845, 650, 330, 200, 'Alert notifier', ['tails alerts.json', 'selects rules 100501–100505'], 'alert-notifier container', '#eaf2fb')
box(1270, 555, 300, 190, 'Elasticsearch', ['index: lab5-alerts', 'alert JSON + timestamp'], '8.19.25 | host :9201', '#e8f5f1')
box(1650, 555, 285, 190, 'Custom Kibana', ['saved dashboard', 'counts by rule + severity'], '8.19.25 | host :5601', '#eeeafa')
box(1270, 805, 300, 170, 'Mailpit inbox', ['one local email per alert', 'rule, severity, raw event'], 'SMTP :1025 | web :8025', '#fcefee')
arrow([(1010,475),(1010,650)], 'alerts.json', (1025,540))
arrow([(1175,700),(1220,700),(1220,650),(1270,650)], 'HTTP POST', (1190,665))
arrow([(1570,650),(1650,650)], 'data view', (1584,615))
arrow([(1175,775),(1220,775),(1220,890),(1270,890)], 'SMTP', (1180,838))

d.text((70, 1000), 'Observed replay: 5/5 rules fired. Synthetic indicators use documentation IPs and reserved test domains.', font=F_SUB, fill='#294b70')
im.save(out, optimize=True)
print(out)
