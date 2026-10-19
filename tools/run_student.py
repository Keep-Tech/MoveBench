"""Generate answers using questions.json only. SPDX-License-Identifier: MIT"""
import argparse
import hashlib
import json
import os
from pathlib import Path
from api_client import chat, atomic_json


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True)
    p.add_argument('--base-url', required=True)
    p.add_argument('--output', type=Path, default=Path('predictions.json'))
    p.add_argument('--temperature', type=float, default=0)
    p.add_argument('--max-tokens', type=int, default=4096)
    args = p.parse_args()
    root = Path(__file__).resolve().parent.parent / 'data'
    questions = json.loads((root / 'questions.json').read_text())
    manifest = json.loads((root / 'manifest.json').read_text())
    digest = manifest['files']['benchmark.json']
    generation = {'base_url': args.base_url, 'temperature': args.temperature, 'max_tokens': args.max_tokens}
    submission = {'schema_version': '1.0', 'dataset_version': 'release-1', 'dataset_sha256': digest,
                  'questions_sha256': hashlib.sha256((root / 'questions.json').read_bytes()).hexdigest(),
                  'model_id': args.model, 'generation': generation, 'predictions': []}
    if args.output.exists():
        old = json.loads(args.output.read_text())
        for field in ('model_id', 'dataset_sha256', 'questions_sha256', 'generation'):
            if old.get(field) != submission[field]:
                raise ValueError('Checkpoint configuration mismatch; use a new output file')
        submission = old
    done = {x['problem_id'] for x in submission['predictions']}
    key = os.environ['STUDENT_API_KEY']
    for item in questions:
        if item['problem_id'] in done:
            continue
        problem = item['problem']
        context, question = problem.get('context') or '', problem.get('question') or ''
        body = question if context == question else '\n\n'.join(x for x in (context, question) if x)
        prompt = f'你是一名专业运动健康专家。\n\n{body}\n\n请给出结构化、专业、安全的中文回答。'
        answer = chat(args.base_url, key, args.model, [{'role': 'user', 'content': prompt}],
                      args.temperature, args.max_tokens)
        submission['predictions'].append({'problem_id': item['problem_id'], 'model_answer': answer})
        atomic_json(args.output, submission)
        print(f'{len(submission["predictions"])}/{len(questions)} {item["problem_id"]}')


if __name__ == '__main__':
    main()
