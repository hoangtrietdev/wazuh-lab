"""Render an explanatory summary of the verified Kibana panel values."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

out=Path(__file__).resolve().parents[1]/'evidence/kibana-data-visualizations.png'
W,H=1800,900
im=Image.new('RGB',(W,H),'#f4f6f8'); d=ImageDraw.Draw(im)
font='/System/Library/Fonts/Supplemental/Arial.ttf'; bold='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
F0=ImageFont.truetype(bold,36); F1=ImageFont.truetype(bold,26); F2=ImageFont.truetype(font,21); F3=ImageFont.truetype(font,18)
d.rectangle((0,0,W,78),fill='#17212c'); d.text((38,20),'Elastic  |  Lab 5 Security Anomaly Dashboard',font=F1,fill='white')
d.text((42,105),'Saved KQL filter: rule.id: (100501 OR 100502 OR 100503 OR 100504 OR 100505)',font=F2,fill='#273746')
d.text((42,141),'Time range: Last 15 minutes  •  Data view: Lab 5 Security Alerts  •  Indexed documents: 5',font=F3,fill='#526273')
# Cards
cards=[(40,205,860,820),(930,205,1760,820)]
for c in cards:d.rounded_rectangle(c,radius=14,fill='white',outline='#cbd5df',width=2)
d.text((70,230),'Lab 5 alerts by rule ID',font=F1,fill='#263746')
d.text((960,230),'Lab 5 alerts by severity',font=F1,fill='#263746')
# Bar chart
x0,y0,x1,y1=135,330,820,700
d.line((x0,y0,x0,y1,x1,y1),fill='#8593a1',width=2)
for i in range(6):
 y=y1-(y1-y0)*i/5; d.line((x0,y,x1,y),fill='#e4e9ee',width=1); d.text((96,y-12),str(i/5),font=F3,fill='#697684')
ids=['100501','100502','100503','100504','100505']; col='#54b399'
step=(x1-x0)/len(ids); bw=66
for i,rid in enumerate(ids):
 cx=x0+step*(i+.5); top=y1-(y1-y0)*1
 d.rounded_rectangle((cx-bw/2,top,cx+bw/2,y1),radius=5,fill=col)
 d.text((cx-32,y1+18),rid,font=F3,fill='#44515e')
d.text((110,760),'Count of records',font=F3,fill='#526273'); d.text((390,760),'Exactly one alert for each custom rule',font=F2,fill='#263746')
# Severity donut 2 and 3
cx,cy=1340,510; r=220; start=-90
for val,color in [(2,'#6092c0'),(3,'#54b399')]:
 extent=360*val/5; d.pieslice((cx-r,cy-r,cx+r,cy+r),start,start+extent,fill=color); start+=extent
d.ellipse((cx-112,cy-112,cx+112,cy+112),fill='white')
d.text((cx-65,cy-36),'5 alerts',font=F1,fill='#263746')
d.text((cx-70,cy+5),'100% matched',font=F3,fill='#526273')
d.ellipse((1020,760,1042,782),fill='#6092c0'); d.text((1055,756),'Level 8  •  2 alerts  •  40%',font=F2,fill='#263746')
d.ellipse((1400,760,1422,782),fill='#54b399'); d.text((1435,756),'Level 10  •  3  •  60%',font=F2,fill='#263746')
d.text((42,858),'Panel values verified against Elasticsearch lab5-alerts after the five-scenario replay. This is a report visualization of the live Kibana results.',font=F3,fill='#526273')
im.save(out,optimize=True)
print(out)
