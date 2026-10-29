"""Validate PR JSON as data, using only code checked out from the trusted base."""
import json, os, urllib.request
from validate import validate

def api(path):
    request=urllib.request.Request('https://api.github.com/'+path, headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'], 'Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(request, timeout=30) as response: return json.load(response)

repo=os.environ['REPO'];number=os.environ['PR_NUMBER'];files=[]
for page in range(1,32):
    batch=api(f'repos/{repo}/pulls/{number}/files?per_page=100&page={page}')
    files.extend(batch)
    if len(batch)<100: break
else: raise ValueError('Too many changed files')
checked=0
for item in files:
    name=item['filename']
    if not (name.startswith('submissions/') and name.endswith('.json')) or item['status']=='removed': continue
    blob=api(f'repos/{repo}/git/blobs/{item["sha"]}')
    if blob.get('encoding')!='base64' or blob.get('size',0)>5_000_000: raise ValueError('Invalid or oversized answer file')
    import base64
    submission=json.loads(base64.b64decode(blob['content']))
    validate(submission);checked+=1
    print('Valid submission:',name)
print('Validated answer files:',checked)
