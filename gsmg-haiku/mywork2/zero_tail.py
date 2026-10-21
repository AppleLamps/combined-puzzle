"""Hypothesis: r2 is a decimal number (-> hex -> ASCII, like the z-sections) whose zeros were
replaced by other letters (counts: six letters ~57 = 570/10, g has ~50 extra).
N mod 2^(8k) depends only on the last 8k decimal digits, so search from the tail."""
import sys, itertools
NODELIM=300000
t=open('files/salphaseion-textarea.txt').read().strip()
def run(r, zl, allowed, maxout=20, label=''):
    d=[ord(c)-96 for c in r]; n=len(d)
    res=[]; best=[0,None]
    sys.setrecursionlimit(10000)
    nodes=[0]
    def rec(k, val, txt):
        nodes[0]+=1
        if nodes[0]>NODELIM: return
        # val = integer of chosen last 8k digits
        if len(res)>=maxout: return
        if k>best[0]: best[0]=k; best[1]=txt
        lo=n-8*(k+1)
        if lo<0:
            # remaining leading digits
            head=r[:n-8*k]
            idx=[i for i,c in enumerate(head) if c in zl]
            for m in itertools.product((0,1),repeat=len(idx)):
                dd=[d[i] for i in range(len(head))]
                for i,b in zip(idx,m):
                    if b: dd[i]=0
                v=int(''.join(map(str,dd)) or '0')*10**(8*k)+val
                b=v.to_bytes((v.bit_length()+7)//8,'big')
                if all(x in allowed for x in b): res.append(b)
            return
        seg=r[lo:lo+8]; idx=[i for i,c in enumerate(seg) if c in zl]
        for m in itertools.product((0,1),repeat=len(idx)):
            dd=[d[lo+i] for i in range(8)]
            for i,b in zip(idx,m):
                if b: dd[i]=0
            v=int(''.join(map(str,dd)))*10**(8*k)+val
            byte=(v>>(8*k))&0xFF
            if byte in allowed:
                rec(k+1, v, chr(byte)+txt)
    rec(0,0,'')
    print(label,'nodes',nodes[0],'zl=',zl,'solutions',len(res),'deepest',best[0],'bytes tail:',repr(best[1]))
    for b in res[:5]: print('  ',b)
    sys.stdout.flush()
low=set(b'abcdefghijklmnopqrstuvwxyz')
lowsp=low|set(b' ')
alnum=low|set(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ')
pr=set(range(32,127))
r1=t[:91]; r2=t[195:765]
# control: z-section with zeros disguised as g
ctl=t[766:829].replace('o','g')
run(ctl,'g',low,label='control')
for name,r in (('r2',r2),('r2rev',r2[::-1]),('r1',r1),('r1rev',r1[::-1])):
    for zl in ('g','i','e','gi','ge','gie'):
        for an,al in (('low',low),('alnum',alnum),('print',pr)):
            if len(zl)==3 and an=='print': continue
            run(r,zl,al,label=f'{name} {an}')
