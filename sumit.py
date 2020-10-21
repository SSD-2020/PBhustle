#function to extract the codeforces user data
import requests
#esdvn.sd
def Codeforces_User():

    url= "https://codeforces.com/api/user.info?handles=sumitthakur"
    r=requests.get(url)

    data_codeforces=r.json()

    if(data_codeforces['status']!='OK'): return -1

    data_codeforces=data_codeforces['result'][0]

    print(data_codeforces)
    #return data_codeforces

def User_Codeforces_Contests():
    url=" https://codeforces.com/api/user.rating?handle=sumitthakur"
    r=requests.get(url)

    contests=r.json()

    if(contests['status']!='OK'): return -1

    contests=contests['result']

    #print(contests)
    for data in contests:

        del data['ratingUpdateTimeSeconds']
        del data['oldRating']
        del data['handle']

    print(contests)

    #print(contests)

    #return contests
User_Codeforces_Contests()

from django.shortcuts import render
from django.http import HttpResponse
from plotly.offline import plot
from plotly.graph_objs import Scatter
import requests
import plotly.graph_objects as go
# Create your views here.

def index(request):
    url=" https://codeforces.com/api/user.rating?handle=deepanshu_pali"
    r=requests.get(url)
    contests=r.json()
    if(contests['status']!='OK'): return -1
    user1=contests['result']
    
    #print(user1)

    url=" https://codeforces.com/api/user.rating?handle=sumitthakur"
    r=requests.get(url)
    contests=r.json()
    if(contests['status']!='OK'): return -1
    user2=contests['result']
    
    all_Contest=[]
    temp=[]

    user1_rank={}
    for i in user1:
        cno=i['contestId']
        time=i['ratingUpdateTimeSeconds']
        all_Contest.append((cno,time))
        user1_rank[cno]=i['newRating']
        temp.append(cno)


    user2_rank={}
    for i in user2:
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

    for i,j in all_Contest:
        if i in user1_rank:
            y_user1.append(user1_rank[i])
        else:
            y_user1.append(None)
        
        if i in user2_rank:
            y_user2.append(user2_rank[i])
        else:
            y_user2.append(None)

    xd=[i for i in range(1,len(all_Contest)+1)]

    #print(len(y_user1),len(y_user2),len(xd))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xd, y=y_user1, connectgaps=True,
                mode='lines+markers',name='deepanshu_pali',line = dict(color='black', width=1)))

    
    fig.add_trace(go.Scatter(x=xd, y=y_user2, connectgaps=True,
                mode='lines+markers',name='sumitthakur',line = dict(color='blue', width=1)))

    fig.update_layout(title='Rating Change',
                   yaxis_title='Rating')

    plot_div=plot(fig, output_type='div')

    #print(plot_div)
    return render(request, "index.html", context={'plot_div':plot_div})

#index("1234")

#function to compare between 3 users
from collections import defaultdict
def same_contest():

    url=" https://codeforces.com/api/user.rating?handle=sparshkesari98"
    r=requests.get(url)
    contests=r.json()
    if(contests['status']!='OK'): return -1
    user1=contests['result']
    

    url=" https://codeforces.com/api/user.rating?handle=sumitthakur"
    r=requests.get(url)
    contests=r.json()
    if(contests['status']!='OK'): return -1
    user2=contests['result']

    #user1 is admin

    d=defaultdict(int)
    for i in user1:
        d[i['contestId']]=i['newRating']
    
    common=[] # contains (contestId,contestname,userrating,2nd userrating, difference of rating)

    for i in user2:
        if i['contestId'] in d:
            common.append((i['contestId'],i['contestName'],d[i['contestId']],i['newRating'],d[i['contestId']]-i['newRating']))

    # print(common)

#codechef compare
def codechef_compare(request):
    url='https://competitive-coding-api.herokuapp.com/api/codechef/abhi1702'
    r = requests.get(url)
    content = r.json()
    if (content['status'] != 'Success'): return -1
    user1=content['contest_ratings']

    url = 'https://competitive-coding-api.herokuapp.com/api/codechef/suanmj18'
    r = requests.get(url)
    content = r.json()
    if (content['status'] != 'Success'): return -1
    user2 = content['contest_ratings']

    #print(user2)

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

    #print(contest)

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

    plot_div = plot(fig, output_type='div')

    #return render(request, "index.html", context={'plot_div': plot_div})

    return render(request,"index.html",context={'plot_div':plot_div})

#pb hustle_contest
import gspread

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1DHh5jPufmWLyPrYngpORRWAtslzbUA_o_8OBdGI3So4')
sheet_ins=sh.get_worksheet(3)
#print(sheet_ins.col_count)
record = sheet_ins.get_all_records()
for i in record:
    print(i)
    print()
