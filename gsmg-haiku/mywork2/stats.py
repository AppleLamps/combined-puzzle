from collections import Counter
t=open('files/salphaseion-textarea.txt').read().strip()
r1=t[:91]; r2=t[195:765]
for n,r in(('r1',r1),('r2',r2)):
    c=Counter(r); print(n,len(r),' '.join(f'{k}:{c[k]}' for k in 'abcdefghi'))
    d=''.join(str(ord(x)-96) for x in r)
    print(d)
    # digram table
    cc=Counter(zip(r,r[1:]))
    for a in 'abcdefghi': print(a,' '.join(f'{cc[(a,b)]:3d}' for b in 'abcdefghi'))
    # base9
    for off,name in((97,'a=0'),):
        v=0
        for ch in r: v=v*9+ord(ch)-off
        b=v.to_bytes((v.bit_length()+7)//8,'big'); print(name,len(b),b[:60])
        v=0
        for ch in r[::-1]: v=v*9+ord(ch)-off
        b=v.to_bytes((v.bit_length()+7)//8,'big'); print(name,'rev',len(b),b[:60])
    v=0
    for ch in r: v=v*9+ord(ch)-96
    b=v.to_bytes((v.bit_length()+7)//8,'big'); print('bij',len(b),b[:60])
