"""Controls for replacement accounting and the actual selection pipeline."""
import unittest
import aligned_replacement_pipeline as a


class ReplacementTests(unittest.TestCase):
    def test_numbers_apostrophes_and_offsets(self):
        text = "You’ve 23 keys."
        ts = a.tokenize(text, 'spelled')
        self.assertEqual([t['value'] for t in ts], ['YOUVE','TWENTY','THREE','KEYS'])
        self.assertEqual(text[ts[1]['start']:ts[1]['end']], '23')
        self.assertEqual(ts[1]['start'], ts[2]['start'])

    def test_unequal_replacements_not_truncated(self):
        src = 'THE OLD LONG SOURCE IS HERE'.split()
        dst = 'THE NEW IS HERE'.split()
        for method in ['sequence','lcs']:
            ops = a.local_ops(src,dst,method)
            a.verify_ops(src,dst,ops)
            removed = [x for tag,i,j,_,_ in ops if tag != 'equal' for x in src[i:j]]
            added = [x for tag,_,_,i,j in ops if tag != 'equal' for x in dst[i:j]]
            self.assertEqual(removed, ['OLD','LONG','SOURCE'])
            self.assertEqual(added, ['NEW'])

    def test_end_indexing_and_no_silent_repairs(self):
        words = ['FIRST','MIDDLE','LAST']
        self.assertEqual(a.extract_words(words,[1,3],'end1')['words'], ['LAST','FIRST'])
        for bad in [[0],[-1],[4]]:
            self.assertIsNone(a.extract_words(words,bad,'start1'))
        self.assertEqual(a.extract_words(words,[0],'start0')['words'], ['FIRST'])

    def test_schedule_and_sum_conservation(self):
        colors = 'BBBBYBBBYYBBBBYBBYYBYYBY'
        self.assertFalse(a.sum_pipeline(dict(values=[1]*84,shape=[6,14]),colors))
        mat = dict(values=[1]*100,shape=[10,10])
        results = a.sum_pipeline(mat,colors)
        self.assertEqual(len(results),12)
        for r in results:
            if r['prime_weight'] and r['colour']=='yellow': self.assertEqual(sum(r['sums']),479)
            if r['prime_weight'] and r['colour']=='blue': self.assertEqual(sum(r['sums']),484)

    def test_planted_end_to_end_selection(self):
        # Each column has exactly one selected blue prime. Fill the rest with zero;
        # require the real mask/sum/index functions to recover the planted words.
        colors = 'B'*24
        mat = dict(values=[0]*100,shape=[10,10])
        mat['values'][1] = 1    # prime slot 2, column 1
        mat['values'][2] = 2    # prime slot 3, column 2
        mat['values'][4] = 3    # prime slot 5, column 4
        summed = next(r['sums'] for r in a.sum_pipeline(mat,colors)
                      if r['colour']=='blue' and r['axis']=='columns' and not r['prime_weight'])
        ws = ['NULL','FOLLOW','THE','RABBIT']
        got = a.extract_words(ws,summed,'start0')['words']
        self.assertEqual(got,['NULL','FOLLOW','THE','NULL','RABBIT','NULL','NULL','NULL','NULL','NULL'])
        # Mutation must change the full reconstructed result.
        mat['values'][4] = 2
        mutated = next(r['sums'] for r in a.sum_pipeline(mat,colors)
                       if r['colour']=='blue' and r['axis']=='columns' and not r['prime_weight'])
        self.assertNotEqual(a.extract_words(ws,mutated,'start0')['words'],got)

    def test_row_colour_schedule_requires_all_24_rows(self):
        row={'source_features':[1,1,1],'replacement_features':[2,2,2],'difference':[1,1,1]}
        self.assertEqual(a.row_colour_pipeline([row]*22,'B'*24),[])
        sums=a.row_colour_pipeline([row]*24,'BBBBYBBBYYBBBBYBBYYBYYBY')
        self.assertEqual(len(sums),36)
        r=next(r for r in sums if r['side']=='source_features' and r['feature']=='word_count'
               and r['colour']=='Y' and r['prime_weight'])
        self.assertEqual(r['total'],479)


if __name__ == '__main__': unittest.main()