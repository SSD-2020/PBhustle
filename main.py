# Class
from collections import defaultdict
import requests

class Codeforce:

    def __init__(self,user_id):

        self.user_id=user_id
        self.user_info=[]
        self.user_contests=[]


    def get_info(self):

        pass

    def get_contests(self):

        pass


class Codechef:

    def __init__(self,user_id):

        self.user_id=user_id
        self.user_info={}
        self.user_contests=[]
        self.user_valid=False


    def fetch_data(self):

        url='https://competitive-coding-api.herokuapp.com/api/codechef/'+self.user_id
        content=requests.get(url).json()

        if(content['status']!='Success'):  return
        self.user_valid=True


        # USER INFORMATION 

        for i in content:
            if(i in ['rating', 'stars', 'highest_rating', 'global_rank', 'country_rank']):
                self.user_info[i]=content[i]

        for i in content['user_details']:
            self.user_info[i]=content['user_details'][i]

        # USER CONTESTS

        for contest in content['contest_ratings']:
            
            here={}
            for key in contest:
                if(key in ['code','rating', 'rank', 'name']):
                    here[key]=contest[key]

            self.user_contests.append(here)


CC_user=Codechef('deepu217')
CC_user.fetch_data()

print(CC_user.user_valid)
print()

print(CC_user.user_info)
print()

print(CC_user.user_contests)
print()

