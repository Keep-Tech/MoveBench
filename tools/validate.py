"""Validate public questions and answer submissions. SPDX-License-Identifier: MIT"""
import argparse, hashlib, json, math, re
from datetime import date
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
        if q['question_format'] not in ('OQ','MCQ') or not (q['problem'].get('question') or q['problem'].get('context')):
            raise ValueError('Invalid question')
        if q['question_format']=='MCQ' and not q['problem'].get('choices'):
            raise ValueError('MCQ question missing choices: '+q['problem_id'])
    if submission is not None:
        if submission.get('dataset_version')!=manifest['version'] or submission.get('dataset_sha256')!=manifest['dataset_sha256']:
            raise ValueError('Dataset version/hash mismatch')
        if submission.get('questions_sha256',manifest['files']['questions.json'])!=manifest['files']['questions.json']:
            raise ValueError('Questions hash mismatch')
        model=submission.get('model_id')
        if not isinstance(model,str) or not model.strip() or len(model)>200:
            raise ValueError('Invalid model ID')
        generation=submission.get('generation')
        if not isinstance(generation,dict): raise ValueError('Missing generation metadata')
        try: date.fromisoformat(generation.get('date',''))
        except (ValueError,TypeError): raise ValueError('generation.date must be YYYY-MM-DD') from None
        temperature=generation.get('temperature')
        if isinstance(temperature,bool) or not isinstance(temperature,(int,float)) or not math.isfinite(temperature) or temperature<0:
            raise ValueError('generation.temperature must be a finite nonnegative number')
        maximum=generation.get('max_tokens')
        if isinstance(maximum,bool) or not isinstance(maximum,int) or maximum<=0:
            raise ValueError('generation.max_tokens must be a positive integer')
        by_id={q['problem_id']:q for q in questions}
        rows=submission.get('predictions')
        if not isinstance(rows,list): raise ValueError('predictions must be an array')
        seen=set()
        for row in rows:
            if not isinstance(row,dict): raise ValueError('Invalid prediction')
            pid,answer=row.get('problem_id'),row.get('model_answer')
            if pid not in ids or pid in seen: raise ValueError('Unknown/duplicate ID')
            if not isinstance(answer,str) or not answer.strip() or len(answer)>40000: raise ValueError('Empty/invalid answer')
            question=by_id[pid]
            if question['question_format']=='MCQ':
                first_line=answer.strip().splitlines()[0].strip().upper()
                if not re.fullmatch(r'[A-Z](?:\s*,\s*[A-Z])*',first_line):
                    raise ValueError('MCQ first line must contain option letters only, e.g. A or A,C: '+pid)
                letters=[x.strip() for x in first_line.split(',')]
                if len(set(letters))!=len(letters) or not set(letters)<=set(question['problem']['choices']):
                    raise ValueError('Invalid/duplicate MCQ option: '+pid)
                if '_SS' in pid and len(letters)!=1:
                    raise ValueError('Single-select answer must contain one option: '+pid)
            seen.add(pid)
        if seen!=set(ids): raise ValueError('Incomplete answers')
    return len(ids)

def main():
    p=argparse.ArgumentParser();p.add_argument('--submission',type=Path);args=p.parse_args()
    count=validate(json.loads(args.submission.read_text()) if args.submission else None)
    print(f'Valid: {count} public questions'+(' and complete submission' if args.submission else ''))

if __name__=='__main__': main()
