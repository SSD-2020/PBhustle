from collections import defaultdict
import requests
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go

class CodeforceCompare:

    def __init__(self,user,friend):
        self.user=user
        self.friend=friend
        self.compare_result=[]
        self.friend_valid=False
        self.plot=0

    def compare(self):

        url=" https://codeforces.com/api/user.rating?handle="+self.user
        r=requests.get(url)
        contests=r.json()

        user_contests=contests['result']

        
        url=" https://codeforces.com/api/user.rating?handle="+self.friend
        r=requests.get(url)
        contests=r.json()


        if(contests['status']!='OK'): return 
        self.friend_valid=True


        friend_contests=contests['result']
        d=defaultdict(int)

        for i in user_contests:
            d[i['contestId']]=i['rank']
        

        for i in friend_contests:
            if i['contestId'] in d:

                dif=i['rank']-d[i['contestId']]
                if(dif>=0): dif='+'+str(dif)
                else: dif=str(dif)

                self.compare_result.append([i['contestId'],i['contestName'],d[i['contestId']],i['rank'],dif])



        all_Contest=[]
        temp=[]

        user1_rank={}
        for i in user_contests:
            cno=i['contestId']
            time=i['ratingUpdateTimeSeconds']
            all_Contest.append((cno,time))
            user1_rank[cno]=i['newRating']
            temp.append(cno)


        user2_rank={}
        for i in friend_contests:
            cno=i['contestId']
            time=i['ratingUpdateTimeSeconds']
            if cno not in temp: 
                all_Contest.append((cno,time))
                temp.append(cno)
            user2_rank[cno]=i['newRating']

        y_user1=[]
        y_user2=[]

        #print(all_Contest)
        all_Contest.sort(key=lambda x:x[1])

        #print(all_Contest)

        for i,_ in all_Contest:
            if i in user1_rank:
                y_user1.append(user1_rank[i])
            else:
                y_user1.append(None)
            
            if i in user2_rank:
                y_user2.append(user2_rank[i])
            else:
                y_user2.append(None)

        xd=[i for i in range(1,len(all_Contest)+1)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xd, y=y_user1, connectgaps=True,
                    mode='lines+markers',name=self.user,line = dict(color='white', width=1)))

        
        fig.add_trace(go.Scatter(x=xd, y=y_user2, connectgaps=True,
                    mode='lines+markers',name=self.friend,line = dict(color='white', width=1)))

        fig.update_layout(title='Rating Change',yaxis_title='Rating')

        fig.layout.plot_bgcolor = '#32353a'
        fig.layout.paper_bgcolor = '#32353a'
        fig.layout.font={'color':'white'}

        self.plot=plot(fig, output_type='div')