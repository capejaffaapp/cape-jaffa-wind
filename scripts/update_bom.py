#!/usr/bin/env python3
"""Collect real measured Cape Jaffa wind readings from the BOM public JSON feed.
Never fabricates observations. On a fetch failure, exits nonzero and retains existing archive.
"""
import datetime as dt
import json
import pathlib
import urllib.request

URL='https://www.bom.gov.au/fwo/IDS60801/IDS60801.94813.json'
DEST=pathlib.Path('data/cape-jaffa-observations.json')
UTC=dt.timezone.utc

def num(v):
    try:
        x=float(v)
        return x if x==x and abs(x)<1e6 else None
    except (TypeError, ValueError): return None

def parse_time(row):
    # BOM aifstime_utc is YYYYMMDDHHMMSS, in UTC.
    raw=str(row.get('aifstime_utc') or '')
    if len(raw)==14 and raw.isdigit():
        return dt.datetime.strptime(raw,'%Y%m%d%H%M%S').replace(tzinfo=UTC)
    raise ValueError('No valid UTC observation timestamp')

def main():
    req=urllib.request.Request(URL,headers={'User-Agent':'CapeJaffaMarineWeather/1.0 (GitHub Pages weather tracker)','Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as response:
        data=json.load(response)
    rows=data.get('observations',{}).get('data',[])
    if not isinstance(rows,list) or not rows:raise RuntimeError('BOM returned no observations')
    new={}
    now=dt.datetime.now(UTC)
    for row in rows:
        try:t=parse_time(row)
        except ValueError:continue
        if t>now+dt.timedelta(minutes=15) or t<now-dt.timedelta(days=7):continue
        # BOM wind_spd_kt and gust_kt are direct measured station readings.
        wind=num(row.get('wind_spd_kt'))
        if wind is None or not 0<=wind<=150:continue
        gust=num(row.get('gust_kt'))
        pressure=num(row.get('press_msl'))
        if pressure is None:pressure=num(row.get('press_qnh'))
        record={'time_utc':t.isoformat(timespec='seconds').replace('+00:00','Z'),
                'wind_kn':wind,'gust_kn':gust,'direction':row.get('wind_dir'),
                'pressure_hpa':pressure}
        new[record['time_utc']]=record
    if not new:raise RuntimeError('No valid BOM measured wind readings')
    previous=[]
    if DEST.exists():
        try:previous=json.loads(DEST.read_text()).get('observations',[])
        except (ValueError, OSError):pass
    cutoff=now-dt.timedelta(days=90)
    merged={x['time_utc']:x for x in previous if isinstance(x,dict) and 'time_utc' in x}
    merged.update(new)
    merged={k:v for k,v in merged.items() if dt.datetime.fromisoformat(k.replace('Z','+00:00'))>=cutoff}
    latest=max(new)
    if now-dt.datetime.fromisoformat(latest.replace('Z','+00:00'))>dt.timedelta(hours=4):
        raise RuntimeError('BOM feed appears stale; refusing to publish new archive')
    payload={'station_id':'026095','station_name':'Cape Jaffa (The Limestone)',
             'source':URL,'collected_at_utc':now.isoformat(timespec='seconds').replace('+00:00','Z'),
             'observations':[merged[k] for k in sorted(merged)]}
    DEST.parent.mkdir(parents=True,exist_ok=True)
    DEST.write_text(json.dumps(payload,indent=2)+'\n')
    print(f'Saved {len(merged)} actual observations; newest {latest}')
if __name__=='__main__':main()
