"""Validate public questions and answer submissions. SPDX-License-Identifier: MIT"""
import argparse, hashlib, json
from pathlib import Path
DATA = Path(__file__).resolve().parent.parent / 'data'

def validate(submission=None):
    manifest=json.loads((DATA/'manifest.json').read_text())
    questions=json.loads((DATA/'questions.json').read_text())
    for name,digest in manifest['files'].items():
        if hashlib.sha256((DATA/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Checksum mismatch: '+name)
    ids=[q['problem_id'] for q in questions]
    if len(ids)!=manifest['n_questions'] or len(set(ids))!=len(ids):
        raise ValueError('Question count or duplicate ID')
    for q in questions:
        if set(q)!={'problem_id','problem','domain','question_format'} or set(q['problem'])!={'context','question','choices'}:
            raise ValueError('Unexpected question fields')
        if q['question_format']!='OQ' or not (q['problem'].get('question') or q['problem'].get('context')):
            raise ValueError('Invalid question')
    if submission is not None:
        if submission.get('dataset_version')!=manifest['version'] or submission.get('dataset_sha256')!=manifest['dataset_sha256']:
            raise ValueError('Dataset version/hash mismatch')
        if submission.get('questions_sha256',manifest['files']['questions.json'])!=manifest['files']['questions.json']:
            raise ValueError('Questions hash mismatch')
        model=submission.get('model_id')
        if not isinstance(model,str) or not model.strip() or len(model)>200:
            raise ValueError('Invalid model ID')
        rows=submission.get('predictions')
        if not isinstance(rows,list): raise ValueError('predictions must be an array')
        seen=set()
        for row in rows:
            if not isinstance(row,dict): raise ValueError('Invalid prediction')
            pid,answer=row.get('problem_id'),row.get('model_answer')
            if pid not in ids or pid in seen: raise ValueError('Unknown/duplicate ID')
            if not isinstance(answer,str) or not answer.strip() or len(answer)>40000: raise ValueError('Empty/invalid answer')
            seen.add(pid)
        if seen!=set(ids): raise ValueError('Incomplete answers')
    return len(ids)

def main():
    p=argparse.ArgumentParser();p.add_argument('--submission',type=Path);args=p.parse_args()
    count=validate(json.loads(args.submission.read_text()) if args.submission else None)
    print(f'Valid: {count} public questions'+(' and complete submission' if args.submission else ''))

if __name__=='__main__': main()
