# Class
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

        for i in content:
            if(i in ['rating', 'stars', 'highest_rating', 'global_rank', 'country_rank']):
                self.user_info[i]=content[i]

        for i in content['user_details']:
            self.user_info[i]=content['user_details'][i]

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



class Codeforces:

    def __init__(self,user_id):

        self.user_id=user_id
        self.user_info={}
        self.user_contests=[]
        self.user_valid=False
        self.plot=0


    def fetch_data(self):

        # USER INFORMATION

        url= "https://codeforces.com/api/user.info?handles=" + self.user_id
        r=requests.get(url)
        data_codeforces=r.json()

        if(data_codeforces['status']!='OK'): return
        self.user_valid=True
        
        self.user_info=data_codeforces['result'][0]


        # USER CONTESTS

        url=" https://codeforces.com/api/user.rating?handle=" + self.user_id
        r=requests.get(url)
        contests=r.json()

        self.user_contests=contests['result']
        last=self.user_contests[0]['newRating']

        for data in self.user_contests:

            del data['ratingUpdateTimeSeconds']
            del data['oldRating']
            del data['handle']

            data['ratingChange']=data['newRating']-last

            if(data['ratingChange']>=0): data['ratingChange']='+'+str(data['ratingChange'])
            else: data['ratingChange']=str(data['ratingChange'])

            last=data['newRating']

    def plot_data(self):

        xd=[]
        yd=[]
        c=1

        
        for i in self.user_contests:
            xd.append(c)
            yd.append(i['newRating'])
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
            xaxis_title='Contest',
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



# CF_user=Codeforces('deepanshu_pali')
# CF_user.fetch_data()
# CF_user.plot_data()

# print(CF_user.user_valid)
# print()

# print(CF_user.user_info)
# print()

# print(CF_user.user_contests)
# print()
