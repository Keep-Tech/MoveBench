"""Validate data integrity and optionally a submission. SPDX-License-Identifier: MIT"""
import argparse
import hashlib
import json
from scoring import ROOT, load_dataset, validate_predictions


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--submission')
    args = p.parse_args()
    data, digest = load_dataset()
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    for filename, expected in manifest['files'].items():
        if hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Checksum mismatch: {filename}')
    if len(data) != manifest['n_questions'] or len({x['problem_id'] for x in data}) != len(data):
        raise ValueError('Dataset count/ID mismatch')
    lines = [json.loads(l) for l in (ROOT / 'test.jsonl').read_text().splitlines()]
    if lines != data:
        raise ValueError('JSON and JSONL records differ')
    questions = json.loads((ROOT / 'questions.json').read_text())
    if [q['problem_id'] for q in questions] != [x['problem_id'] for x in data]:
        raise ValueError('Question order mismatch')
    count = 0
    for item, question in zip(data, questions):
        if question['problem'] != item['problem'] or set(question) != {'problem_id', 'problem', 'domain', 'question_format'}:
            raise ValueError('Student input differs from data or contains extra fields')
        if item['evaluation']['type'] != 'rubric' or item['evaluation']['question_structure'].lower() != 'openqa':
            raise ValueError('Release 1 supports only annotated OQ items')
        rubric = item['evaluation']['rubric']
        if len({(r['dimension'], r['criterion']) for r in rubric}) != len(rubric) or sum(r['score'] for r in rubric if r['score'] > 0) <= 0:
            raise ValueError('Invalid rubric')
        count += len(rubric)
    if count != manifest['n_rubric_criteria']:
        raise ValueError('Rubric count mismatch')
    if args.submission:
        validate_predictions(json.loads(__import__('pathlib').Path(args.submission).read_text()), data, digest)
        print('Submission complete and valid')
    print(f'Dataset valid: {len(data)} questions, {count} rubric criteria, SHA-256 {digest}')


if __name__ == '__main__':
    main()
