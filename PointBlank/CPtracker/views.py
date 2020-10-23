from django.shortcuts import render
from django.http import HttpResponse
from .codechefCompare import *
from .codeforcesCompare import *
from .codechefData import *
from .codeforcesData import *
from .backend import *
from .leaderboards import *

# Create your views here.

firebase_user=firebase()
ranking=standings()


    

def landingpage(request,SignUp=False,logOut=False,edit=False,inValid=(False,False,False)):

    # if(not logOut and firebase_user.user!=None): return userhome(request)

    print(firebase_user.user!=None)

    return render(request,'landingpage.html',{
        'SignUp':SignUp ,
        'inValid_Email': inValid[0],
        'inValid_CF': inValid[1],
        'inValid_CC': inValid[2],
        'user': firebase_user.user!=None,
        'edit': False,

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

    name=request.POST['name']
    emailid=request.POST['emailid']
    password=request.POST['password']
    sem=request.POST['sem']
    branch=request.POST['branch']

    data={
        'email': emailid,
        'CC_id': '--',
        'CF_id': '--',
        'name': name, 
        'college' : "Dayananda Sagar College of Engineering",
        'branch' : branch,
        'sem': sem,
        'CF_rating' : -10000,
        'CC_rating' : -10000,
        'PB_rating' : -10000,
    }

    emailid_exist=firebase_user.EmailExist(emailid)

    if(not emailid_exist):
        firebase_user.SignUp(emailid,password)
        firebase_user.PushData(data)
        return landingpage(request,True)

    return landingpage(request,True,False,False,(True,False,False))


def edit(request):

    firebase_user.GetData()
    data=firebase_user.data
    
    CF_id=request.POST['CF_id']
    CC_id=request.POST['CC_id']
    data['branch']=request.POST['branch']
    data['sem']=request.POST['sem']
    # data['college']=request.POST['college']


    # print(data)
    CF_user=Codeforces(CF_id)
    CF_user.fetch_data()

    CC_user=Codechef(CC_id)
    CC_user.fetch_data()

    if(CF_user.user_valid): 
        data['CF_id']=CF_id
        data['CF_rating']= CF_user.user_info["Current Rating"]
        data['PB_rating']= firebase_user.getPBRating(CF_id)

        if(data['PB_rating']==None): data['PB_rating']=-10000

    if(CC_user.user_valid): 
        data['CC_id']=CC_id
        data['CC_rating']= CC_user.user_info["Current Rating"]

    firebase_user.UpdateData(data)

    return userhome(request)



def userhome(request,edit=False,CF_invalid=False,CC_invalid=False):


    firebase_user.GetData()
    print(firebase_user.data)

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
            'edit' : edit,
            'inValid_CF': CF_invalid,
            'inValid_CC': CC_invalid,
            
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
    firebase_user.UpdateCFRatings(CF_user.user_info["Current Rating"])
    ranking.codeforces()

    return render( 
        request,
        'codeforces.html', 
        {
            'plot':CF_user.plot,
            'info':CF_user.user_info,
            'contests':CF_user.user_contests[::-1],
            'standings': ranking.CF_Standings
            }
        )


def codechef(request):

    CC_user=Codechef(firebase_user.data['CC_id'])
    CC_user.fetch_data()
    CC_user.plot_data()

    print(CC_user.user_info)

    firebase_user.UpdateCCRatings(CC_user.user_info["Current Rating"])
    ranking.codechef()

    return render(
        request,
        'codechef.html',
        {
            'plot':CC_user.plot,
            'info':CC_user.user_info,
            'contests':CC_user.user_contests[::-1],
            'standings': ranking.CC_Standings
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