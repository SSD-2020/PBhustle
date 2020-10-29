from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse
from .codechefCompare import *
from .codeforcesCompare import *
from .codechefData import *
from .pbhustleData import *
from .pbhustleCompare import *
from .codeforcesData import *
from .backend import *
from .leaderboards import *

# Create your views here.


    

def landingpage(request,SignIn=False,SignUp=False,logOut=False,edit=False,inValid=(False,False,False),inValid_Pass=False):

    user_id=request.session.get('uid')
    print(user_id)


    return render(request,'landingpage.html',{
        'SignIn' : SignIn ,
        'SignUp':SignUp ,
        'inValid_Email': inValid[0],
        'inValid_CF': inValid[1],
        'inValid_CC': inValid[2],
        'user': user_id!=None,
        'edit': False,
        'inValid_Pass': inValid_Pass,

        }
        )




def signin(request):

    emailid=request.POST['emailid']
    password=request.POST['password']

    firebase_user=firebase()

    try: firebase_user.SignIn(emailid,password)
    except: return landingpage(request,False,False,False,False,(False,False,False),True)
    
    # print(firebase_user.user['idToken'])
    session_id=firebase_user.user
    request.session['uid']=str(session_id)

    firebase_user.GetData()
    return landingpage(request,True)

def signup(request):

    name=request.POST['name']
    emailid=request.POST['emailid']
    password=request.POST['password']
    sem=request.POST['sem']
    branch=request.POST['branch']


    data={
        'email': emailid,
        'CC_id': 'N/A',
        'CF_id': 'N/A',
        'name': name, 
        'college' : "Dayananda Sagar College of Engineering",
        'branch' : branch,
        'sem': sem,
        'CC_rating' : -10000,
        'CF_rating' : '-10000 ',
        'PB_rating' : -10000,
    }
    firebase_user=firebase()
    emailid_exist=firebase_user.EmailExist(emailid)

    
    try: firebase_user.SignUp(emailid,password)
    except: emailid_exist=True

    if(not emailid_exist):
        
        firebase_user.PushData(data)
        return landingpage(request,False,True)
 
    return landingpage(request,False,True,False,False,(True,False,False))


def edit(request):

    user=request.session.get('uid')
    firebase_user=firebase(user)

    if(user==None): return render(request, 'error.html')

    firebase_user.GetData()
    data=firebase_user.data
    
    CF_id=request.POST['CF_id']
    CC_id=request.POST['CC_id']
    data['branch']=request.POST['branch']
    data['sem']=request.POST['sem']

    CF_user=Codeforces(CF_id)
    CF_user.fetch_data()

    CC_user=Codechef(CC_id)
    CC_user.fetch_data()

    if(CF_user.user_valid): 
        data['CF_id']=CF_id
        data['CF_rating']= CF_user.user_info["Current Rating"]
        data['PB_rating']= firebase_user.getPBRating(CF_id)

    if(CC_user.user_valid): 
        data['CC_id']=CC_id
        data['CC_rating']= CC_user.user_info["Current Rating"]

    firebase_user.UpdateData(data)

    return userhome(request,True,CF_user.user_valid,CC_user.user_valid)



def userhome(request,edit=False,CF_valid=True,CC_valid=True):

    user=request.session.get('uid')
    firebase_user=firebase(user)

    if(firebase_user.user==None): return render(request, 'error.html')

    firebase_user.GetData()
    ratings=firebase_user.GetRatings()
    # print(ratings)

    CF_rating=ratings['CF']
    CC_rating=ratings['CC']
    PB_rating=ratings['PB']

    if(PB_rating==-10000): PB_rating='N/A'
    if(CF_rating=='-10000 ') : CF_rating='N/A'
    else:
        j=0
        while(j<len(CF_rating) and CF_rating[j]!=' '): j+=1
        CF_rating=CF_rating[:j]

    if(CC_rating==-10000): CC_rating='N/A'


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
            'Valid_CF': CF_valid,
            'Valid_CC': CC_valid,
            'CF_rating': CF_rating,
            'CC_rating' : CC_rating,
            'PB_rating' : PB_rating,
            
        }
        )

        

def logout(request):


    request.session['uid']=None
    return landingpage(request,False,False,True)


def update(request):

    user=request.session.get('uid')
    firebase_user=firebase(user)

    if(firebase_user.user==None): return render(request, 'error.html')

    firebase_user.updateHustle()
    return userhome(request)

#### CP Stuff -----------------------------------------------------------/

