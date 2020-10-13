#function to extract the codeforces user data
import requests

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