import sys, random
T=open('ta.txt').read().strip()
faed=T[195:765]; dbbi=T[:91]
seg1=T[766:829]; seg2=T[830:859]
def gspace_digits(s):  # digit string -> letter space with 0,7 -> g
    m={'1':'a','2':'b','3':'c','4':'d','5':'e','6':'f','7':'g','8':'h','9':'i','0':'g'}
    return ''.join(m[c] for c in s)
def kmers(s,k): return {s[i:i+k]:i for i in range(len(s)-k+1)}
targets={'faed':faed,'dbbi':dbbi,'faed_rev':faed[::-1],'dbbi_rev':dbbi[::-1],'residue':'difhccgihaeeihggegebgehhehhfafdhffcdbfcccgfeggecdcifffgigeea'}
def lcs(a,b):
    # longest common substring via DP (small)
    best=0;prev=[0]*(len(b)+1)
    for i in range(1,len(a)+1):
        cur=[0]*(len(b)+1)
        for j in range(1,len(b)+1):
            if a[i-1]==b[j-1]:
                cur[j]=prev[j-1]+1
                if cur[j]>best: best=cur[j]
        prev=cur
    return best
K=7
idx={n:kmers(s,K) for n,s in targets.items()}
def score(cand_letters):
    """max over targets of longest exact match starting from any K-mer hit"""
    best=(0,'')
    for n,ix in idx.items():
        t=targets[n]
        for i in range(len(cand_letters)-K+1):
            w=cand_letters[i:i+K]
            if w in ix:
                j=ix[w]
                # extend
                L=K
                while i+L<len(cand_letters) and j+L<len(t) and cand_letters[i+L]==t[j+L]: L+=1
                # extend left
                a=i;b=j
                while a>0 and b>0 and cand_letters[a-1]==t[b-1]: a-=1;b-=1;L+=1
                if L>best[0]: best=(L,n)
    return best
def digit_cands(path):
    for line in open(path):
        s=line.strip()
        if s and s.isdigit(): yield s
if __name__=='__main__':
    files=sys.argv[1:]
    res=[]
    for f in files:
        for s in digit_cands(f):
            g=gspace_digits(s)
            res.append((score(g),s))
            # also reverse
            res.append((score(g[::-1]),s[::-1]))
    res.sort(reverse=True)
    print('cands',len(res))
    for r in res[:8]: print(r[0],r[1][:80])
