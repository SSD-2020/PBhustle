from django.shortcuts import render
from django.http import HttpResponse
from .main import *
from .backend import *

# Create your views here.

backend_obj=firebase()


# data={
    # 'name':'Deepanshu Kumar Pali', 
    # 'email': 'deepanshukumarpali@gmail.com',
    # 'college' : 'Dayananda Sagar College of Engineering',
    # 'branch' : 'Computer Science',
    # 'CC_id': 'deepu217',
    # 'CF_id': 'deepanshu_pali',
    # 'HE_id': 'deepanshu424',
    # 'HR_id': 'deepanshukumarp2',
# }


    

def landingpage(request):

    return render(request,'landingpage.html')

def signin(request):

    emailid=request.POST['emailid']
    password=request.POST['password']
    backend_obj.SignIn(emailid,password)
    # print(backend_obj.user)

    return userhome(request)

def signup(request):

    emailid=request.POST['emailid']
    password=request.POST['password']
    CF_id=request.POST['CF_id']
    CC_id=request.POST['CC_id']
    name=request.POST['name']
    branch=request.POST['branch']
    sem=request.POST['sem']
    backend_obj.SignUp(emailid,password)

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

    backend_obj.PushData(data)

    return landingpage(request)



def userhome(request):

    print(backend_obj.user)
    backend_obj.GetData()

    return render(
        request,'userhome.html',
        {
            'name':  backend_obj.data['name'],
            'email': backend_obj.data['email'],
            'college': backend_obj.data['college'],
            'branch': backend_obj.data['branch'],
            'sem': backend_obj.data['sem'],
            'CC_id': backend_obj.data['CC_id'],
            'CF_id': backend_obj.data['CF_id'],
        }
        )



#### CP Stuff ------------------------------------------------------------/

def codeforces(request):

    CF_user=Codeforces(backend_obj.data['CF_id'])
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
    compare=CodeforceCompare(backend_obj.data['CF_id'],friend)
    compare.compare()

    return render(request, "codeforcescompare.html",{
        'friend' : friend,
        'result': compare.compare_result[::-1],
        'plot' : compare.plot
        }
        )

def codechefCompare(request):

    friend=request.GET['friend_id']
    compare=CodechefCompare(backend_obj.data['CC_id'],friend)
    compare.compare()


    return render(request, "codechefcompare.html",{
        'friend' : friend,
        'result': compare.compare_result[::-1],
        'plot' : compare.plot
        }
        )



def codechef(request):

    CC_user=Codechef(backend_obj.data['CC_id'])
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
    
    print(backend_obj.user)
    return render(request,'pbhustle.html')