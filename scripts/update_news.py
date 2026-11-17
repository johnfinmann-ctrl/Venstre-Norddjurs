"""Daily, free Google News RSS discovery of public Din Avis links.

Keeps publisher articles at their original location. Only metadata is stored.
A mention is categorized as coverage, not authorship. Verified authored pieces must be added manually with author and authorshipVerified=true.
Google News indexing is not exhaustive; there is no promise of full coverage.
"""
from __future__ import annotations
import datetime as dt
import email.utils
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'articles.json'
SINCE = dt.date(2025, 6, 1)
PEOPLE = {
    'Kasper Juncher Bjerregaard': ['kasper bjerregaard', 'kasper juncher bjerregaard'],
    'Benno Blæsild': ['benno blæsild', 'benno blaesild'],
    'Niels Ole Birk': ['niels ole birk'],
    'Rikke Albæk Jørgensen': ['rikke albæk', 'rikke albaek'],
    'Peter Poulsen': ['peter poulsen', 'peter arler poulsen'],
    'Agnete Brandt Grann': ['agnete brandt grann'],
    'Michael Bengtson': ['michael bengtson'],
    'Søren Kejser': ['søren kejser'],
}
QUERIES = [
    'site:dinavis.dk "Norddjurs" "Venstre"',
    'site:dinavis.dk "Kasper Bjerregaard"',
    'site:dinavis.dk "Rikke Albæk"',
    'site:dinavis.dk "Benno Blæsild"',
    'site:dinavis.dk "Niels Ole Birk"',
    'site:dinavis.dk "Agnete Brandt Grann"',
    'site:dinavis.dk "Michael Bengtson"',
    'site:dinavis.dk "Søren Kejser"',
    'site:dinavis.dk "Peter Poulsen" "Norddjurs"',
]

def get_feed(query: str) -> ET.Element:
    qs = urllib.parse.urlencode({'q': query + ' after:2025-05-31', 'hl': 'da', 'gl': 'DK', 'ceid': 'DK:da'})
    req = urllib.request.Request('https://news.google.com/rss/search?' + qs,
                                 headers={'User-Agent':'Mozilla/5.0 (compatible; venstre-norddjurs-news/1.0)'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return ET.fromstring(r.read(2_000_000))

def members_in(text: str) -> list[str]:
    low = text.casefold()
    return [name for name, variants in PEOPLE.items() if any(v in low for v in variants)]

def main() -> None:
    data = json.loads(OUT.read_text(encoding='utf-8'))
    rows = data.get('articles', [])
    seen = {(r.get('title','').casefold(), r.get('date','')) for r in rows}
    additions = 0
    for q in QUERIES:
        try:
            feed = get_feed(q)
        except Exception as exc:
            print('Feed unavailable:', q, exc)
            continue
        for item in feed.findall('./channel/item'):
            title = (item.findtext('title') or '').strip()
            url = (item.findtext('link') or '').strip()
            source = item.find('source')
            source_name = (source.text or '').strip() if source is not None else ''
            source_url = source.attrib.get('url','') if source is not None else ''
            try:
                day = email.utils.parsedate_to_datetime(item.findtext('pubDate') or '').date()
            except Exception:
                continue
            if not SINCE <= day <= dt.date.today() or not url.startswith('https://'):
                continue
            # Restrict source to Din Avis, rather than treating every match as publisher content.
            if 'dinavis.dk' not in source_url.casefold() and 'din avis' not in source_name.casefold():
                continue
            clean = re.sub(r'\s+-\s+(Din Avis|Dinavis).*$', '', title, flags=re.I).strip()
            names = members_in(clean)
            local_context = any(t in clean.casefold() for t in ('norddjurs', 'grenaa', 'venstre'))
            if not names and not local_context:
                continue
            key = (clean.casefold(), day.isoformat())
            if key in seen:
                continue
            rows.append({'title':clean, 'date':day.isoformat(), 'source':'Din Avis',
                         'summary':'Avisomtale fundet via offentlig nyhedssøgning. Læs artiklen hos udgiveren.',
                         'url':url, 'people':names, 'authorshipVerified':False})
            seen.add(key)
            additions += 1
    if additions:
        rows.sort(key=lambda row: row.get('date',''), reverse=True)
        data['articles'] = rows[:300]
        data['updated'] = dt.date.today().strftime('%d-%m-%Y')
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'Added {additions}; currently {len(rows)} articles')

if __name__ == '__main__':
    main()
