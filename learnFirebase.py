import pyrebase

firebaseConfig= {

    'apiKey': "AIzaSyBMMqB30RHpiRa3auSr4IMr13iz1bUEFP4",
    'authDomain': "testing-5499b.firebaseapp.com",
    'databaseURL': "https://testing-5499b.firebaseio.com",
    'projectId': "testing-5499b",
    'storageBucket': "testing-5499b.appspot.com",
    'messagingSenderId': "585804373742",
    'appId': "1:585804373742:web:0e22b9d40d99238a759dff",
    'measurementId': "G-8KPP9G2ZS6"
}

firebase= pyrebase.initialize_app(firebaseConfig)

auth=firebase.auth()
db=firebase.database()

email=input("ID: ")
password=input("password: ")
user=auth.create_user_with_email_and_password(email,password)
print(user)




