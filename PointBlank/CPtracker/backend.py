
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


    def SignIn(self,email,password):

        self.user=self.auth.sign_in_with_email_and_password(email,password)

    def SignUp(self,email,password):

        self.user=self.auth.create_user_with_email_and_password(email,password)

    def PushData(self): 
        
        pass


        