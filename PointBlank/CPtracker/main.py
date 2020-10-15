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


        from collections import defaultdict
    

class Compare:

    def __init__(self,user,friend):
        self.user=user
        self.friend=friend
        self.compare_result=[]
        self.friend_valid=False
        self.CFplot=0
        self.CCplot=0

    def CFcompare(self):

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
                    mode='lines+markers',name=self.user,line = dict(color='black', width=1)))

        
        fig.add_trace(go.Scatter(x=xd, y=y_user2, connectgaps=True,
                    mode='lines+markers',name=self.friend,line = dict(color='blue', width=1)))

        fig.update_layout(title='Rating Change',yaxis_title='Rating')

        self.CFplot=plot(fig, output_type='div')

        

    def CCcompare(self):
        
        pass






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
# CF_user.compare('sumitthakur')
# CF_user.plot_data()

# print(CF_user.user_valid)
# print()

# print(CF_user.user_info)
# print()

# print(CF_user.compare_result)
# print()
