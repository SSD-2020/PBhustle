from collections import defaultdict
import requests
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go

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
        
        temp=data_codeforces['result'][0]
        # print(temp)

        try: temp['lastName']=temp['lastName']
        except: temp['lastName']=" "

        try: temp['firstName']=temp['firstName']
        except: temp['firstName']="[ Not Given On Codeforces ]"



        self.user_info={

            "User Handle" : temp['handle'],
            "Name" : temp['firstName']+' '+temp['lastName'],
            "Current Rating" : str(temp['rating'])+ ' ( ' + temp['rank'] +' )',
            "Maximum Rating" : str(temp['maxRating'])+ ' ( ' + temp['maxRank'] +' )',

        }


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
            line = dict(color='white', width=1)
            )
        )

        fig.update_layout(
            xaxis_title='Contest',
            yaxis_title='Rating'
            )

        fig.layout.plot_bgcolor = '#32353a'
        fig.layout.paper_bgcolor = '#32353a'
        fig.layout.font={'color':'white'}
        
        self.plot=plot(fig, output_type='div')



# CF_user=Codeforces('sparshkesari98')
# CF_user.fetch_data()
# CF_user.compare('sumitthakur')
# CF_user.plot_data()

# print(CF_user.user_valid)
# print()

# print(CF_user.user_info)
# print()

# print(CF_user.compare_result)
# print()