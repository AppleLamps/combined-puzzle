// Exact-prefix search of all invertible affine 2x2 Hill maps mod 9.
// Reuse the previously controlled integer arithmetic, without its entry point.
#define main previous_bifid_entry_point
#include "../../read/SOLVE/bifid-numeric.cpp"
#undef main
#include <numeric>

bool asciiCommon(const vector<uint8_t>& p) {
    return all_of(p.begin(), p.end(), printable);
}

// Every residue zero may be decimal zero OR nine. Branches are pruned only
// when a fixed byte violates the stated ASCII alphabet. Unset suffix digits
// range over all 0..9, a superset of their true possible values.
bool lossyPrefix(const vector<int>& residues, int total, int at=0,
                 vector<int>* work=nullptr) {
    vector<int> local;
    if(!work) work=&local;
    if(at && (at%4==0 || at==int(residues.size()))) {
        auto fixed=commonPrefix(*work,total,10,0);
        if(!asciiCommon(fixed)) return false;
    }
    if(at==int(residues.size())) return true;
    work->push_back(residues[at]);
    if(lossyPrefix(residues,total,at+1,work)) {work->pop_back();return true;}
    if(residues[at]==0) {
        work->back()=9;
        if(lossyPrefix(residues,total,at+1,work)) {work->pop_back();return true;}
    }
    work->pop_back();return false;
}

vector<int> mapped(const vector<int>& source, const array<int,4>& m,
                   int u,int v,bool halvesIn,bool halvesOut,int count) {
    int half=source.size()/2;
    vector<int> result;
    for(int i=0;i<count;i++) {
        int pair=halvesOut?i%half:i/2, axis=halvesOut?i/half:i%2;
        int x=source[halvesIn?pair:2*pair],y=source[halvesIn?pair+half:2*pair+1];
        result.push_back((m[2*axis]*x+m[2*axis+1]*y+(axis?v:u))%9);
    }
    return result;
}

int main(int argc,char**argv) {
    if(argc!=3) {cerr<<"letter-input survivor-jsonl"<<endl;return 2;}
    initPowers(700);
    // Independent control: preserve every ASCII numeral prefix even though
    // all original 9s are now ambiguous zero residues.
    string msg="Restore the zeros before deciding that this is not a message.";
    Big n{0};for(unsigned char c:msg)step(n,256,c);
    vector<int> ds;
    while(n.size()>1||n[0]) {
        uint64_t rem=0;
        for(int i=int(n.size())-1;i>=0;i--){uint64_t x=(rem<<32)|n[i];n[i]=x/10;rem=x%10;}
        trim(n);ds.push_back(rem%9);
    }
    reverse(ds.begin(),ds.end());assert(lossyPrefix(ds,ds.size()));
    ifstream in(argv[1]);vector<int> original;char c;
    while(in.get(c))if(c>='a'&&c<='i')original.push_back((c-'a'+1)%9);
    if(original.size()!=570)return 3;
    ofstream out(argv[2]);uint64_t tested=0,survivors=0;
    for(int rev=0;rev<2;rev++)for(int hi=0;hi<2;hi++)for(int ho=0;ho<2;ho++) {
        auto src=original;if(rev)reverse(src.begin(),src.end());
        for(int a=0;a<9;a++)for(int b=0;b<9;b++)for(int c=0;c<9;c++)for(int d=0;d<9;d++) {
            if(gcd((a*d-b*c+81)%9,9)!=1)continue;
            array<int,4> m{a,b,c,d};
            for(int u=0;u<9;u++)for(int v=0;v<9;v++) {
                tested++;
                auto head=mapped(src,m,u,v,hi,ho,40);
                if(!lossyPrefix(head,570))continue;
                survivors++;auto full=mapped(src,m,u,v,hi,ho,570);
                out<<"{\"reverse\":"<<rev<<",\"halvesIn\":"<<hi<<",\"halvesOut\":"<<ho
                   <<",\"matrix\":["<<a<<","<<b<<","<<c<<","<<d<<"],\"bias\":["<<u<<","<<v
                   <<"],\"residues\":\"";
                for(int z:full)out<<z;
                out<<"\"}\n";
            }
        }
        out.flush();cout<<"group "<<rev<<hi<<ho<<" tested "<<tested<<" prefix survivors "<<survivors<<endl;
    }
    cout<<"COMPLETE models="<<tested<<" survivors="<<survivors<<" control=passed"<<endl;
}
