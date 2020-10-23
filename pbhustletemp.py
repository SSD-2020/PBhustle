from dataclasses import dataclass
import numpy as np
from numpy.fft import fft, ifft
import gspread
from collections import defaultdict

def intdiv(x, y):
    return -(-x // y) if x < 0 else x // y

@dataclass
class Contestant:
    party: str
    points: float
    penalty: int
    rating: int
    need_rating: int = 0
    delta: int = 0
    rank: float = 0.0
    seed: float = 0.0


class CodeforcesRatingCalculator:
    def __init__(self, standing_rows, prev_ratings):
        """Calculate Codeforces rating changes and seeds given contest and user information."""
        self.contestants = [
            Contestant(handle, points, penalty, prev_ratings[handle])
            for handle, _, points, penalty in standing_rows
        ]

        self._precalc_seed()
        self._reassign_ranks()
        self._process()
        self._update_delta()

    def calculate_rating_changes(self):
        """Return a mapping between contestants and their corresponding delta."""
        return {contestant.party: contestant.delta for contestant in self.contestants}

    def get_seed(self, rating, me=None):
        """Get seed given a rating and user."""
        seed = self.seed[rating]
        if me:
            seed -= self.elo_win_prob[rating - me.rating]
        return seed

    def _precalc_seed(self):
        MAX = 6144

        # Precompute the ELO win probability for all possible rating differences.
        self.elo_win_prob = np.roll(1 / (1 + pow(10, np.arange(-MAX, MAX) / 600)), -MAX)

        # Compute the rating histogram.
        count = np.zeros(2 * MAX)
        for a in self.contestants:
            count[a.rating] += 1

        # Precompute the seed for all possible ratings using FFT.
        self.seed = 1 + ifft(fft(count) * fft(self.elo_win_prob)).real

    def _reassign_ranks(self):
        """Find the rank of each contestant."""
        contestants = self.contestants
        contestants.sort(key=lambda o: (-o.points, o.penalty))
        points = penalty = rank = None
        for i in reversed(range(len(contestants))):
            if contestants[i].points != points or contestants[i].penalty != penalty:
                rank = i + 1
                points = contestants[i].points
                penalty = contestants[i].penalty
            contestants[i].rank = rank

    def _process(self):
        """Process and assign approximate delta for each contestant."""
        for a in self.contestants:
            a.seed = self.get_seed(a.rating, a)
            mid_rank = (a.rank * a.seed) ** 0.5
            a.need_rating = self._rank_to_rating(mid_rank, a)
            a.delta = intdiv(a.need_rating - a.rating, 2)

    def _rank_to_rating(self, rank, me):
        """Binary Search to find the performance rating for a given rank."""
        left, right = 1, 8000
        while right - left > 1:
            mid = (left + right) // 2
            if self.get_seed(mid, me) < rank:
                right = mid
            else:
                left = mid
        return left

    def _update_delta(self):
        """Update the delta of each contestant."""
        contestants = self.contestants
        n = len(contestants)

        contestants.sort(key=lambda o: -o.rating)
        correction = intdiv(-sum(c.delta for c in contestants), n) - 1
        for contestant in contestants:
            contestant.delta += correction

        zero_sum_count = min(4 * round(n ** 0.5), n)
        delta_sum = -sum(contestants[i].delta for i in range(zero_sum_count))
        correction = min(0, max(-10, intdiv(delta_sum, zero_sum_count)))
        for contestant in contestants:
            contestant.delta += correction

def predict(rows, prev_ratings):
    calc = CodeforcesRatingCalculator(rows, prev_ratings)
    return calc.calculate_rating_changes()



gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1DHh5jPufmWLyPrYngpORRWAtslzbUA_o_8OBdGI3So4')
total_pages=sh.__sizeof__()
person=defaultdict(list)
prev_rating=defaultdict(int)
for i in range(1,29):
    sheet_ins=sh.get_worksheet(i)
    record = sheet_ins.get_all_records()
    rows=[]
    temp=defaultdict(int)
    name=sheet_ins.title
    print(name)
    rank={}
    for i in record:
        st=""
        for j in i['Who']:
            if(not j.isalnum() and j!="." and j!="_"):
                break
            st+=j
        rows+=[(st,i['#'],i['#ERROR!'],i['Penalty'])]
        rank[st]=i['#']

        if st not in prev_rating:
            temp[st]=500
        else:
            temp[st]=prev_rating[st]

    predicted = predict(rows, temp)
    new_rating=defaultdict(int)
    for i in predicted:
        new_rating[i]=temp[i]+predicted[i]
        prev_rating[i]=new_rating[i]
        person[i]+=[{name:(new_rating[i],rank[i])}]

    #print(new_rating)
#print(prev_rating)
res=[]
for i in person:
    res+=[{i:person[i]}]

print(res)


#user contests
def databaseuse(user):  #return list of all the contest of the user
    res=db.child("PBhustle").child(user).get().val()
    res=res['contests']
    name="PBhustle "
    
    temp=[]
    for i in res:
        val=[str(x) for x in i.split("_")]
        temp+=[(int(val[0]),int(val[1]),i)]
    temp.sort(key=lambda x:(2*x[0],x[1]))
    
    all_contest=[] #contains contest name, contest rank, contest rating
    for i,j,cname in temp:
        all_contest+=[(name+str(i)+"."+str(j),res[cname]['rank'],res[cname]['rating'])]
        
    return all_contest

#pb user graph
def PB_User_graph(user):  
    res=db.child("PBhustle").child(user).get().val()
    res=res['contests']
    name="PBhustle "

    temp=[]
    for i in res:
        val=[str(x) for x in i.split("_")]
        temp+=[(int(val[0]),int(val[1]),i)]
    temp.sort(key=lambda x:(2*x[0],x[1]))

    xd=[]
    yd=[]
    for i,j,cname in temp:
        xd+=[name+str(i)+"."+str(j)]
        yd+=[int(res[cname]['rank'])]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xd, y=yd,
                             mode='lines+markers', name='line+markers', line=dict(color='white', width=1)))

    fig.update_layout(title='Rating Change',yaxis_title='Rating',width=1100,height=500)
    fig.layout.plot_bgcolor = '#32353a'
    fig.layout.paper_bgcolor = '#32353a'
    fig.layout.font = {'color': 'white'}

    plot_div = plot(fig, output_type='div')

    # return render(request, "index.html", context={'plot_div': plot_div})

    return render(request, "index.html", context={'plot_div': plot_div})


