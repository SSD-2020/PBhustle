from django.shortcuts import render
from django.http import HttpResponse
from .main import *
from .backend import firebase

# Create your views here.

backend_obj=firebase()


data={
    'name':'Deepanshu Kumar Pali', 
    'email': 'deepanshukumarpali@gmail.com',
    'college' : 'Dayananda Sagar College of Engineering',
    'branch' : 'Computer Science',
    'CC_id': 'deepu217',
    'CF_id': 'deepanshu_pali',
    'HE_id': 'deepanshu424',
    'HR_id': 'deepanshukumarp2',
}


    




def landingpage(request):

    return render(request,'landingpage.html')

def signin(request):

    emailid=request.GET(['emailid'])
    password=request.GET(['password'])
    backend_obj.SignIn(emailid,password)

    return userhome(request)

def signup(request):

    emailid=request.GET(['emailid'])
    password=request.GET(['password'])
    backend_obj.SignUp(emailid,password)
    backend_obj.PushData()

    return userhome(request)



def userhome(request):

    return render(
        request,'userhome.html',
        {
            'name':  data['name'],
            'email': data['email'],
            'college': data['college'],
            'branch': data['branch'],
            'CC_id': data['CC_id'],
            'CF_id': data['CF_id'],
            'HE_id': data['HE_id'],
            'HR_id': data['HR_id'],
        }
        )



#### CP Stuff ------------------------------------------------------------/

def codeforces(request):

    CF_user=Codeforces(data['CF_id'])
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
    compare=CodeforceCompare(data['CF_id'],friend)
    compare.compare()

    return render(request, "codeforcescompare.html",{
        'friend' : friend,
        'result': compare.compare_result[::-1],
        'plot' : compare.plot
        }
        )

def codechefCompare(request):

    friend=request.GET['friend_id']
    compare=CodechefCompare(data['CC_id'],friend)
    compare.compare()


    return render(request, "codechefcompare.html",{
        'friend' : friend,
        'result': compare.compare_result[::-1],
        'plot' : compare.plot
        }
        )



def codechef(request):

    CC_user=Codechef(data['CC_id'])
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
    return render(request,'pbhustle.html')