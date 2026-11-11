#!/usr/bin/env python3
"""Collect actual Cape Jaffa station observations. Never substitute forecasts."""
import datetime as dt
import json
import pathlib
import urllib.error
import urllib.request

URLS = [
    'https://www.bom.gov.au/fwo/IDS60801/IDS60801.94813.json',
    'https://reg.bom.gov.au/fwo/IDS60801/IDS60801.94813.json',
]
DEST = pathlib.Path('data/cape-jaffa-observations.json')
UTC = dt.timezone.utc

def number(v):
    try:
        x = float(v)
        return x if x == x and abs(x) < 1e6 else None
    except (ValueError, TypeError):
        return None

def fetch():
    failures = []
    for url in URLS:
        try:
            req = urllib.request.Request(url, headers={'Accept':'application/json', 'User-Agent':'CapeJaffaWindObservationCollector/1.1'})
            with urllib.request.urlopen(req, timeout=25) as resp:
                payload = json.load(resp)
            return payload, url
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
            failures.append(f'{url}: {e}')
    raise RuntimeError('No authorised BOM feed responded. Do not treat forecast values as observations. ' + ' | '.join(failures))

def main():
    payload, url = fetch()
    rows = payload.get('observations', {}).get('data', [])
    if not isinstance(rows, list) or not rows:
        raise RuntimeError('BOM response contains no observation rows')
    now = dt.datetime.now(UTC)
    collected = {}
    for row in rows:
        stamp = str(row.get('aifstime_utc') or '')
        if len(stamp) != 14 or not stamp.isdigit():
            continue
        t = dt.datetime.strptime(stamp, '%Y%m%d%H%M%S').replace(tzinfo=UTC)
        if not now - dt.timedelta(days=7) <= t <= now + dt.timedelta(minutes=15):
            continue
        speed = number(row.get('wind_spd_kt'))
        if speed is None or not 0 <= speed <= 150:
            continue
        record = {'time_utc':t.isoformat(timespec='seconds').replace('+00:00','Z'),
                  'wind_kn':speed,'gust_kn':number(row.get('gust_kt')),
                  'direction':row.get('wind_dir'),
                  'pressure_hpa':number(row.get('press_msl')) or number(row.get('press_qnh'))}
        collected[record['time_utc']] = record
    if not collected:
        raise RuntimeError('No valid measured wind readings in response')
    latest = max(collected)
    if now - dt.datetime.fromisoformat(latest.replace('Z','+00:00')) > dt.timedelta(hours=4):
        raise RuntimeError(f'Latest BOM observation {latest} is stale (>4 hours)')
    previous = []
    if DEST.exists():
        try:
            previous = json.loads(DEST.read_text()).get('observations', [])
        except (ValueError, OSError):
            pass
    cutoff = now - dt.timedelta(days=90)
    merged = {x['time_utc']:x for x in previous if isinstance(x, dict) and x.get('time_utc')}
    merged.update(collected)
    merged = {k:v for k,v in merged.items() if dt.datetime.fromisoformat(k.replace('Z','+00:00')) >= cutoff}
    result = {'station_id':'026095','station_name':'Cape Jaffa (The Limestone)',
              'source':url,'collected_at_utc':now.isoformat(timespec='seconds').replace('+00:00','Z'),
              'observations':[merged[k] for k in sorted(merged)]}
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(json.dumps(result, indent=2)+'\n')
    print(f'Saved {len(merged)} measured observations; newest {latest}')

if __name__ == '__main__':
    main()
