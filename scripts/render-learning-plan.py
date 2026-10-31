"""Render local planning documents from the registry. Does not execute a phase."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'docs/phases/registry.json'
DATA = json.loads(REGISTRY.read_text())
PHASES = DATA['learning_phases']
GROUPS = {g['id']: g for g in DATA['learning_groups']}
INDEX = {p['id']: p for p in PHASES}
if len(INDEX) != len(PHASES):
    raise ValueError('Duplicate learning phase IDs')
for p in PHASES:
    if not re.fullmatch(r'[A-Z][0-9]{2}', p['id']) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', p['slug']):
        raise ValueError('Nonportable phase ID or slug')
    if p['group'] not in GROUPS or any(dep not in INDEX for dep in p['depends_on']):
        raise ValueError(f"Unknown group/dependency for {p['id']}")

def filename(p):
    return p['id'].lower() + '-' + p['slug'] + '.md'

def link(p, base=''):
    return f"[{p['id']}]({base}{filename(p)})"

def bullets(items):
    return '\n'.join('- ' + text for text in items)

def render(template, values):
    def replace(match):
        key = match.group(1)
        if key not in values:
            raise ValueError(f'Unknown template field {key}')
        return str(values[key])
    return re.sub(r'\n{3,}', '\n\n', re.sub(r'{{([A-Z_]+)}}', replace, template))

card_template = (ROOT / 'docs/phases/learning-phase.template.md').read_text()
output = ROOT / 'docs/phases/learning'
output.mkdir(parents=True, exist_ok=True)
for n, p in enumerate(PHASES):
    g = GROUPS[p['group']]
    deps = ', '.join(link(INDEX[x]) for x in p['depends_on']) or 'none'
    next_note = 'Return to the master plan to select the next unmet prerequisite in this track.'
    if n + 1 < len(PHASES) and PHASES[n+1]['group'] == p['group']:
        next_note = f"Next card in this group: {link(PHASES[n+1])} {PHASES[n+1]['title']}."
    values = {
        'ID': p['id'], 'TITLE': p['title'], 'STATUS': p['status'],
        'GROUP': g['id'] + ' ' + g['title'], 'TRACK': g['track'], 'DEPENDENCIES': deps,
        'PREREQUISITE': '**Additional prerequisite:** ' + p['additional_prerequisite'] if p['additional_prerequisite'] else '',
        'GOAL': p['goal'], 'CONCEPT': p['concept'], 'READ_FOCUS': bullets(p['read_focus']),
        'CHANGE_SCOPE': p['change_scope'],
        'STEPS': '\n'.join(f'{i}. {s}' for i,s in enumerate(p['steps'],1)),
        'SUCCESS': bullets(p['success']), 'EVIDENCE': bullets(p['evidence']),
        'RECORD_STATUS': '**Actual execution record:** ' + (str(p['record']) if p['record'] else ('none; this phase has not been executed.' if p['status'] == 'planned' else 'not yet linked; do not infer completion without evidence.')),
        'ROLLBACK': p['rollback'], 'TEACH_BACK': p['teach_back'], 'NEXT': next_note,
    }
    (output / filename(p)).write_text(render(card_template, values))

first = PHASES[:7]
first_table = ['| Small phase | What you do | What you learn |','| --- | --- | --- |']
for p in first:
    first_table.append(f"| {link(p, 'phases/learning/')} {p['title']} | {p['goal']} | {p['concept']} |")
sections = []
for g in DATA['learning_groups']:
    rows = [f"### {g['id']} {g['title']}", '', g['outcome'], '', f"Track: `{g['track']}`. Capability milestones: {', '.join(g['milestones']) or 'additional proposed discovery extension' }.", '', '| Small phase | Narrow result | Prerequisites |', '| --- | --- | --- |']
    for p in PHASES:
        if p['group'] != g['id']: continue
        deps = ', '.join(p['depends_on']) or 'none'
        rows.append(f"| {link(p, 'phases/learning/')} {p['title']} | {p['goal']} | {deps} |")
    sections.append('\n'.join(rows))
active = DATA.get('active_learning_phase')
if DATA.get('execution_summary'):
    implementation_status = DATA['execution_summary']
else:
    implementation_status = ('Implementation work has started according to the registry; consult each card and its actual evidence for qualified scope.'
                             if DATA['implementation_started'] else
                             'The current work is documentation only: no source checkout, tool installation, custom firmware or SITL run has been performed here.')
master_values = {'IMPLEMENTATION_STATUS': implementation_status, 'DATE':DATA['recorded_date'],'NEXT_PHASE':DATA['next_proposed_learning_phase'], 'ACTIVE_STATUS': f'Active learning phase: {active}.' if active else 'No implementation learning phase is active.', 'FIRST_PHASES':'\n'.join(first_table),'GROUP_PHASES':'\n\n'.join(sections)}
master_template = (ROOT/'docs/phases/master-learning-plan.template.md').read_text()
(ROOT/'docs/MASTER-LEARNING-PLAN.md').write_text(render(master_template, master_values))

# This is a learning workflow, not a new flight/deployment architecture.
positions = {'L01':('setup',0),'L02':('setup',1),'L03':('setup',2),'L04':('understand',2),'L05':('understand',3),'L06':('experiment',3),'L07':('arrival',3)}
labels = ['01 Get source','02 Launch SITL','03 First flight','04 Trace code','05 One goal','06 One speed','07 Observe stop']
subs = ['Source folders / pin','Stock build / disarmed','Takeoff, hold, land','Read one command path','Stock navigation','Predict and compare','Position, speed, dwell']
spec = {'schema_version':2,'diagram_type':'workflow','meta':{'title':'First seven learning phases — progress and proposed sequence','locale':'en','quality_profile':'showcase','output':'docs/phases/learning-workflow.html','legend':{'entries':{'backend':{'label':'Learning phase; see status'},'security':{'label':'Next proposed phase'}}}},'lanes':[{'id':'setup','label':'Get an unchanged simulation working'},{'id':'understand','label':'Connect the code to one movement'},{'id':'experiment','label':'Make one small change'},{'id':'arrival','label':'Explain measured stopping'}],'mainPath':[p['id'] for p in first],'nodes':[],'edges':[],'cards':[{'dot':'rose','title':'One phase, one observable result','items':[f"Next proposed learning phase: {DATA['next_proposed_learning_phase']}. Statuses and actual evidence are recorded in the registry.",'Before a change, explain the behavior and predict the result. Afterward, retain evidence and explain the difference.','L01–L04 add no custom flight behavior. L05–L07 reuse stock behavior; early learning needs no detector or application UI.']},{'dot':'emerald','title':'Then add capability in small slices','items':['Later master groups cover native mission code, instrumented sensing/avoidance, the approved operator UI and optional object goals.','Bounded search, landing and hardware have their own additional prerequisites; SkyDive stays a separate deferred branch.','The source registry, reusable card template and master plan define the detailed scopes. This diagram is a learning sequence, not implementation or UI approval.']}]}
for i,p in enumerate(first):
    lane,col=positions[p['id']]
    display_status = 'Review' if p['status'] == 'ready_for_review' else p['status']
    spec['nodes'].append({'id':p['id'],'lane':lane,'col':col,'type':'security' if p['id']==DATA['next_proposed_learning_phase'] else 'backend','label':labels[i],'sublabel':('Next proposed · ' + p['status']) if p['id']==DATA['next_proposed_learning_phase'] else (display_status + ' · ' + subs[i])})
    if i: spec['edges'].append({'from':first[i-1]['id'],'to':p['id'],'label':'Evidence retained','role':'main'})
(ROOT/'docs/phases/learning-workflow.json').write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n')
print(f'Rendered master plan, {len(PHASES)} phase cards and one editable learning workflow.')
