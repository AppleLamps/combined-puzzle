import unittest
import compare_dbbi_forward_models as f

class ForwardTests(unittest.TestCase):
    def test_heldout_full_prediction(self):
        # Three-digit row sums: 20x20 uniform fives -> twenty 100s -> 60 digits.
        # Forward generator never uses the expected payload to fit the sums.
        values=[5]*400
        source=next(p for p in f.proposals(values) if p['shape']==[20,20] and p['axis']=='rows' and not p['reverse'])
        schedule=[dict(token='b' if i%2 else 'be') for i in range(25)]
        expected=f.insert(('100'*20).translate(f.LET),schedule,83)
        generated=f.insert(source['payload'],schedule,83)
        self.assertEqual(generated,expected)
        parsed=f.parse(expected,schedule)
        self.assertTrue(parsed['complete']);self.assertEqual(parsed['logical_cells'],83)
        self.assertEqual(parsed['payload'],source['payload'])
        self.assertIsNone(f.insert(source['payload'],schedule,84))
        values[0]+=1
        changed=next(p for p in f.proposals(values) if p['shape']==[20,20] and p['axis']=='rows' and not p['reverse'])
        self.assertNotEqual(f.insert(changed['payload'],schedule,83),expected)

    def test_endpoint_cannot_be_chosen_from_shared_prefix(self):
        schedule=[dict(token='b') for _ in range(25)]
        text=f.insert('a'*61,schedule,84)
        parsed=f.parse(text,schedule)
        self.assertEqual(parsed['logical_cells'],84)
        self.assertEqual(''.join(c['token'] for c in parsed['cells']),text)

    def test_84_endpoint_full_prediction(self):
        # Twenty row sums of 100, then one of 1: exactly 61 serialized digits.
        values=[5]*400+[1]+[0]*19
        source=next(p for p in f.proposals(values) if p['shape']==[21,20]
                    and p['axis']=='rows' and not p['reverse'])
        schedule=[dict(token='b') for _ in range(25)]
        self.assertEqual(len(source['payload']),61)
        expected=f.insert(('100'*20+'1').translate(f.LET),schedule,84)
        generated=f.insert(source['payload'],schedule,84)
        self.assertIsNotNone(generated)
        self.assertEqual(generated,expected)
        self.assertIsNone(f.insert(source['payload'],schedule,83))
        decoded=f.parse(generated,schedule)
        self.assertTrue(decoded['complete'])
        self.assertEqual(decoded['logical_cells'],84)
        self.assertEqual(decoded['payload'],source['payload'])

    def test_no_schedule_extension(self):
        result=f.parse('aa',[dict(token='b')],start_slot=101,start_marker=1)
        self.assertFalse(result['complete']);self.assertEqual(result['reason'],'schedule exhausted')

    def test_all_margins_conserve_total(self):
        for p in f.proposals([1,2,3,4,5,6]):
            self.assertEqual(sum(p['sums']),21*(2 if '_' in p['axis'] else 1))

if __name__=='__main__':unittest.main()