"""Maintainer-run, three-judge evaluation; never run on untrusted fork code.
SPDX-License-Identifier: MIT
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
from api_client import chat, atomic_json
from scoring import ROOT, WEIGHTS, SCORING_VERSION, load_dataset, validate_predictions, score_item, aggregate


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--submission', type=Path, required=True)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    data, digest = load_dataset()
    submission = json.loads(args.submission.read_text())
    answers = validate_predictions(submission, data, digest)
    config = json.loads(args.config.read_text())
    judges = config['judges']
    if len(judges) != 3 or {j['id'] for j in judges} != set(WEIGHTS):
        raise ValueError('Exactly the configured gemini, claude and gpt judges are required')
    if len({(j['base_url'], j['model']) for j in judges}) != 3:
        raise ValueError('Three distinct judge configurations are required')
    for j in judges:
        if j['weight'] != WEIGHTS[j['id']] or 'REPLACE' in j['model']:
            raise ValueError('Configure exact judge model IDs; weights are fixed at .35/.35/.30')
        if not os.environ.get(j['api_key_env']):
            raise ValueError(f'Missing environment variable {j["api_key_env"]}')
    # The evidence records env-variable names, never their values.
    prompt = (ROOT / 'judge_prompt.txt').read_text().strip()
    policy = {'scoring_version': SCORING_VERSION, 'judges': judges,
              'temperature': config.get('temperature', 0), 'max_tokens': config.get('max_tokens', 8192),
              'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
              'scoring_source_sha256': hashlib.sha256((ROOT / 'scoring.py').read_bytes()).hexdigest()}
    run_id = hashlib.sha256(json.dumps({'submission': submission, 'policy': policy}, sort_keys=True).encode()).hexdigest()
    evidence = {'run_id': run_id, 'dataset_version': 'release-1', 'dataset_sha256': digest,
                'model_id': submission['model_id'], 'policy': policy, 'complete': False, 'results': []}
    if args.output.exists():
        old = json.loads(args.output.read_text())
        if old.get('run_id') != run_id:
            raise ValueError('Evidence checkpoint mismatch; choose another output path')
        # Revalidate any completed items; no partial judge committee is accepted.
        lookup = {x['problem_id']: x for x in data}
        if len({r['problem_id'] for r in old['results']}) != len(old['results']):
            raise ValueError('Duplicate checkpoint item')
        for row in old['results']:
            computed = score_item(lookup[row['problem_id']], row['judges'])
            if any(computed[k] != row[k] for k in ('earned', 'max', 'redline_override')):
                raise ValueError('Checkpoint score mismatch')
        evidence = old
    done = {r['problem_id'] for r in evidence['results']}
    for item in data:
        if item['problem_id'] in done:
            continue
        body = item['problem'].get('question') or item['problem'].get('context')
        user_input = 'Problem:\n' + body + '\n\nRubric:\n' + json.dumps(item['evaluation']['rubric'], ensure_ascii=False) + '\n\nAnswer:\n' + answers[item['problem_id']]
        outputs = {}
        for judge in judges:
            raw = chat(judge['base_url'], os.environ[judge['api_key_env']], judge['model'],
                       [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': user_input}],
                       policy['temperature'], policy['max_tokens'])
            # Reject malformed JSON rather than inventing scores or silently dropping a judge.
            outputs[judge['id']] = json.loads(raw)
        row = score_item(item, outputs)
        row['model_answer'] = answers[item['problem_id']]
        evidence['results'].append(row)
        atomic_json(args.output, evidence)
        print(f'{len(evidence["results"])}/{len(data)} {item["problem_id"]}')
    evidence['score'] = aggregate(evidence['results'], len(data))
    evidence['complete'] = True
    evidence['evaluated_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    atomic_json(args.output, evidence)
    print(json.dumps(evidence['score'], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
