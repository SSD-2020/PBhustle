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

        self.db.child('users').child(self.user['localId']).push(data)
        ratings={'CF' : data['CF_rating'], 'CC' : data['CC_rating'], 'PB' : data['PB_rating']}
        self.db.child('Ratings').child(self.user['localId']).push(ratings)

    def UpdateData(self,data):

        self.db.child('users').child(self.user['localId']).remove()
        self.db.child('Ratings').child(self.user['localId']).remove()
        self.PushData(data)

    
    def GetData(self):
        res=self.db.child("users").child(self.user['localId']).child('').get()
        for have in res.each(): self.data=have.val()

    def EmailExist(self, emailid):

        users=self.db.child("users").get().val()
        uid=[]
        if(users==None): return False

        for i in users: uid.append(users[i][list(users[i].keys())[0]])

        for user in uid:
            if(user['email']==emailid): return True

        return False

# f=firebase()
# print(f.EmailExist('deepanshukumarpali7@gmail.com'))      
    


        