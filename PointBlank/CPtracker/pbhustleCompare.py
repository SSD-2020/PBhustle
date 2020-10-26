from collections import defaultdict
import requests
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go
import pyrebase

firebaseConfig = {
            'apiKey': "AIzaSyAIuua7NGadNu4dHChW0hYGHLApMW_XVOE",
            'authDomain': "pbhustle-702d9.firebaseapp.com",
            'databaseURL': "https://pbhustle-702d9.firebaseio.com",
            'projectId': "pbhustle-702d9",
            'storageBucket': "pbhustle-702d9.appspot.com",
            'messagingSenderId': "63903745303",
            'appId': "1:63903745303:web:1f610bfc6f8df057e52352",
            'measurementId': "G-YKZE3DKT4Z"
        }
db=pyrebase.initialize_app(firebaseConfig).database()

class PBhustleCompare:

    def __init__(self,user,friend):
        self.user=user
        self.friend=friend
        self.compare_result=[]
        self.friend_valid=False
        self.plot=0

    def compare(self):

        res1=db.child("PBhustle").child(self.user).get().val()
        res1=res1['contests']

        try:
            res2=db.child("PBhustle").child(self.friend).get().val()
            res2=res2['contests']
        except: return

        self.friend_valid=True

        name="PBhustle "
        user1_rank={}
        temp=[]
        for i in res1:
            val=[str(x) for x in i.split("_")]
            temp+=[(int(val[0]),int(val[1]),i)]
            user1_rank[i]=int(res1[i]['rating'])

        user2_rank={}
        for i in res2:
            if i not in user1_rank:
                val = [str(x) for x in i.split("_")]
                temp += [(int(val[0]), int(val[1]), i)]
            user2_rank[i] = int(res2[i]['rating'])

        temp.sort(key=lambda x:(2*x[0],x[1]))

        for i,j,cname in temp:
            if(cname in user1_rank and cname in user2_rank):
                dif=user1_rank[cname]-user2_rank[cname]
                if (dif >= 0):
                    dif = '+' + str(dif)
                else:
                    dif = str(dif)
                self.compare_result.append([name+str(i)+"."+str(j),user1_rank[cname],user2_rank[cname],dif])

        y_user1=[]
        y_user2=[]
        xd=[]

        for k,j,i in temp:
            xd+=[name+str(k)+"."+str(j)]
            if i in user1_rank:
                y_user1+=[user1_rank[i]]
            else:
                y_user1+=[None]

            if i in user2_rank:
                y_user2+=[user2_rank[i]]
            else:
                y_user2+=[None]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xd, y=y_user1, connectgaps=True,
                    mode='lines+markers',name=self.user,line = dict(color='white', width=1)))

        
        fig.add_trace(go.Scatter(x=xd, y=y_user2, connectgaps=True,
                    mode='lines+markers',name=self.friend,line = dict(color='skyblue', width=1)))
        fig.update_layout(title='Rating Change',yaxis_title='Rating',width=1100,height=500)

        fig.layout.plot_bgcolor = '#32353a'
        fig.layout.paper_bgcolor = '#32353a'
        fig.layout.font={'color':'white'}

        self.plot=plot(fig, output_type='div')