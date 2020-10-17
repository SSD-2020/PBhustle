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
            line = dict(color='black', width=1)
            )
        )

        fig.update_layout(
            xaxis_title='Contest',
            yaxis_title='Rating'
            )

        self.plot=plot(fig, output_type='div')


        from collections import defaultdict
    

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
                    mode='lines+markers',name=self.user,line = dict(color='black', width=1)))

        
        fig.add_trace(go.Scatter(x=xd, y=y_user2, connectgaps=True,
                    mode='lines+markers',name=self.friend,line = dict(color='blue', width=1)))

        fig.update_layout(title='Rating Change',yaxis_title='Rating')

        self.plot=plot(fig, output_type='div')

        

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


    





# CC_user=Codechef('deepu217')
# CC_user.fetch_data()

# print(CC_user.user_valid)
# print()

# print(CC_user.user_info)
# print()

# print(CC_user.user_contests)
# print()



CF_user=Codeforces('deepanshu_pali')
CF_user.fetch_data()
# CF_user.compare('sumitthakur')
# CF_user.plot_data()

# print(CF_user.user_valid)
# print()

# print(CF_user.user_info)
# print()

# print(CF_user.compare_result)
# print()
