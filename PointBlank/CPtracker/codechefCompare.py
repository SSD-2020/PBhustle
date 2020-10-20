from collections import defaultdict
import requests
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go


class CodechefCompare:

    def __init__(self,user,friend):
        self.user=user
        self.friend=friend
        self.compare_result=[]
        self.friend_valid=False
        self.plot=0

    def compare(self):
        url='https://competitive-coding-api.herokuapp.com/api/codechef/'+self.user
        r = requests.get(url)
        content = r.json()
        if (content['status'] != 'Success'): return -1
        user1=content['contest_ratings']

        url = 'https://competitive-coding-api.herokuapp.com/api/codechef/'+self.friend
        r = requests.get(url)
        content = r.json()
        if (content['status'] != 'Success'): return -1
        user2 = content['contest_ratings']

        #compare contests
        d = defaultdict(int)
        for i in user1:
            d[i['code']] = i['rank']

        for i in user2:
            if i['code'] in d:

                dif=int(i['rank']) - int(d[i['code']])
                if(dif>=0): dif='+'+str(dif)
                else: dif=str(dif)
                    
                self.compare_result.append((i['code'], i['name'], int(d[i['code']]),int(i['rank']),dif))
                            

        all_contest=[]
        temp=[]
        user1_rank={}
        for i in user1:
            val=i['code']
            all_contest.append([val,int(i['getyear']),int(i['getmonth']),int(i['getday'])])
            temp.append(val)
            user1_rank[val]=int(i['rating'])

        user2_rank={}
        for i in user2:
            val=i['code']
            if val not in temp:
                all_contest.append([val,int(i['getyear']),int(i['getmonth']),int(i['getday'])])
                temp.append(val)
            user2_rank[val]=int(i['rating'])

        contest=sorted(all_contest, key=lambda x: (x[1]*3,x[2]*2,x[3]))

        xd=[]
        for i in contest:
            xd.append(i[0])

        #print(xd)

        y_user1=[]
        y_user2=[]

        for i in xd:
            if i in user1_rank:
                y_user1.append(user1_rank[i])
            else:
                y_user1.append(None)

            if i in user2_rank:
                y_user2.append(user2_rank[i])
            else:
                y_user2.append(None)

        #print(y_user1)
        #print(y_user2)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xd, y=y_user1, connectgaps=True,
                                mode='lines+markers', name='deepanshu_pali', line=dict(color='black', width=1)))

        fig.add_trace(go.Scatter(x=xd, y=y_user2, connectgaps=True,
                                mode='lines+markers', name='sumitthakur', line=dict(color='blue', width=1)))

        fig.update_layout(title='Rating Change',
                        yaxis_title='Rating')

        self.plot = plot(fig, output_type='div')