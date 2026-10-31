"""Render a documentation figure from explicit illustrative geometry. No flight/planner implementation."""
import json
from pathlib import Path
from html import escape
P=Path(__file__).resolve().parent
D=json.loads((P/'path-geometry.json').read_text())
W,H=1000,930
# Screen x is East; screen y decreases with North.
def xy(v):
 n,e,_=v
 return 360+14*e,740-14*n
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
'<title id="title">Illustrative coordinate mission and obstacle detour</title>',
'<desc id="desc">Top-down local map. Start North zero East zero, goal North forty East zero. A central obstacle blocks the direct line. An illustrative route passes west via North ten East minus nine and North thirty East minus nine. This is not observed ArduPilot output.</desc>',
'<rect width="1000" height="930" fill="#fff"/>',
'<g font-family="Arial, sans-serif" fill="#17202a">',
'<text x="40" y="45" font-size="25" font-weight="bold">One destination; an obstacle changes the route</text>',
'<text x="40" y="73" font-size="16">Illustrative geometry only · fixed Down = −8 m relative to the EKF origin</text>']
for n in range(0,41,10):
 y=740-14*n
 parts += [f'<path d="M150 {y}H570" stroke="#dce3e9"/>',f'<text x="125" y="{y+5}" font-size="14" text-anchor="end">{n}</text>']
for e in range(-10,11,5):
 x=360+14*e
 parts += [f'<path d="M{x} 110V810" stroke="#dce3e9"/>',f'<text x="{x}" y="837" font-size="14" text-anchor="middle">{e}</text>']
parts += ['<rect x="164" y="152" width="392" height="616" rx="2" fill="none" stroke="#64748b" stroke-dasharray="7 5"/>',
'<text x="360" y="869" font-size="17" text-anchor="middle">East (m) →</text>',
'<text x="54" y="450" transform="rotate(-90 54 450)" font-size="17">North (m) →</text>']
b=D['obstacle_rectangle'];m=D['illustrative_exclusion_expansion_m'];n0,n1=b['north_m'];e0,e1=b['east_m']
parts += [f'<rect x="{360+14*(e0-m)}" y="{740-14*(n1+m)}" width="{14*(e1-e0+2*m)}" height="{14*(n1-n0+2*m)}" fill="#fff2da" stroke="#b36b00" stroke-dasharray="6 4"/>',
f'<rect x="{360+14*e0}" y="{740-14*n1}" width="{14*(e1-e0)}" height="{14*(n1-n0)}" fill="#526171"/>',
'<text x="360" y="455" font-size="16" text-anchor="middle" fill="#fff">Obstacle</text>']
x0,y0=xy(D['start_ned_m']);x1,y1=xy(D['goal_ned_m'])
parts += [f'<path d="M{x0} {y0}L{x1} {y1}" stroke="#a82626" stroke-width="3" stroke-dasharray="8 5" fill="none"/>']
pts=' '.join(f'{x},{y}' for x,y in map(xy,D['illustrative_route_ned_m']))
parts += [f'<polyline points="{pts}" fill="none" stroke="#006b78" stroke-width="5" stroke-linejoin="round"/>']
for i,v in enumerate(D['illustrative_route_ned_m']):
 x,y=xy(v);label=['Start (0, 0)','P1 (10, −9)','P2 (30, −9)','Goal (40, 0)'][i]
 label_x = x-13 if i == 2 else x+13
 anchor = 'end' if i == 2 else 'start'
 parts += [f'<circle cx="{x}" cy="{y}" r="7" fill="#006b78" stroke="#fff" stroke-width="2"/>',f'<text x="{label_x}" y="{y-12}" text-anchor="{anchor}" font-size="16">{escape(label)}</text>']
for y,label in [(190,'Mission supplies the final goal'),(220,'[North 40, East 0, Down −8] m'),(300,'Red: direct route is blocked'),(350,'Amber: expanded exclusion region'),(400,'Teal: one possible detour'),(460,'P1 and P2 are route references,'),(485,'not separate user instructions.'),(560,'Navigation adds timing and limits.'),(585,'Controllers calculate motor outputs.'),(650,'New observations can change'),(675,'or invalidate the route.')]:
 parts.append(f'<text x="600" y="{y}" font-size="16">{escape(label)}</text>')
parts += ['<text x="40" y="909" font-size="14">Coordinates shown as (North, East). No planner run, SITL flight, clearance qualification or performance result is claimed.</text>','</g></svg>']
(P/'coordinate-mission-path.svg').write_text('\n'.join(parts))
print(P/'coordinate-mission-path.svg')
