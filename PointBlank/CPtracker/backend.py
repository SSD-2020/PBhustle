import pyrebase


class firebase:

    def __init__(self):

        self.firebaseConfig = {
            'apiKey': "AIzaSyAIuua7NGadNu4dHChW0hYGHLApMW_XVOE",
            'authDomain': "pbhustle-702d9.firebaseapp.com",
            'databaseURL': "https://pbhustle-702d9.firebaseio.com",
            'projectId': "pbhustle-702d9",
            'storageBucket': "pbhustle-702d9.appspot.com",
            'messagingSenderId': "63903745303",
            'appId': "1:63903745303:web:1f610bfc6f8df057e52352",
            'measurementId': "G-YKZE3DKT4Z"
        }

        self.user=None
        self.auth=pyrebase.initialize_app(self.firebaseConfig).auth()
        self.db=pyrebase.initialize_app(self.firebaseConfig).database()
        self.data={}


    def Clear(self):
        
        self.user=None
        self.auth=pyrebase.initialize_app(self.firebaseConfig).auth()
        self.db=pyrebase.initialize_app(self.firebaseConfig).database()
        self.data={}


    def SignIn(self,email,password):
        self.user=self.auth.sign_in_with_email_and_password(email,password)

    def SignUp(self,email,password):
        self.user=self.auth.create_user_with_email_and_password(email,password)

    def PushData(self,data):

        self.db.child('users').child(self.user['localId']).set(data)
        ratings={'CF' : data['CF_rating'], 'CC' : data['CC_rating'], 'PB' : data['PB_rating']}
        self.db.child('Ratings').child(self.user['localId']).set(ratings)

    def UpdateData(self,data):

        self.db.child('users').child(self.user['localId']).remove()
        self.db.child('Ratings').child(self.user['localId']).remove()
        self.PushData(data)

    def UpdateCFRatings(self,CF):
        self.db.child('Ratings').child(self.user['localId']).update({'CF':CF})

    def UpdateCCRatings(self,CC):
        self.db.child('Ratings').child(self.user['localId']).update({'CC':CC})
    
    def UpdatePBRatings(self,PB):
        self.db.child('Ratings').child(self.user['localId']).update({'PB':PB})


    
    def GetData(self):
        res=self.db.child("users").child(self.user['localId']).get()

        self.data=res.val()

    def EmailExist(self, emailid):

        users=self.db.child("users").get().val()
        uid=[]
        if(users==None): return False

        for i in users: uid.append(users[i][list(users[i].keys())[0]])

        for user in uid:
            if(user['email']==emailid): return True

        return False

    
    def getPBRating(self,id):
        res=self.db.child("PBhustle").child(id.replace('.','*')).child('curRating').get().val()
        return res

    def getPBcontests(self,id):
        res=self.db.child("PBhustle").child(id.replace('.','*')).child('contests').get().val()
        return res




                    








# f=firebase()
# print(f.getPBcontests('deepanshu_pali'))
# print(f.EmailExist('deepanshukumarpali7@gmail.com'))
# 

# f.SignIn('deepanshukumarpali7@gmail.com','1234567')
# f.GetData()
# print(f.data)      
    
