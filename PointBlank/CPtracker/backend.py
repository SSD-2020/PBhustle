import pyrebase
import gspread

from .PbhustleUpdate import *


gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1DHh5jPufmWLyPrYngpORRWAtslzbUA_o_8OBdGI3So4')

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
        if(users==None): return False

        for i in users: 
            if(users[i]['email']==emailid): return True

        return False

    
    def getPBRating(self,id):
        res=self.db.child("PBhustle").child(id.replace('.','*')).child('curRating').get().val()
        return res

    def getPBcontests(self,id):
        res=self.db.child("PBhustle").child(id.replace('.','*')).child('contests').get().val()
        return res


    def updateHustle(self):

        cur_page=self.db.child("PBhustle").child('PageIndex').get().val()
        print(cur_page)

        while(True):

            try: sheet=sh.get_worksheet(cur_page).get_all_records()
            except: break

            curRating={}
            for i in sheet:

                here=i['Who']

                j=0
                while(j<len(here) and here[j]!=" "): j+=1
                here=here[:j]
                
                curRating[here]=self.getPBRating(here)
                print(here,curRating[here])

            newRating=ratingcal(sheet,curRating)

            cur_page+=1



                    



f=firebase()
f.updateHustle()




# f=firebase()
# print(f.getPBcontests('deepanshu_pali'))
# print(f.EmailExist('deepanshukumarpali7@gmail.com'))
# 

# f.SignIn('deepanshukumarpali7@gmail.com','1234567')
# f.GetData()
# print(f.data)      
    
