import requests
import matplotlib.pyplot as plt
def User_Codeforces_Contests():
    url=" https://codeforces.com/api/user.rating?handle=deepanshu_pali"
    r=requests.get(url)

    contests=r.json()

    if(contests['status']!='OK'): return -1

    contests=contests['result']
    x=[]
    y=[]
    c=1
    for i in contests:
        x+=[c]
        y+=[i['newRating']]
        c+=1
    #print(x)
    #print(y)
    plt.style.use('seaborn-whitegrid')
    plt.figure(figsize=(len(x), len(y)))
    plt.plot(x, y, color='green', linestyle='dashed', linewidth=3,
             marker='o', markerfacecolor='blue', markersize=12)
    plt.xlabel('contest Number')
    plt.ylabel('Rating')
    plt.savefig('sumitpb.jpg')
    plt.show()
User_Codeforces_Contests()