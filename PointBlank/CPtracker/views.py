from django.shortcuts import render
from django.http import HttpResponse
from .main import *
from .backend import *

# Create your views here.

firebase_user=firebase()

    

def landingpage(request,SignUp=False,logOut=False):

    if(not logOut and firebase_user.user!=None): return userhome(request)

    firebase_user.Clear()
    return render(request,'landingpage.html',{'SignUp':SignUp})

def signin(request):

    emailid=request.POST['emailid']
    password=request.POST['password']
    firebase_user.SignIn(emailid,password)
    # print(firebase_user.user)

    return userhome(request)

def signup(request):

    emailid=request.POST['emailid']
    password=request.POST['password']
    CF_id=request.POST['CF_id']
    CC_id=request.POST['CC_id']
    name=request.POST['name']
    branch=request.POST['branch']
    sem=request.POST['sem']
    firebase_user.SignUp(emailid,password)

    data={
        'email': emailid,
        'CC_id': CC_id,
        'CF_id': CF_id,
        'name': name, 
        'college' : 'Dayananda Sagar College of Engineering',
        'branch' : branch,
        'sem': sem,
        # 'HE_id': HE_id,
        # 'HR_id': HR_id,
    }

    firebase_user.PushData(data)

    return landingpage(request,True)



def userhome(request):

    print(firebase_user.user)
    firebase_user.GetData()

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
    return landingpage(request,False,True)




#### CP Stuff ------------------------------------------------------------/

def codeforces(request):

    CF_user=Codeforces(firebase_user.data['CF_id'])
    CF_user.fetch_data()
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


def hackerrank(request):
    return render(request,'hackerrank.html')

def pbhustle(request):
    
    print(firebase_user.user)
    return render(request,'pbhustle.html')