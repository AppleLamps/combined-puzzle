#include <bits/stdc++.h>
using namespace std;
struct Result { double s; array<int,4> k; string t; bool operator<(const Result&o)const{return s<o.s;} };
int main(int argc,char**argv){
 string root=argv[1]; vector<double> q(26*26*26*26);ifstream qf(root+"/quadgrams.bin",ios::binary);qf.read((char*)q.data(),q.size()*8);if(!qf)return 2;
 ifstream in(root+"/hill_models.txt");ofstream out(root+"/hill_scan.tsv");string name,t;
 string A="abcdefghiklmnopqrstuvwxyz";int z[25];for(int i=0;i<25;i++)z[i]=A[i]-'a';
 while(in>>name>>t){
  int n=t.size();vector<int> v;for(char c:t)v.push_back(A.find(c));if(n%2)return 3;
  vector<vector<int>> rows(625,vector<int>(n/2));
  for(int a=0;a<25;a++)for(int b=0;b<25;b++)for(int j=0;j<n/2;j++)rows[a*25+b][j]=(a*v[2*j]+b*v[2*j+1])%25;
  vector<Result> best;long count=0;vector<int> p(n);
  for(int a=0;a<25;a++)for(int b=0;b<25;b++)for(int c=0;c<25;c++)for(int d=0;d<25;d++){
   if(gcd((a*d-b*c+625)%25,25)!=1)continue;count++;
   for(int j=0;j<n/2;j++){p[2*j]=z[rows[a*25+b][j]];p[2*j+1]=z[rows[c*25+d][j]];}
   double s=0;int skip=name.find("tail_")==0?6:0;
   for(int j=skip;j<n-3;j++)s+=q[((p[j]*26+p[j+1])*26+p[j+2])*26+p[j+3]];
   s/=(n-3-skip);
   if(best.size()<10||s>best.back().s){string text;for(int x:p)text+=char('a'+x);best.push_back({s,{a,b,c,d},text});sort(best.begin(),best.end(),[](auto&x,auto&y){return x.s>y.s;});if(best.size()>10)best.pop_back();}
  }
  for(auto&r:best)out<<name<<'\t'<<setprecision(14)<<r.s<<'\t'<<r.k[0]<<','<<r.k[1]<<','<<r.k[2]<<','<<r.k[3]<<'\t'<<r.t<<'\n';out.flush();
  cout<<name<<" keys="<<count<<" best="<<best[0].s<<" text="<<best[0].t.substr(0,80)<<endl;
 }
}
