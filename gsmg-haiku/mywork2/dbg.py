src=open('mywork2/zero_mixed.py').read().split("def enc(s)")[0]
src=src.replace("        k += 1\n","        k += 1\n        rk=[i for i,s in enumerate(states) if TRUE.endswith(s[3])]\n        print(k,'true rank',rk[:1],len(states),repr(states[0][3][:30]) if states else None)\n")
TRUE="The last words before the Architect's choice: This password, Neo."
exec(src)
c1=str(int.from_bytes(TRUE.encode(),'big')); A='abcdefghi'
print(len(c1), [c1[max(0,len(c1)-8*(i+1)):len(c1)-8*i].count('0') for i in range(20)])
search(''.join(A[int(x)-1] for x in c1 if x != '0'), 'insert', beam=20000, label='ci')
