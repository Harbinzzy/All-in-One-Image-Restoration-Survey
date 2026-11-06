#!/usr/bin/env python3
"""Validate shared benchmark data and render its five README tables.

python scripts/sync_catalog.py --import-papers
python scripts/sync_catalog.py --site ../Harbinzzy.github.io/projects/aioir
python scripts/sync_catalog.py --check

Edit data/catalog.json to add verified results. Paper metadata is imported from
the year-grouped README paper list only when --import-papers is requested.
The project website reads the public JSON and keeps a local fallback snapshot.
No third-party dependencies are required.
"""
from pathlib import Path
from html import unescape
import argparse, json, math, re, sys

ROOT=Path(__file__).resolve().parents[1]
HEADINGS=[
 'Performance Comparisons of AiOIR Models on Three Challenging Datasets',
 'Performance Comparisons of AiOIR Models on Five Challenging Datasets',
 'Performance Comparisons of AiOIR Models on All-Weather Datasets',
 'Performance Comparisons of AiOIR Models on Real-World Weather-Related Datasets',
 'Performance Comparisons of AiOIR Models on CDD-11 Datasets'
]

def text(s):return unescape(re.sub('<[^>]*>','',s)).strip()
def normalize(s):return re.sub('[^a-z0-9]','',s.lower())
def find_url(s):
    m=re.search(r'\]\((https?://[^)]+)\)',s)
    return m[1] if m else ''
def import_papers(readme):
    papers=[];year=0
    for line in readme.split('## 📊')[0].splitlines():
        if re.fullmatch(r'### 20\d\d',line):year=int(line[4:])
        if not year or not line.startswith('|') or '<sub>' not in line:continue
        cells=[s.strip() for s in line.strip('|').split('|')]
        title=text(re.split(r'<br\s*/?>',cells[0])[0])
        authors=text(re.search(r'<sub>(.*?)</sub>',cells[0])[1])
        if any(normalize(p['title'])==normalize(title) for p in papers):continue
        papers.append(dict(title=title,authors=authors,venue=text(cells[1]),year=year,paper=find_url(cells[2]),code=find_url(cells[3])))
    return papers

def validate(data):
    assert data['schemaVersion']==1
    assert len(data['benchmarks'])==5
    ids=set()
    for g in data['benchmarks']:
        for r in g['rows']:
            assert r['id'] not in ids, r['id'];ids.add(r['id'])
            assert r['method'] and r['source'].startswith('https://')
            if g.get('tracks'):assert r['track'] in [t['id'] for t in g['tracks']]
            for c in g['columns']:
                pair=r['scores'][c['id']]
                assert len(pair) in [2,3]
                assert all(isinstance(v,(int,float)) and math.isfinite(v) for v in pair)
                assert pair[0]>0 and 0<=pair[1]<=1
                if len(pair)==3:assert pair[2]>=0
    assert data['paperCount']==len(data['papers'])
    return len(ids)

def pair(v):
    # Preserve 4-digit SSIM precision where the source provides it.
    ss=f'{v[1]:.4f}' if abs(v[1]*1000-round(v[1]*1000))>1e-6 else f'{v[1]:.3f}'
    return f'{v[0]:.2f}/{ss}'
def source(r):return f"[{r['sourceLabel']}]({r['source']})"+(' **NEW**' if r['added'] else (' †' if r.get('corrected') else ''))
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(str(c).replace('|','&#124;') for c in row)+' |' for row in rows])

