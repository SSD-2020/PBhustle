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

class PBhustle:

    def __init__(self,user_id):

        self.user_id=user_id
        self.user_info={}
        self.user_contests=[]
        self.user_valid=False
        self.plot=0

    def fetch_data(self):
        #user contests
        res=db.child("PBhustle").child(self.user_id).get().val()
        res=res['contests']
        name="PBhustle "
        
        temp=[]
        for i in res:
            val=[str(x) for x in i.split("_")]
            temp+=[(int(val[0]),int(val[1]),i)]
        temp.sort(key=lambda x:(2*x[0],x[1]))
        
        for i,j,cname in temp:
            self.user_contests+=[(name+str(i)+"."+str(j),res[cname]['rank'],res[cname]['rating'])]

        
    def plot_data(self):

        xd=[]
        yd=[]

        for i in self.user_contests:
            xd.append(i[0])
            yd.append(i[2])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=xd, 
            y=yd,
            mode='lines+markers',
            name=self.user_id,
            line = dict(color='white', width=1)
            )
        )

        fig.update_layout(
            xaxis_title='Contest',
            yaxis_title='Rating',
            width=1100,
            height=500
            )

        fig.layout.plot_bgcolor = '#32353a'
        fig.layout.paper_bgcolor = '#32353a'
        fig.layout.font={'color':'white'}

        self.plot=plot(fig, output_type='div')
        