def codeforces(request):

    user=request.session.get('uid')
    firebase_user=firebase(user)
    
    if(firebase_user.user==None): return render(request, 'error.html')

    firebase_user.GetData()
    CF_user=Codeforces(firebase_user.data['CF_id'])
    CF_user.fetch_data()

    CF_user.plot_data()
    firebase_user.UpdateCFRatings(CF_user.user_info["Current Rating"])

    ranking=standings()
    ranking.codeforces()

    here={}
    for i in CF_user.user_info: here[i]=CF_user.user_info[i]

    if(here["Current Rating"]=='-10000 '): here["Current Rating"]='N/A'
    if(here["Maximum Rating"]=='-10000 '): here["Maximum Rating"]='N/A'

    return render( 
        request,
        'codeforces.html', 
        {
            'plot':CF_user.plot,
            'info':here,
            'contests':CF_user.user_contests[::-1],
            'standings': ranking.CF_Standings,
            'user_id' : firebase_user.data['CF_id']!='N/A',
            }
        )


def codechef(request):

    user=request.session.get('uid')
    firebase_user=firebase(user)

    if(firebase_user.user==None): return render(request, 'error.html')

    firebase_user.GetData()
    CC_user=Codechef(firebase_user.data['CC_id'])
    CC_user.fetch_data()
    CC_user.plot_data()

    firebase_user.UpdateCCRatings(CC_user.user_info["Current Rating"])

    ranking=standings()
    ranking.codechef()

    here={}
    for i in CC_user.user_info: here[i]=CC_user.user_info[i]

    if(here["Current Rating"]==-10000): here["Current Rating"]='N/A'
    if(here["Maximum Rating"]==-10000): here["Maximum Rating"]='N/A'

    return render(
        request,
        'codechef.html',
        {
            'plot':CC_user.plot,
            'info':here,
            'contests':CC_user.user_contests[::-1],
            'standings': ranking.CC_Standings,
            'user_id' : firebase_user.data['CF_id']!='N/A',
            }
        )


def codeforcesCompare(request):

    user=request.session.get('uid')
    firebase_user=firebase(user)

    if(firebase_user.user==None): return render(request, 'error.html')

    friend=request.GET['friend_id']
    firebase_user.GetData()
    compare=CodeforceCompare(firebase_user.data['CF_id'],friend)
    compare.compare()

    return render(request, "codeforcescompare.html",{
        'friend' : friend,
        'result': compare.compare_result[::-1],
        'plot' : compare.plot,
        'not_valid': compare.friend_valid==False,
        'empty_list' : len(compare.compare_result)==0,
        }
        )

def codechefCompare(request):

    user=request.session.get('uid')
    firebase_user=firebase(user)

    if(firebase_user.user==None): return render(request, 'error.html')

    firebase_user.GetData()

    friend=request.GET['friend_id']
    compare=CodechefCompare(firebase_user.data['CC_id'],friend)
    compare.compare()

    print(compare.friend_valid)


    return render(request, "codechefcompare.html",{
        'friend' : friend,
        'result': compare.compare_result[::-1],
        'plot' : compare.plot,
        'not_valid': compare.friend_valid==False,
        'empty_list' : len(compare.compare_result)==0,
        }
        )

def pbhustle(request):

    user=request.session.get('uid')
    firebase_user=firebase(user)

    if(firebase_user.user==None): return render(request, 'error.html')

    # print(firebase_user)
    firebase_user.GetData()
    PB_user=PBhustle(firebase_user.data['CF_id'])
    PB_user.fetch_data()
    PB_user.plot_data()
    rating=firebase_user.getPBRating(firebase_user.data['CF_id'])

    if(rating==-10000): rating='N/A'

    ranking=standings()
    ranking.pbhustle()

    user_info={
        'user handle' : firebase_user.data['CF_id'],
        'current rating' : rating,
        'maximum rating' : PB_user.maxRating

    }

    return render(
        request,
        'pbhustle.html',
        {
            'plot':PB_user.plot,
            'info':user_info,
            'contests':PB_user.user_contests[::-1],
            'standings': ranking.PB_Standings,
            'user_id' : firebase_user.data['CF_id']!='N/A',
            }
        )

def pbhustleCompare(request):

    user=request.session.get('uid')
    firebase_user=firebase(user)
    firebase_user.GetData()

    if(firebase_user.user==None): return render(request, 'error.html')

    friend=request.GET['friend_id']
    compare=PBhustleCompare(firebase_user.data['CF_id'],friend)
    compare.compare()


    return render(request, "pbhustleCompare.html",{
        'friend' : friend,
        'result': compare.compare_result[::-1],
        'plot' : compare.plot,
        'not_valid': compare.friend_valid==False,
        'empty_list' : len(compare.compare_result)==0,
        }
        )

#### ERROR VIEWS ####

def error_view(request,exception=None):
    return render(request, 'error.html')