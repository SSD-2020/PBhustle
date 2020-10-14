from django.shortcuts import render
from django.http import HttpResponse
from .main import Codechef,Codeforces

# Create your views here.



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

def userhome(request):



    return render(
        request,'userhome.html',
        {
            'name':  data['name'],
            'email': data['email'],
            'college': data['college'],
            'branch' : data['branch'],
            'CC_id': data['CC_id'],
            'CF_id': data['CF_id'],
            'HE_id': data['HE_id'],
            'HR_id': data['HR_id'],
        }
        )

def codeforces(request):

    CF_user=Codeforces(data['CF_id'])
    CF_user.fetch_data()
    CF_user.plot_data()

    return render(
        request,'codeforces.html',
        {
            'info': CF_user.user_info,
            'contest': CF_user.user_contests,
        }
        )

def codechef(request):

    CC_user=Codechef(data['CC_id'])
    CC_user.fetch_data()
    CC_user.plot_data()


    return render(
        request,'codechef.html',
        {
            'info': CC_user.user_info,
            'contest': CC_user.user_contests,
        }
        )

def hackerrank(request):
    return render(request,'hackerrank.html')

def pbhustle(request):
    return render(request,'pbhustle.html')