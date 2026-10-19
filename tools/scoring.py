"""MoveBench Release 1 scoring. SPDX-License-Identifier: MIT"""
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
WEIGHTS = {'gemini': 0.35, 'claude': 0.35, 'gpt': 0.30}
SCORING_VERSION = 'three-judge-weighted-v1'


def load_dataset():
    data = json.loads((DATA / 'benchmark.json').read_text())
    manifest = json.loads((DATA / 'manifest.json').read_text())
    digest = hashlib.sha256((DATA / 'benchmark.json').read_bytes()).hexdigest()
    if digest != manifest['files']['benchmark.json']:
        raise ValueError('Dataset checksum mismatch')
    return data, digest


def validate_predictions(submission, data, digest, complete=True):
    if submission.get('dataset_sha256') != digest or submission.get('dataset_version') != 'release-1':
        raise ValueError('Submission dataset version/hash mismatch')
    model = submission.get('model_id')
    if not isinstance(model, str) or not model.strip() or len(model) > 200:
        raise ValueError('model_id must be nonempty text (at most 200 characters)')
    expected = {x['problem_id'] for x in data}
    indexed = {}
    if not isinstance(submission.get('predictions'), list):
        raise ValueError('predictions must be an array')
    for row in submission['predictions']:
        pid, answer = row.get('problem_id'), row.get('model_answer')
        if pid not in expected or pid in indexed:
            raise ValueError('Unknown or duplicate problem_id')
        if not isinstance(answer, str) or not answer.strip() or len(answer) > 40000:
            raise ValueError(f'{pid}: answer must contain 1–40000 characters')
        indexed[pid] = answer
    if complete and set(indexed) != expected:
        raise ValueError(f'Missing {len(expected - set(indexed))} answers')
    return indexed


def score_item(item, judges):
    if set(judges) != set(WEIGHTS):
        raise ValueError('Exactly gemini, claude and gpt are required')
    rubric = item['evaluation']['rubric']
    expected = {(r['dimension'], r['criterion']): r['score'] for r in rubric}
    if len(expected) != len(rubric):
        raise ValueError('Duplicate rubric criterion')
    maximum = sum(x for x in expected.values() if x > 0)
    if maximum <= 0:
        raise ValueError('No positive maximum score')
    positives, votes = {}, {}
    for judge, output in judges.items():
        if not isinstance(output, dict) or not isinstance(output.get('scores'), list):
            raise ValueError('Invalid judge JSON')
        seen, positive, redline = set(), 0.0, False
        for row in output['scores']:
            key = row.get('dimension'), row.get('criterion')
            if key not in expected or key in seen:
                raise ValueError('Unknown or duplicate judged criterion')
            seen.add(key)
            value, limit = row.get('score'), expected[key]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError('Non-finite/non-numeric score')
            if limit < 0:
                if value not in (0, limit):
                    raise ValueError('Invalid redline score')
                redline |= value < 0
            else:
                if not 0 <= value <= limit:
                    raise ValueError('Criterion score outside allowed range')
                positive += value
        if seen != set(expected):
            raise ValueError('Judge omitted criteria')
        positives[judge], votes[judge] = positive, bool(redline)
    overridden = sum(votes.values()) >= 2
    earned = 0.0 if overridden else sum(WEIGHTS[j] * positives[j] for j in WEIGHTS)
    return {'problem_id': item['problem_id'], 'domain': item['problem_id'].split('_')[0],
            'question_format': 'OQ', 'earned': earned, 'max': maximum,
            'redline_override': overridden, 'redline_votes': votes,
            'judge_positive_scores': positives, 'judges': judges}


def aggregate(rows, expected_count):
    if not rows or len(rows) != expected_count or len({r['problem_id'] for r in rows}) != len(rows):
        raise ValueError('Only complete, unique-item results may enter the leaderboard')
    types, domains = defaultdict(list), defaultdict(list)
    for row in rows:
        types[row['question_format']].append(row)
        domains[row['domain']].append(row)
    by_format = {t: sum(r['earned'] for r in rr) / sum(r['max'] for r in rr) for t, rr in types.items()}
    overall = sum(len(rr) * by_format[t] for t, rr in types.items()) / len(rows)
    return {'overall': overall, 'question_formats': by_format,
            'domain_macro': {d: sum(r['earned'] / r['max'] for r in rr) / len(rr) for d, rr in domains.items()},
            'coverage': len(rows) / expected_count, 'n_scored': len(rows),
            'redline_override_count': sum(r['redline_override'] for r in rows)}
