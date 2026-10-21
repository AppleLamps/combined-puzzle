words=set(w for w in open('words.txt').read().split())
short2={'of','to','in','is','it','be','by','or','as','at','on','so','we','he','me','my','no','up','us','do','go','if','an','am'}
short1={'a','i'}
extra={'throphies','waisting','fourty','sedulously','ciaobellao','youve','thats','havent','ill','im','youll','gsmg','guys','wasting','trophies','hopefully','bullshit','wont','isnt','cant','dont','itll','ive','youre','well','mathematical','precision','anomaly','eventuality','harmony','inexorably','sincerest','concordantly','irrevocably','unbalanced','dissemination','intertwined','ciphers','encryptions','cataclysmic','exterminatio','extermination','exceedingly','predictable','worthless','prices','thropies','sedulously','ciaobella','ciao','bella','pertinent','disseminate','reinserting','basics','waisting','lifetime','hunting','remainder','equation','inherent','programming','sincerest','efforts','unable','eliminate','otherwise','avoid','unexpected','beyond','measure','control','inexorably','answered','quite','interesting','quicker','others','please','complete','private','earned','wise','hinted','worth','hundred','fourty','investment','accomplish','instead','build','sorry','tell','finish','expect','denial','response','rest','assured','destroyed','restless','soul','become','efficient','function','return','source','codes','allowing','temporary','carry','after','which','required','select','over','twenty','three','sixteen','seven','passwords','actual','note','brute','forcing','might','failure','comply','process','result','catastrophic','system','crash','killing','willpower','coupled','extermination','live','ultimately','extinction','entirety','yourself','self','good','luck','nevertheless','really','hope','the','one'}
S3={'the','and','you','are','was','for','not','but','all','can','one','our','out','who','how','why','its','has','had','him','his','her','she','may','now','new','use','way','get','see','any','end','let','try','too','yet','saw','sum','key','say','man','men','set','far','few','act','age','ago','bad','big','buy','cut','did','eat','got','law','low','lot','met','off','old','own','pay','ran','run','sea','sit','son','sun','ten','war','win','won','yes','ill','arc','sad','die','put','lie','job','god','air','mad'}
def ok(w):
    if w in {'im','youve','thats','havent','ill','ive','youre','youll','wont','dont','isnt','hasnt','ciaobellao','throphies','waisting','fourty'}: return True
    if len(w)==1: return w in short1
    if len(w)==2: return w in short2
    if len(w)==3: return w in S3 or w in words
    return w in extra or w in words
A=open('architect.txt').read(); n=len(A)
INF=10**9
best=[INF]*(n+1); prev=[0]*(n+1); best[0]=0
for i in range(n):
    if best[i]>=INF: continue
    for L in range(1,20):
        if i+L>n: break
        w=A[i:i+L]
        if ok(w):
            c=best[i]+1+(0.5 if L<=2 else 0)+(0.8 if (L==3 and w not in S3) else 0)
            if c<best[i+L]: best[i+L]=c; prev[i+L]=L
        elif L>=4:
            c=best[i]+6+L*0.2
            if c<best[i+L]: best[i+L]=c; prev[i+L]=L
i=n; seg=[]
while i>0:
    L=prev[i]
    if L==0: print('fail at',i); break
    seg.append(A[i-L:i]); i-=L
seg=seg[::-1]
print(len(seg)); print(' '.join(seg))
open('arch_words.txt','w').write(' '.join(seg))