#compare table 
def PB_compare(user1,user2): #user1 is admin
    res1=db.child("PBhustle").child(user1).get().val()
    res1=res1['contests']

    res2=db.child("PBhustle").child(user2).get().val()
    res2=res2['contests']

    name="PBhustle "

    user1_rank={}
    temp=[]
    for i in res1:
        val=[str(x) for x in i.split("_")]
        temp+=[(int(val[0]),int(val[1]),i)]
        user1_rank[i]=int(res1[i]['rank'])

    user2_rank={}
    for i in res2:
        if i not in user1_rank:
            val = [str(x) for x in i.split("_")]
            temp += [(int(val[0]), int(val[1]), i)]
        user2_rank[i] = int(res2[i]['rank'])

    temp.sort(key=lambda x:(2*x[0],x[1]))

    common=[] #contains contest name of common contests, rating of both users and there difference
    for i,j,cname in temp:
        if(cname in user1_rank and cname in user2_rank):
            dif=user2_rank[cname]-user1_rank[cname]
            if (dif >= 0):
                dif = '+' + str(dif)
            else:
                dif = str(dif)
            common+=[(name+str(i)+"."+str(j),user1_rank[cname],user2_rank[cname],dif)]

    return common

#compare graph
def PB_compare_graph(user1,user2): #user1 is admin
    res1=db.child("PBhustle").child(user1).get().val()
    res1=res1['contests']

    res2=db.child("PBhustle").child(user2).get().val()
    res2=res2['contests']

    name="PBhustle "

    user1_rank={}
    temp=[]
    for i in res1:
        val=[str(x) for x in i.split("_")]
        temp+=[(int(val[0]),int(val[1]),i)]
        user1_rank[i]=int(res1[i]['rank'])

    user2_rank={}
    for i in res2:
        if i not in user1_rank:
            val = [str(x) for x in i.split("_")]
            temp += [(int(val[0]), int(val[1]), i)]
        user2_rank[i] = int(res2[i]['rank'])

    temp.sort(key=lambda x:(2*x[0],x[1]))

    y_user1=[]
    y_user2=[]
    xd=[]

    for k,j,i in temp:
        xd+=[name+str(k)+"."+str(j)]
        if i in user1_rank:
            y_user1+=[user1_rank[i]]
        else:
            y_user1+=[None]

        if i in user2_rank:
            y_user2+=[user2_rank[i]]
        else:
            y_user2+=[None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xd, y=y_user1, connectgaps=True,
                             mode='lines+markers', name=self.user, line=dict(color='white', width=1)))

    fig.add_trace(go.Scatter(x=xd, y=y_user2, connectgaps=True,
                             mode='lines+markers', name=self.friend, line=dict(color='skyblue', width=1)))

    fig.update_layout(title='Rating Change', yaxis_title='Rating', width=1100, height=500)

    fig.layout.plot_bgcolor = '#32353a'
    fig.layout.paper_bgcolor = '#32353a'
    fig.layout.font = {'color': 'white'}

    plot_div = plot(fig, output_type='div')

    return render(request, "index.html", context={'plot_div': plot_div})