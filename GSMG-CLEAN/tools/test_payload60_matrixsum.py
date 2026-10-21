"""Exact, bounded tests of the 83-cell DBBI remainder as matrix/sum-list data."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from test_offwhite_marker_alignment import extract, guided_parse, prime

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runs/2026-09-14_payload60_matrixsum'
TR=str.maketrans('abcdefghi','123456789')


def byte_integer(digits,base=10):
    n=int(digits,base)
    return n.to_bytes((n.bit_length()+7)//8,'big')


def ascii_paths(digits):
    count=[0]*(len(digits)+1); witness=['']*(len(digits)+1);count[0]=1
    for i in range(len(digits)):
        if not count[i]:continue
        for size in (2,3):
            part=digits[i:i+size]
            if len(part)==size and part[0]!='0' and 32<=int(part)<=126:
                count[i+size]+=count[i]
                witness[i+size]=witness[i]+chr(int(part))
    return dict(complete_paths=count[-1],witness=witness[-1] if count[-1] else None)


def integer_record(digits,base=10):
    raw=byte_integer(digits,base)
    texts={}
    for codec in ('ascii','utf-8','utf-16-le','utf-16-be','utf-32-le','utf-32-be','cp037','cp273'):
        try:texts[codec]=raw.decode(codec)
        except UnicodeError:pass
    return dict(digits=digits,base=base,byte_length=len(raw),hex=raw.hex(),
                strict_decodings=texts,fully_printable_ascii=all(32<=b<=126 or b in (9,10,13) for b in raw))


def margins(board):
    return [sum(r) for r in board],[sum(r[c] for r in board) for c in range(len(board[0]))]


def sequences(rows,cols):
    for name,values in [('rows',rows),('columns',cols),('rows_columns',rows+cols),('columns_rows',cols+rows)]:
        for direction,seq in [('forward',values),('reverse',values[::-1])]:
            yield name+'/'+direction,seq


def serializations(values):
    yield 'decimal_joined',''.join(map(str,values)).encode()
    for width in (2,3):
        yield f'decimal_minwidth{width}',''.join(f'{v:0{width}d}' for v in values).encode()
    for delimiter,name in [(' ','spaces'),(',','commas'),(';','semicolons'),('\n','LF')]:
        yield name,delimiter.join(map(str,values)).encode()
    yield 'json_compact',json.dumps(values,separators=(',',':')).encode()
    if all(0<=v<=255 for v in values):
        yield 'unsigned_bytes',bytes(values)
    if all(-128<=v<=127 for v in values):
        yield 'signed_bytes',bytes(v%256 for v in values)
    if all(0<=v<=65535 for v in values):
        for order in ('big','little'):
            yield 'unsigned16_'+order,b''.join(v.to_bytes(2,order) for v in values)
    if all(-32768<=v<=32767 for v in values):
        for order in ('big','little'):
            yield 'signed16_'+order,b''.join(v.to_bytes(2,order,signed=True) for v in values)


def main():
    OUT.mkdir(exist_ok=True)
    grid,image_hash=extract()
    marked=[x for x in grid if x['color'] not in 'KW']
    schedule=''.join('B' if x['rgb'][2] else 'Y' for x in marked)
    dbbi=(ROOT/'data/DBBI_91.txt').read_text().strip()
    faed=(ROOT/'data/FAED_570.txt').read_text().strip()
    wrapper=(ROOT/'data/salphaseion_compact_1075.txt').read_text().strip()
    parsed=guided_parse(dbbi,schedule)
    assert parsed['complete'] and parsed['logical_cells']==83
    payload=''.join(c['token'] for c in parsed['cells'] if not c['prime'])
    assert payload==(ROOT/'runs/2026-09-13_offwhite_alignment/payload_60.txt').read_text().strip()
    digits=payload.translate(TR)
    direct=integer_record(digits)
    raw=bytes.fromhex(direct['hex'])
    assert len(digits)==60 and len(raw)==25
    assert str(int.from_bytes(raw,'big'))==digits
    # Verify the exact page codec on both independently solved neighboring labels.
    for lo,hi,label in [(766,829,'lastwordsbeforearchichoice'),(830,859,'thispassword')]:
        s=wrapper[lo:hi].translate(str.maketrans('abcdefghio','1234567890'))
        assert byte_integer(s)==label.encode()
    assert ascii_paths('656667')['witness']=='ABC'
    manifest=dict(input=payload,input_digits=digits,input_sha256=hashlib.sha256(payload.encode()).hexdigest(),
                  poster_sha256=image_hash,
                  hypothesis='The ordinary cells of the poster-guided 83-cell DBBI parse are matrix data or a serialized poster sum list',
                  criterion='Exact equality of a complete representation or full decoded source phrase; no prefix/word-count success gate',
                  scope=['Original 14x14 poster geometry; first23/all25 selected markers; ordinal primes, ordinals, signed/unsigned/color-separated values',
                         'Binary poster as additional established representation; off-white remains zero in the known URL reading',
                         'Rows, columns, both concatenation orders, and full reversal; direct decimal/list text and fixed-width byte encodings',
                         'All exact rectangles of the 60 digit values; complete numerical and letter readings',
                         'All exact rectangles of the 25 decoded bytes, including 5x5; unsigned and signed-byte interpretations',
                         'Literal big/little-endian distinction is tested through exact byte equality, not guessed cryptography'],
                  exclusions='No password generation, AES, arbitrary symbol substitutions, selective deletion, ragged padding, or prime-sign claim')
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    ps=[n for n in range(2,101) if prime(n)]
    boards=[]
    for take in (23,25):
        for source in ('prime','ordinal'):
            for mode in ('all','blue_negative','yellow_negative','blue_only','yellow_only'):
                board=[[0]*14 for _ in range(14)]
                for i,cell in enumerate(marked[:take]):
                    color=schedule[i]
                    value=ps[i] if source=='prime' else i+1
                    if mode=='blue_negative' and color=='B' or mode=='yellow_negative' and color=='Y':value=-value
                    if mode=='blue_only' and color!='B' or mode=='yellow_only' and color!='Y':value=0
                    board[cell['row']][cell['column']]=value
                boards.append((f'{take}_{source}_{mode}',board))
    board=[[0]*14 for _ in range(14)]
    for c in grid:board[c['row']][c['column']]=int(c['color'] in 'KB')
    boards.append(('known_binary',board))
    targets={'decimal_digits_ascii':digits.encode(),'page_integer_bytes':raw,'letters_ascii':payload.encode()}
    attempts=[];hits=[];board_records=[]
    for board_name,board in boards:
        rows,cols=margins(board)
        assert sum(rows)==sum(cols)
        board_records.append(dict(name=board_name,rows=rows,columns=cols,total=sum(rows)))
        for axis,values in sequences(rows,cols):
            for form,value in serializations(values):
                matches=[name for name,target in targets.items() if value==target]
                rec=dict(board=board_name,axis=axis,values=values,form=form,bytes=len(value),hex=value.hex(),matches=matches)
                attempts.append(rec)
                if matches:hits.append(rec)
    # Construct complete source objects from the remainder itself, with no
    # added cells. This is a separate hypothesis from decoding it as a sum list.
    array=[int(c) for c in digits]
    payload_sums=[]; source_targets=['matrixsumlist','lastwordsbeforearchichoice','thispassword',
                                    'ourfirsthintisyourlastcommand','hillfexmgsgq']
    sums_views=[]
    for width in range(1,61):
        if 60%width:continue
        board=[array[i:i+width] for i in range(0,60,width)]
        rows,cols=margins(board)
        assert sum(rows)==sum(cols)==sum(array)==336
        for axis,values in sequences(rows,cols):
            joined=''.join(map(str,values))
            texts={'mod26_A0':''.join(chr(97+v%26) for v in values),
                   'mod26_A1':''.join(chr(97+(v-1)%26) for v in values)}
            if all(32<=v<=126 for v in values):texts['ASCII']=''.join(chr(v) for v in values)
            view=integer_record(joined)
            rec=dict(width=width,height=60//width,axis=axis,values=values,decimal=joined,
                     text_views=texts,integer_view=view,
                     exact_label_matches=[dict(form=n,label=t) for n,t in texts.items() if t in source_targets],
                     exact_FAED=joined==faed.translate(TR),exact_DBBI=joined==dbbi.translate(TR))
            payload_sums.append(rec)
            if rec['exact_label_matches'] or rec['exact_FAED'] or rec['exact_DBBI']:sums_views.append(rec)
    byte_sums=[]
    for interpretation,array in [('unsigned8',list(raw)),('signed8',[v if v<128 else v-256 for v in raw])]:
        for width in (1,5,25):
            board=[array[i:i+width] for i in range(0,25,width)]
            rows,cols=margins(board)
            assert sum(rows)==sum(cols)==sum(array)
            for axis,values in sequences(rows,cols):
                texts={'mod26_A0':''.join(chr(97+v%26) for v in values),
                       'mod26_A1':''.join(chr(97+(v-1)%26) for v in values)}
                if all(32<=v<=126 for v in values):texts['ASCII']=''.join(chr(v) for v in values)
                joined=''.join(map(str,values))
                byte_sums.append(dict(interpretation=interpretation,width=width,height=25//width,axis=axis,
                                      values=values,text_views=texts,
                                      integer_view=integer_record(joined) if all(v>=0 for v in values) else None,
                                      exact_label_matches=[dict(form=n,label=t) for n,t in texts.items() if t in source_targets],
                                      exact_FAED=joined==faed.translate(TR),exact_DBBI=joined==dbbi.translate(TR)))
    known={'matrixsumlist':wrapper[91:195], 'lastwordsbeforearchichoice':wrapper[766:829],
           'thispassword':wrapper[830:859]}
    direct_labels=[]
    for label in known:
        encoded=str(int.from_bytes(label.encode(),'big'))
        direct_labels.append(dict(label=label,decimal=encoded,length=len(encoded),equals_payload=encoded==digits))
    # Formatting tests also need a positive full-list control.
    values=[2,13,89,-97,0]
    serials=dict(serializations(values))
    assert json.loads(serials['json_compact'])==values
    assert [int.from_bytes(serials['signed16_big'][i:i+2],'big',signed=True) for i in range(0,10,2)]==values
    metadata=dict(direct=direct,direct_printable_ASCII_decimal=ascii_paths(digits),direct_labels=direct_labels,
                  direct_byte_matrix=dict(shape=[5,5],distinct_values=len(set(raw)),values=list(raw),
                                          is_permutation_0_24=set(raw)==set(range(25)),is_permutation_1_25=set(raw)==set(range(1,26))),
                  digit_total=sum(map(int,digits)),poster_boards=len(boards),poster_serializations=len(attempts),
                  exact_poster_matches=hits,payload_sum_readings=len(payload_sums),exact_payload_sum_matches=sums_views,
                  decoded_byte_sum_readings=len(byte_sums),exact_decoded_byte_sum_matches=[r for r in byte_sums if r['exact_label_matches'] or r['exact_FAED'] or r['exact_DBBI']],
                  binary_margin_bound=dict(poster14x14_max_decimal_chars=56,poster14x15_max_decimal_chars=58,
                                           input_decimal_chars=60,scope='Unpadded concatenation of all row and column sums of a binary matrix; no separators'),
                  controls_passed=True,status='No exact sum-list or full instruction recovered; every tested representation retained')
    for name,data in [('summary.json',metadata),('poster_boards.json',board_records),
                      ('poster_serializations.json',attempts),('payload_sum_readings.json',payload_sums),('decoded_byte_sum_readings.json',byte_sums)]:
        (OUT/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
    (OUT/'direct_integer.bin').write_bytes(raw)
    print(json.dumps(metadata,indent=2))


if __name__=='__main__':
    main()
