from reconstruct import *
import random
def base_digits(n,b):
    out=[]
    while n:out.append(n%b);n//=b
    return out[::-1] or [0]
control=('returntothebeginningandreadtheentiremessagebeforeyoudecidewhichpartofthecalculationisimportantthecorrectproceduremustpreserveallthecharactersandmustreconstructtheoriginalciphertextwithoutinventinganotherexception')
control=(control+'eachstepmustbecheckedagainsttheinputandtheknownanswer')[:226];assert len(control)==226
digits=base_digits(int.from_bytes(control.encode(),'big'),9);assert len(digits)<=570
digits=[0]*(570-len(digits))+digits
K=((1,2,3),(0,1,4),(0,0,1));cipher=[]
for i in range(0,len(digits),3):
    cipher += [sum(a*b for a,b in zip(row,digits[i:i+3]))%9 for row in K]
models={'natural0':[ord(c)-97 for c in faed],'natural1':[ (ord(c)-96)%9 for c in faed],'dbbi0':['dbifhcega'.index(c) for c in faed],'forward_control':cipher}
(R/'radix_models.txt').write_text('\n'.join(k+' '+''.join(map(str,v)) for k,v in models.items())+'\n')
(R/'radix_models_ring.txt').write_text((R/'radix_models.txt').read_text())
for b in range(3):
    for c in range(3):
        if any((x*x+b*x+c)%3==0 for x in range(3)):continue
        def add(x,y):return (x%3+y%3)%3+3*((x//3+y//3)%3)
        def mul(x,y):
            x0,x1=x%3,x//3;y0,y1=y%3,y//3
            return (x0*y0-c*x1*y1)%3+3*((x0*y1+x1*y0-b*x1*y1)%3)
        cipher=[]
        for i in range(0,len(digits),3):
            for row in K:
                v=0
                for x,y in zip(row,digits[i:i+3]):v=add(v,mul(x,y))
                cipher.append(v)
        mod=dict(models);mod['forward_control']=cipher
        (R/f'radix_models_{b}{c}.txt').write_text('\n'.join(k+' '+''.join(map(str,v)) for k,v in mod.items())+'\n')
# Conservative top-7-byte fixed point bounds. Coefficient A=9^550/256^219.
num=9**550;den=256**219;coef=(num*(1<<64))//den
(R/'radix_coef.txt').write_text(str(coef)+'\n')
(R/'radix_control.json').write_text(json.dumps(dict(plaintext=control,key=K,digits=digits,cipher=cipher,coefficient=coef,coefficient_ratio=str(num)+'/'+str(den)),indent=2))
print('control',len(digits),'digits',len(control),'bytes','coefficient',coef)
