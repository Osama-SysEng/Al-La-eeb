import argparse, json, re
from pathlib import Path
P={'private_key':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),'aws_access_key':re.compile(r'AKIA[0-9A-Z]{16}'),'quoted_secret':re.compile(r'(?:secret|password|token|api[_-]?key)\s*[:=]\s*[\'\"][^\'\"\s]{12,}[\'\"]',re.I)}; I={'.git','.venv','venv','node_modules','__pycache__','reports','build','dist'}
def main():
 a=argparse.ArgumentParser();a.add_argument('--root',default='.');a.add_argument('--output',required=True);x=a.parse_args();r=Path(x.root).resolve();f=[]
 for p in r.rglob('*'):
  if not p.is_file() or any(q in I for q in p.parts) or p.name.startswith('.env') or p.stat().st_size>1_000_000:continue
  try:lines=p.read_text(encoding='utf-8').splitlines()
  except UnicodeDecodeError:continue
  for n,line in enumerate(lines,1):
   for k,v in P.items():
    if v.search(line):f.append({'rule':k,'file':str(p.relative_to(r)),'line':n})
 o=Path(x.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps({'scanner':'local_secret_heuristic','findings':f},indent=2),encoding='utf-8');print(json.dumps({'findings':len(f)}));raise SystemExit(1 if f else 0)
if __name__=='__main__':main()