def render_group(g,index):
    introduction=f"Metrics are PSNR (dB) / SSIM, higher is better. Updated **{data['updated']}**. Results are source-reported, not independently re-evaluated. **NEW** marks newly added rows. [Protocol and source notes](data/SOURCES.md).\n\n"
    if index in [0,1]:
        headers=['Category','Method','Venue & Year','Params']+[c['label'] for c in g['columns']]+['Approach','Source']
        rows=[[r['category'],r['method'],r['venue'],r['params']]+[pair(r['scores'][c['id']]) for c in g['columns']]+[r['approach'],source(r)] for r in g['rows']]
        result=introduction+table(headers,rows)
        if index==1:result+='\n\n† InstructIR-5D SOTS and Rain100L columns were swapped in the previous table; corrected from the original paper, Table 2. BSD68 denoising uses σ = 25.'
    elif index==2:
        headers=['Method']+[c['label'] for c in g['columns']]+['Params','Source']
        rows=[[r['method']]+[pair(r['scores'][c['id']]) for c in g['columns']]+[r['params'],source(r)] for r in g['rows']]
        result=introduction+table(headers,rows)+'\n\n*DCMPC-Net and WeatherRemover averages are arithmetic means over the three displayed datasets, computed here. WeatherRemover uses the **Multi Weather** results from Tables I–III. DCMPC-Net’s original four-dataset average is not used. DCMPC-Net parameter count excludes its vision-language and text encoders. Training mixtures differ; see source notes.*'
    elif index==3:
        result=introduction+'These tracks use different datasets / settings and must be compared separately.\n'
        for track in g['tracks']:
            rows=[r for r in g['rows'] if r['track']==track['id']]
            result+='\n#### '+track['label'].replace(' · new','')+'\n\n'
            if track['id']=='weatherbench':
                result+='Each cell reports **PSNR / SSIM / LPIPS** (LPIPS: lower is better). All values below are from ClusIR Table 5, including reproduced baselines.\n\n'
                values=[[r['method']]+['/'.join([f'{v[0]:.2f}',f'{v[1]:.3f}',f'{v[2]:.3f}']) for c in g['columns'] for v in [r['scores'][c['id']]]]+[source(r)] for r in rows]
                result+=table(['Method']+[c['label'] for c in g['columns']]+['Source'],values)+'\n'
            else:
                values=[[r['method']]+[pair(r['scores'][c['id']]) for c in g['columns']]+[r['params'],source(r)] for r in rows]
                result+=table(['Method']+[c['label'] for c in g['columns']]+['Params','Source'],values)+'\n'
    else:
        result=introduction+table(['Type','Method','Venue & Year','PSNR ↑','SSIM ↑','Params','Source'],[[r['category'],r['method'],r['venue'],f"{r['scores']['avg'][0]:.2f}",f"{r['scores']['avg'][1]:.3f}",r['params'],source(r)] for r in g['rows']])
    return result.strip()+'\n\n'

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check',action='store_true',help='validate and fail if generated tables or snapshot differ')
parser.add_argument('--import-papers',action='store_true',help='refresh paper metadata from the README year tables')
parser.add_argument('--site',type=Path,help='optional aioir page directory for the local JS snapshot')
args=parser.parse_args()
readme=(ROOT/'README.md').read_text(encoding='utf8')
data=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf8'))
if args.import_papers:
    data['papers']=import_papers(readme);data['paperCount']=len(data['papers'])
count=validate(data)
rendered=readme
for i,(g,heading) in enumerate(zip(data['benchmarks'],HEADINGS)):
    pattern=r'(### '+re.escape(heading)+r'\s*\n).*?(?=\n### |\n## |\Z)'
    rendered,n=re.subn(pattern,lambda m:'### '+heading+'\n\n'+render_group(g,i),rendered,flags=re.S)
    assert n==1,heading
snapshot='window.AIOIR_CATALOG = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n'
if args.check:
    if readme!=rendered:sys.exit('README benchmark tables differ; run scripts/sync_catalog.py')
    if args.site and (args.site/'catalog.js').read_text(encoding='utf8')!=snapshot:sys.exit('Website fallback differs; run sync with --site')
else:
    (ROOT/'data/catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (ROOT/'README.md').write_text(rendered,encoding='utf8')
    if args.site:
        assert args.site.is_dir(),args.site
        (args.site/'catalog.js').write_text(snapshot,encoding='utf8')
print(f"Validated {len(data['papers'])} papers and {count} results across 5 benchmark families.")
