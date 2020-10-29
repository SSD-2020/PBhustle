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



class standings:

    def __init__(self):

        self.CF_Standings=[]
        self.CC_Standings=[]
        self.PB_Standings=[]
        self.ratings=[]



    def codeforces(self):

        self.ratings=db.child('Ratings').get().val()
        self.CF_Standings.clear()
        for id in self.ratings:
            
            name=db.child('users').child(id).child('name').get().val()
            handle=db.child('users').child(id).child('CF_id').get().val()
            rating=self.ratings[id]['CF']

            self.CF_Standings.append([name,handle,rating])

        self.CF_Standings.sort(key= lambda x: int(x[2][:x[2].index(' ')]),reverse=True)

        j=0
        while( j<len(self.CF_Standings) and   self.CF_Standings[j][2]!='-10000 '): j+=1
        self.CF_Standings=self.CF_Standings[:j]
        


    def codechef(self):

        self.ratings=db.child('Ratings').get().val()
        self.CC_Standings.clear()

        for id in self.ratings:
            
            name=db.child('users').child(id).child('name').get().val()
            handle=db.child('users').child(id).child('CC_id').get().val()
            rating=self.ratings[id]['CC']

            self.CC_Standings.append([name,handle,rating])

        self.CC_Standings.sort(key= lambda x: x[2],reverse=True)

        j=0
        while( j<len(self.CC_Standings) and   self.CC_Standings[j][2]!=-10000): j+=1
        self.CC_Standings=self.CC_Standings[:j]

    def pbhustle(self):

        self.ratings=db.child('Ratings').get().val()
        self.PB_Standings.clear()

        for id in self.ratings:
            
            name=db.child('users').child(id).child('name').get().val()
            handle=db.child('users').child(id).child('CF_id').get().val()
            rating=self.ratings[id]['PB']

            self.PB_Standings.append([name,handle,rating])

        self.PB_Standings.sort(key= lambda x: x[2],reverse=True)
        
        j=0
        while( j<len(self.PB_Standings) and   self.PB_Standings[j][2]!=-10000): j+=1
        self.PB_Standings=self.PB_Standings[:j]


    
# a=standings()
# a.pbhustle()
# print(a.PB_Standings)


