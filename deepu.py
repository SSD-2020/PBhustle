import requests

def GetContestIDs():
    
    url='https://competitive-coding-api.herokuapp.com/api/codechef/deepu217'
    r=requests.get(url)

    content=r.json()
    
    info={}
    contests=[]

    for contest in content['contest_ratings']:
        
        here={}
        for key in contest:
            if(key in ['code','rating', 'rank', 'name']):
                here[key]=contest[key]

        contests.append(here)

    for i in content:
        if(i in ['rating', 'stars', 'highest_rating', 'global_rank', 'country_rank']):
            info[i]=content[i]

    for i in content['user_details']:
        info[i]=content['user_details'][i]


GetContestIDs()