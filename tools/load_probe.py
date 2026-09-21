import argparse, concurrent.futures, json, time
from pathlib import Path
from urllib.parse import urlparse
import httpx
def safety(url,remote):
 if urlparse(url).hostname not in {'localhost','127.0.0.1','::1'} and not remote:raise ValueError('Remote target requires --allow-remote and an approved staging window')
def one(base,path):
 s=time.perf_counter()
 try:r=httpx.get(base.rstrip('/')+path,timeout=10);return {'status':r.status_code,'latency_ms':round((time.perf_counter()-s)*1000,2)}
 except httpx.HTTPError as e:return {'status':0,'latency_ms':round((time.perf_counter()-s)*1000,2),'error':type(e).__name__}
def main():
 p=argparse.ArgumentParser();p.add_argument('--base-url',default='http://localhost:8002');p.add_argument('--path',default='/health');p.add_argument('--requests',type=int,default=20);p.add_argument('--concurrency',type=int,default=4);p.add_argument('--allow-remote',action='store_true');p.add_argument('--output',default='reports/load/latest.json');a=p.parse_args();safety(a.base_url,a.allow_remote)
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.concurrency) as e:rows=list(e.map(lambda _:one(a.base_url,a.path),range(a.requests)))
 l=sorted(x['latency_ms'] for x in rows);q=lambda p:l[min(len(l)-1,max(0,int(len(l)*p+.999)-1))];out={'target':a.base_url,'summary':{'requests':len(rows),'success_rate':round(sum(200<=x['status']<400 for x in rows)/len(rows),4),'p50_ms':q(.5),'p95_ms':q(.95),'p99_ms':q(.99)}};o=Path(a.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out['summary'],indent=2))
if __name__=='__main__':main()
