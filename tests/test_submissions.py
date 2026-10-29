import copy, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from validate import validate

class SubmissionTests(unittest.TestCase):
    def setUp(self):
        self.s=json.loads((ROOT/'data/submission_template.json').read_text())
        self.s['generation']={'date':'2026-10-29','temperature':0,'max_tokens':128}
        for row in self.s['predictions']:
            row['model_answer']='A' if '_SS' in row['problem_id'] else ('A,C' if '_MS' in row['problem_id'] else 'Synthetic test response')
    def test_complete(self): self.assertEqual(validate(self.s),80)
    def test_missing_generation(self):
        self.s['generation']={}
        with self.assertRaisesRegex(ValueError,'generation.date'):validate(self.s)
    def test_bad_generation(self):
        for field,value in [('date','2026-02-30'),('temperature',float('nan')),('temperature',True),('max_tokens',0),('max_tokens',True)]:
            with self.subTest(field=field,value=value):
                data=copy.deepcopy(self.s);data['generation'][field]=value
                with self.assertRaises(ValueError):validate(data)
    def test_mcq_invalid(self):
        for answer in ['Z','A,A','A,C','Answer: A']:
            with self.subTest(answer=answer):
                data=copy.deepcopy(self.s);row=next(x for x in data['predictions'] if '_SS' in x['problem_id']);row['model_answer']=answer
                with self.assertRaises(ValueError):validate(data)
    def test_mcq_explanation(self):
        next(x for x in self.s['predictions'] if '_SS' in x['problem_id'])['model_answer']='A\nReason for answer'
        self.assertEqual(validate(self.s),80)
    def test_bad_ids_and_hash(self):
        for kind in ['missing','duplicate','hash','empty']:
            with self.subTest(kind=kind):
                data=copy.deepcopy(self.s)
                if kind=='missing':data['predictions'].pop()
                if kind=='duplicate':data['predictions'][1]=data['predictions'][0]
                if kind=='hash':data['dataset_sha256']='wrong'
                if kind=='empty':data['predictions'][0]['model_answer']=''
                with self.assertRaises(ValueError):validate(data)

if __name__=='__main__':unittest.main()
