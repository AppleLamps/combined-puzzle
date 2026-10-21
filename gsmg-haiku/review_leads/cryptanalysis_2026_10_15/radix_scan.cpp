#include <bits/stdc++.h>
using namespace std;using u64=uint64_t;using u128=__uint128_t;
struct Big{array<u64,29>w{};void digit(int d){u128 carry=d;for(int i=0;i<29;i++){carry+=u128(w[i])*9;w[i]=u64(carry);carry>>=64;}}};
struct Row{array<int,3> k;vector<int>d;u64 prefix;Big value;};
bool textbyte(int c){return (c>=32&&c<=126)||c==9||c==10||c==13;}
bool print7(u64 v){for(int i=0;i<7;i++){int c=v&255;if(!textbyte(c))return false;v>>=8;}return v==0;}
string hexify(vector<unsigned char>&b){ostringstream s;s<<hex<<setfill('0');for(int x:b)s<<setw(2)<<x;return s.str();}
int main(int argc,char**argv){string root=argv[1];u64 coef;ifstream cf(root+"/radix_coef.txt");cf>>coef;
 string mode=argc>2?argv[2]:"ring";int add[9][9],mul[9][9],neg[9];
 for(int x=0;x<9;x++)for(int y=0;y<9;y++){
  if(mode=="ring"){add[x][y]=(x+y)%9;mul[x][y]=x*y%9;}
  else{int b=mode[0]-'0',c=mode[1]-'0',x0=x%3,x1=x/3,y0=y%3,y1=y/3;
   add[x][y]=(x0+y0)%3+3*((x1+y1)%3);mul[x][y]=((x0*y0-c*x1*y1)%3+3)%3+3*(((x0*y1+x1*y0-b*x1*y1)%3+6)%3);
  }
 }
 for(int x=0;x<9;x++)for(int y=0;y<9;y++)if(add[x][y]==0)neg[x]=y;
 ifstream in(root+"/radix_models_"+mode+".txt");ofstream out(root+"/radix_scan_"+mode+".tsv");string name,t;
 while(in>>name>>t){vector<int> v;for(char c:t)v.push_back(c-'0');if(v.size()!=570)return 2;
  u64 pw[20];pw[19]=1;for(int i=18;i>=0;i--)pw[i]=9*pw[i+1];vector<Row> rows[3];
  for(int phase=0;phase<3;phase++)for(int a=0;a<9;a++)for(int b=0;b<9;b++)for(int c=0;c<9;c++){
   Row r;r.k={a,b,c};r.prefix=0;
   for(int j=0;j<190;j++){int x=add[add[mul[a][v[3*j]]][mul[b][v[3*j+1]]]][mul[c][v[3*j+2]]];r.d.push_back(x);int pos=3*j+phase;if(pos<20)r.prefix+=pw[pos]*x;for(int k=0;k<3;k++)r.value.digit(k==phase?x:0);}rows[phase].push_back(move(r));
  }
  long total=0,passed=0,units=0,fullprint=0;int best=0;vector<string> bestrows;
  for(auto&a:rows[0])for(auto&b:rows[1])for(auto&c:rows[2]){
   total++;u64 p=a.prefix+b.prefix+c.prefix;
   // True top7 for a full 226-byte result is within [floor(p*C),floor((p+1)*C)+1].
   u64 lo=(u128(p)*coef)>>64,hi=((u128(p+1)*coef)>>64)+1;
   bool ok=false;
   if(lo<(u64(1)<<48))ok=true; // Shorter byte lengths are checked exactly, never discarded.
   else for(u64 z=lo;z<=hi;z++)if(print7(z)){ok=true;break;}
   if(!ok)continue;passed++;
   auto x=a.k,y=b.k,z=c.k;
   int e0=mul[x[0]][add[mul[y[1]][z[2]]][neg[mul[y[2]][z[1]]]]];
   int e1=mul[x[1]][add[mul[y[0]][z[2]]][neg[mul[y[2]][z[0]]]]];
   int e2=mul[x[2]][add[mul[y[0]][z[1]]][neg[mul[y[1]][z[0]]]]];
   int det=add[add[e0][neg[e1]]][e2];if(mode=="ring"?det%3==0:det==0)continue;units++;
   Big n;u128 carry=0;for(int i=0;i<29;i++){carry+=u128(a.value.w[i])+b.value.w[i]+c.value.w[i];n.w[i]=u64(carry);carry>>=64;}vector<unsigned char> bytes;bool started=false;for(int i=231;i>=0;i--){int byte=(n.w[i/8]>>(8*(i%8)))&255;if(byte||started){bytes.push_back(byte);started=true;}}int prefix=0;for(int x:bytes){if(!textbyte(x))break;prefix++;}
   bool all=prefix==(int)bytes.size();if(all)fullprint++;
   bool special=bytes.size()<=128||(bytes.size()>=8&&string(bytes.begin(),bytes.begin()+8)=="Salted__");
   if(prefix>=best||all||special){ostringstream key;for(auto row:{a.k,b.k,c.k})for(int x:row)key<<x;string line=name+"\t"+key.str()+"\t"+to_string(prefix)+"\t"+to_string(bytes.size())+"\t"+hexify(bytes);if(prefix>best){best=prefix;bestrows.clear();}if(prefix==best&&bestrows.size()<20)bestrows.push_back(line);if(all||special)out<<line<<'\n';}
  }
  for(auto&line:bestrows)out<<line<<'\n';out.flush();cout<<name<<" total="<<total<<" prefix_pass="<<passed<<" invertible_survivors="<<units<<" full_printable="<<fullprint<<" best_prefix="<<best<<endl;
 }
}
