"""Recompute audited evidence before updating leaderboard.json. SPDX-License-Identifier: MIT"""
import argparse
import hashlib
import json
import urllib.parse
from pathlib import Path
from api_client import atomic_json
from scoring import ROOT, WEIGHTS, SCORING_VERSION, load_dataset, score_item, aggregate


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--evidence', type=Path, required=True)
    p.add_argument('--evidence-url', required=True, help='Public, immutable evidence link reviewed by maintainer')
    args = p.parse_args()
    url = urllib.parse.urlsplit(args.evidence_url)
    if (url.scheme != 'https' or url.hostname not in ('github.com', 'raw.githubusercontent.com')
            or not url.path.startswith('/SatoSakula/MoveBench/') or url.username or url.password
            or url.query or url.fragment):
        raise ValueError('Use a public GitHub evidence URL in this repository, without credentials or query parameters')
    data, digest = load_dataset()
    evidence = json.loads(args.evidence.read_text())
    if not evidence.get('complete') or evidence.get('dataset_sha256') != digest:
        raise ValueError('Complete evidence for this dataset is required')
    if evidence.get('policy', {}).get('scoring_version') != SCORING_VERSION:
        raise ValueError('Scoring version mismatch')
    judges = evidence['policy'].get('judges', [])
    if len(judges) != 3 or {j['id'] for j in judges} != set(WEIGHTS) or any(j['weight'] != WEIGHTS[j['id']] for j in judges):
        raise ValueError('Judge policy mismatch')
    indexed = {r['problem_id']: r for r in evidence['results']}
    if len(indexed) != len(evidence['results']) or set(indexed) != {x['problem_id'] for x in data}:
        raise ValueError('Evidence must cover every item exactly once')
    rows = [score_item(item, indexed[item['problem_id']]['judges']) for item in data]
    score = aggregate(rows, len(data))
    target = ROOT / 'leaderboard.json'
    board = json.loads(target.read_text())
    if board['dataset_sha256'] != digest or board['scoring_version'] != SCORING_VERSION:
        raise ValueError('Leaderboard version mismatch')
    policy_hash = hashlib.sha256(json.dumps(evidence['policy'], sort_keys=True).encode()).hexdigest()
    if board.get('judge_policy_sha256') not in (None, policy_hash):
        raise ValueError('Judge configuration differs from this leaderboard; use a separately versioned leaderboard')
    board['judge_policy_sha256'] = policy_hash
    entry = {'model_id': evidence['model_id'], **score, 'evaluated_at': evidence['evaluated_at'],
             'run_id': evidence['run_id'], 'evidence_url': args.evidence_url, 'verification': 'maintainer-reviewed',
             'judge_policy_sha256': policy_hash}
    board['entries'] = [r for r in board['entries'] if r['run_id'] != entry['run_id']] + [entry]
    board['entries'].sort(key=lambda r: r['overall'], reverse=True)
    atomic_json(target, board)
    print(f'Updated leaderboard: {entry["model_id"]} / {score["overall"]:.6f}')


if __name__ == '__main__':
    main()
