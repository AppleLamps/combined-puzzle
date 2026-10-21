"""Preserve an exploratory full-marker sum observation without promoting it."""
import json
from collections import defaultdict
from pathlib import Path
from test_offwhite_marker_alignment import extract,prime

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-14_offwhite_colour_totals'


def main():
    OUT.mkdir(exist_ok=True)
    cells,digest=extract()
    special=[c for c in cells if c['color'] not in ('K','W')]
    ps=[n for n in range(2,100) if prime(n)]
    assert len(special)==len(ps)==25
    sums={color:sum(p for p,c in zip(ps,special) if c['color']==color) for color in ('B','Y','F')}
    assert sums==dict(B=490,Y=497,F=73)
    regular=[c for c in special if c['color']!='F']
    old={color:sum(p for p,c in zip(ps,regular) if c['color']==color) for color in ('B','Y')}
    sal=(ROOT/'data/salphaseion_compact_1075.txt').read_text().strip()
    assert [i for i in (765,829,859) if sal[i]=='z']==[765,829,859]
    assert sal[1063:]=='shabefanstoo'
    y_rgb=next(c['rgb'] for c in special if c['color']=='Y')
    b_rgb=next(c['rgb'] for c in special if c['color']=='B')
    # Exact conditional subset count: F stays at its observed position. Nine
    # yellow labels occupy nine of the remaining 24 prime slots uniformly.
    fpos=next(i for i,c in enumerate(special) if c['color']=='F')
    dp={(0,0):1}
    for i,p in enumerate(ps):
        if i==fpos:continue
        new=dict(dp)
        for (k,total),count in dp.items():
            if k<9:new[k+1,total+p]=new.get((k+1,total+p),0)+count
        dp=new
    denominator=sum(count for (k,total),count in dp.items() if k==9)
    numerator=dp.get((9,sum(y_rgb)),0)
    gap_checks=[]
    for gap in range(25):
        markers=regular[:gap]+[special[fpos]]+regular[gap:]
        ysum=sum(p for p,c in zip(ps,markers) if c['color']=='Y')
        gap_checks.append(dict(gap=gap,yellow_sum=ysum,matches_yellow_rgb=ysum==sum(y_rgb)))
    record=dict(status='Exploratory arithmetic observation; no decoded field or password follows.',poster_sha256=digest,
                all25_prime_sums=sums,regular24_prime_sums=old,
                rgb={'B':b_rgb,'Y':y_rgb},rgb_sums={'B':sum(b_rgb),'Y':sum(y_rgb)},
                exact_equalities=dict(yellow_prime_sum_equals_rgb_sum=sums['Y']==sum(y_rgb),
                                      all25_prime_sum=sum(ps),sal_length_without_three_separators_and_last_literal=len(sal)-3-len('shabefanstoo'),
                                      blue_plus_offwhite=sums['B']+sums['F'],faed_length_minus_btcseed_prefix=570-len('btcseed'),
                                      initial_sal_before_first_separator=765,white_rgb_sum=3*255),
                countercheck='Ordinary blue prime sum is 490, not its RGB sum 339. Grouping off-white with blue changes it to 563 but does not fix that mismatch.',
                conditional_null=dict(description='Uniformly select nine yellow slots among the 24 non-F prime slots; F fixed at its observed position',
                                      exact_yellow_target_count=numerator,total_assignments=denominator,probability=numerator/denominator,
                                      caveat='Chosen after observing data; does not correct for prior arithmetic searches, other targets or other rules.'),
                limitations=['The BTCSEED prefix is an unconfirmed Bifid lead, not an authenticated plaintext boundary.',
                             'The 1060-character equality uses a selected subset of the Sal stream and is not a complete cipher recipe.',
                             'RGB summation is an added operation; no creator instruction selecting it has been found.',
                             'Do not turn these equalities into passwords or call them a solved matrix construction.'],gap_checks=gap_checks)
    (OUT/'observation.json').write_text(json.dumps(record,indent=2))
    print(json.dumps({k:v for k,v in record.items() if k not in ('gap_checks','limitations')},indent=2))


if __name__=='__main__':main()
