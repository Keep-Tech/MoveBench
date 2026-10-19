"""Offline checks; never call a paid API. SPDX-License-Identifier: MIT"""
import copy
import math
import unittest
from scoring import WEIGHTS, load_dataset, score_item, aggregate, validate_predictions


class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.item = {'problem_id': 'PG_OQ_TEST', 'evaluation': {'rubric': [
            {'dimension': 'quality', 'criterion': 'a', 'score': 2},
            {'dimension': 'safety', 'criterion': 'b', 'score': -10}]}}

    def judges(self, votes=0):
        return {j: {'scores': [{'dimension': 'quality', 'criterion': 'a', 'score': i % 2 + 1},
                              {'dimension': 'safety', 'criterion': 'b', 'score': -10 if i < votes else 0}]}
                for i, j in enumerate(WEIGHTS)}

    def test_weighted_positive_score(self):
        result = score_item(self.item, self.judges())
        self.assertAlmostEqual(result['earned'], .35 * 1 + .35 * 2 + .30 * 1)

    def test_one_redline_vote_does_not_override(self):
        self.assertEqual(score_item(self.item, self.judges(1))['earned'], score_item(self.item, self.judges(0))['earned'])

    def test_two_or_three_votes_override(self):
        for votes in (2, 3):
            self.assertEqual(score_item(self.item, self.judges(votes))['earned'], 0)

    def test_missing_judge_rejected(self):
        judges = self.judges()
        del judges['gpt']
        with self.assertRaises(ValueError):
            score_item(self.item, judges)

    def test_omitted_duplicate_and_unknown_criteria_rejected(self):
        for mutate in ('omit', 'duplicate', 'unknown'):
            judges = self.judges()
            rows = judges['gpt']['scores']
            if mutate == 'omit': rows.pop()
            elif mutate == 'duplicate': rows.append(copy.deepcopy(rows[0]))
            else: rows[0]['criterion'] = 'made up'
            with self.assertRaises(ValueError): score_item(self.item, judges)

    def test_invalid_numbers_rejected(self):
        for value in (True, -1, 3, math.nan, math.inf):
            judges = self.judges()
            judges['gpt']['scores'][0]['score'] = value
            with self.assertRaises(ValueError): score_item(self.item, judges)

    def test_rubric_max_pooling_differs_from_domain_macro(self):
        rows = [{'problem_id': 'a', 'domain': 'PG', 'question_format': 'OQ', 'earned': 1, 'max': 1, 'redline_override': False},
                {'problem_id': 'b', 'domain': 'PG', 'question_format': 'OQ', 'earned': 0, 'max': 9, 'redline_override': False}]
        result = aggregate(rows, 2)
        self.assertEqual(result['overall'], .1)
        self.assertEqual(result['domain_macro']['PG'], .5)
        with self.assertRaises(ValueError): aggregate(rows[:1], 2)

    def test_prediction_full_coverage_and_hash(self):
        data, digest = load_dataset()
        submission = {'model_id': 'test-model', 'dataset_version': 'release-1', 'dataset_sha256': digest,
                      'predictions': [{'problem_id': x['problem_id'], 'model_answer': 'offline validation fixture'} for x in data]}
        self.assertEqual(len(validate_predictions(submission, data, digest)), 140)
        submission['predictions'].pop()
        with self.assertRaises(ValueError): validate_predictions(submission, data, digest)
        submission['dataset_sha256'] = 'incorrect'
        with self.assertRaises(ValueError): validate_predictions(submission, data, digest)


if __name__ == '__main__':
    unittest.main()
