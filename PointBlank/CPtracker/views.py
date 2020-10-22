from django.shortcuts import render
from django.http import HttpResponse
from .codechefCompare import *
from .codeforcesCompare import *
from .codechefData import *
from .codeforcesData import *
from .backend import *

# Create your views here.

firebase_user=firebase()

    

def landingpage(request,SignUp=False,logOut=False,inValid=(False,False,False,False)):

    # if(not logOut and firebase_user.user!=None): return userhome(request)

    print(firebase_user.user!=None)

    return render(request,'landingpage.html',{
        'SignUp':SignUp ,
        'inValid_Email': inValid[0],
        'inValid_CF': inValid[2],
        'inValid_CC': inValid[3],
        'inValid_Pass': inValid[1],
        'user': firebase_user.user!=None

        }
        )




def signin(request):

    emailid=request.POST['emailid']
    password=request.POST['password']
    # print(firebase_user.user)

    try: firebase_user.SignIn(emailid,password)
    except: return landingpage(request,False,False,(False,True,False,False))
    
    firebase_user.GetData()
    return landingpage(request)

def signup(request):

    emailid=request.POST['emailid']
    password=request.POST['password']
    CF_id=request.POST['CF_id']
    CC_id=request.POST['CC_id']
    name=request.POST['name']
    branch=request.POST['branch']
    sem=request.POST['sem']

    data={
        'email': emailid,
        'CC_id': CC_id,
        'CF_id': CF_id,
        'name': name, 
        'college' : 'Dayananda Sagar College of Engineering',
        'branch' : branch,
        'sem': sem,
    }

    print(data)
    CF_user=Codeforces(data['CF_id'])
    CF_user.fetch_data()

    CC_user=Codechef(data['CC_id'])
    CC_user.fetch_data()

    emailid_exist=firebase_user.EmailExist(emailid)

    if(CF_user.user_valid and CC_user.user_valid and not emailid_exist):
        firebase_user.SignUp(emailid,password)
        firebase_user.PushData(data)
        return landingpage(request,True,False,(False,False,not CF_user.user_valid,not CC_user.user_valid))

    return landingpage(request,False,False,(emailid_exist,False,not CF_user.user_valid,not CC_user.user_valid))



def userhome(request):


    return render(
        request,'userhome.html',
        {
            'name':  firebase_user.data['name'],
            'email': firebase_user.data['email'],
            'college': firebase_user.data['college'],
            'branch': firebase_user.data['branch'],
            'sem': firebase_user.data['sem'],
            'CC_id': firebase_user.data['CC_id'],
            'CF_id': firebase_user.data['CF_id'],
        }
        )

        

def logout(request):
    firebase_user.Clear()
    return landingpage(request,False,True)




#### CP Stuff ------------------------------------------------------------/

def codeforces(request):

    CF_user=Codeforces(firebase_user.data['CF_id'])

    try: CF_user.fetch_data()
    except : return render(request,'error.html')
    CF_user.plot_data()

    return render( 
        request,
        'codeforces.html', 
        {
            'plot':CF_user.plot,
            'info':CF_user.user_info,
            'contests':CF_user.user_contests[::-1]
            }
        )


def codechef(request):

    CC_user=Codechef(firebase_user.data['CC_id'])
    CC_user.fetch_data()
    CC_user.plot_data()

    return render(
        request,
        'codechef.html',
        {
            'plot':CC_user.plot,
            'info':CC_user.user_info,
            'contests':CC_user.user_contests[::-1]
            }
        )


def codeforcesCompare(request):

    friend=request.GET['friend_id']
    compare=CodeforceCompare(firebase_user.data['CF_id'],friend)
    compare.compare()

    return render(request, "codeforcescompare.html",{
        'friend' : friend,
        'result': compare.compare_result[::-1],
        'plot' : compare.plot
        }
        )

def codechefCompare(request):

    friend=request.GET['friend_id']
    compare=CodechefCompare(firebase_user.data['CC_id'],friend)
    compare.compare()


    return render(request, "codechefcompare.html",{
        'friend' : friend,
        'result': compare.compare_result[::-1],
        'plot' : compare.plot
        }
        )

def pbhustle(request):
    
    print(firebase_user.user)
    return render(request,'pbhustle.html')