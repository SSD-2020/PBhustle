from collections import defaultdict
import requests
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go

class Codechef:

    def __init__(self,user_id):

        self.user_id=user_id
        self.user_info={}
        self.user_contests=[]
        self.user_valid=False
        self.plot=0


    def fetch_data(self):

        url='https://competitive-coding-api.herokuapp.com/api/codechef/' + self.user_id
        content=requests.get(url).json()

        if(content['status']!='Success'):  return
        self.user_valid=True


        # USER INFORMATION 

        temp={}
        for i in content:
            if(i in ['rating', 'stars', 'highest_rating', 'global_rank', 'country_rank']):
                temp[i]=content[i]

        for i in content['user_details']:
            temp[i]=content['user_details'][i]


        self.user_info={

            "User Handle" : temp['username'],
            "Name" : temp['name'],
            "Current Rating" : temp['rating'],
            "Maximum Rating" : temp['highest_rating'],

        }
        # USER CONTESTS
        temp=[]

        for contest in content['contest_ratings']:
            
            here={}
            for key in contest:
                if(key in ['code','rating', 'rank', 'name']):
                    here[key]=contest[key]

            temp.append(here)

        last=int(temp[0]['rating'])

        for contest in temp:

            here={}

            here['code']=contest['code']
            here['name']=contest['name']
            here['rank']=contest['rank']
            here['rating']=int(contest['rating'])
            here['change']=here['rating']-last
            last=here['rating']

            if(here['change']>=0): here['change']='+'+str(here['change'])
            else: here['change']=str(here['change'])

            self.user_contests.append(here)

    def plot_data(self):
        
        xd=[]
        yd=[]
        c=1
        
        for i in self.user_contests:
            xd.append(c)
            yd.append(i['rating'])
            c+=1
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=xd, 
            y=yd,
            mode='lines+markers',
            name='lines+markers',
            line = dict(color='black', width=1)
            )
        )

        fig.update_layout(
            xaxis_title='Contests',
            yaxis_title='Rating'
            )

        self.plot=plot(fig, output_type='div')



# CC_user=Codechef('deepu217')
# CC_user.fetch_data()

# print(CC_user.user_valid)
# print()

# print(CC_user.user_info)
# print()

# print(CC_user.user_contests)
# print()
