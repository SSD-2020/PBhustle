import pyrebase
import gspread
from dataclasses import dataclass
import numpy as np
from numpy.fft import fft, ifft
import gspread
from collections import defaultdict
import requests

# path = ['', '', '']

# # Deepanshu
# path[0] = '/Users/deepanshukumarpali/Desktop/projects/PBhustle/credentials.json'
# path[1] = 'C:\Users\Sparsh\Desktop\PBhustle\credentials.json'  # Sparsh
# path[2] = ''  # Sumit

# bhai index change kar lena bas
gc = gspread.service_account(filename="./credentials.json")
sh = gc.open_by_key('1DHh5jPufmWLyPrYngpORRWAtslzbUA_o_8OBdGI3So4')

############### Rating Calculator ###################


def intdiv(x, y):
    return -(-x // y) if x < 0 else x // y


class Contestant:

    def __init__(self, handle, points, penalty, rating):
        self.party = handle
        self.points = points
        self.penalty = penalty
        self.rating = rating
        self.need_rating = 0
        self.delta = 0
        self.rank = 0.0
        self.seed = 0.0


class CodeforcesRatingCalculator:
    def __init__(self, standing_rows, prev_ratings):
        """Calculate Codeforces rating changes and seeds given contest and user information."""
        self.contestants = [
            Contestant(handle, points, penalty, prev_ratings[handle])
            for handle, _, points, penalty in standing_rows
        ]

        self._precalc_seed()
        self._reassign_ranks()
        self._process()
        self._update_delta()

    def calculate_rating_changes(self):
        """Return a mapping between contestants and their corresponding delta."""
        return {contestant.party: contestant.delta for contestant in self.contestants}

    def get_seed(self, rating, me=None):
        """Get seed given a rating and user."""
        seed = self.seed[rating]
        if me:
            seed -= self.elo_win_prob[rating - me.rating]
        return seed

    def _precalc_seed(self):
        MAX = 6144

        # Precompute the ELO win probability for all possible rating differences.
        self.elo_win_prob = np.roll(
            1 / (1 + pow(10, np.arange(-MAX, MAX) / 600)), -MAX)

        # Compute the rating histogram.
        count = np.zeros(2 * MAX)
        for a in self.contestants:
            count[a.rating] += 1

        # Precompute the seed for all possible ratings using FFT.
        self.seed = 1 + ifft(fft(count) * fft(self.elo_win_prob)).real

    def _reassign_ranks(self):
        """Find the rank of each contestant."""
        contestants = self.contestants
        contestants.sort(key=lambda o: (-o.points, o.penalty))
        points = penalty = rank = None
        for i in reversed(range(len(contestants))):
            if contestants[i].points != points or contestants[i].penalty != penalty:
                rank = i + 1
                points = contestants[i].points
                penalty = contestants[i].penalty
            contestants[i].rank = rank

    def _process(self):
        """Process and assign approximate delta for each contestant."""
        for a in self.contestants:
            a.seed = self.get_seed(a.rating, a)
            mid_rank = (a.rank * a.seed) ** 0.5
            a.need_rating = self._rank_to_rating(mid_rank, a)
            a.delta = intdiv(a.need_rating - a.rating, 2)

    def _rank_to_rating(self, rank, me):
        """Binary Search to find the performance rating for a given rank."""
        left, right = 1, 8000
        while right - left > 1:
            mid = (left + right) // 2
            if self.get_seed(mid, me) < rank:
                right = mid
            else:
                left = mid
        return left

    def _update_delta(self):
        """Update the delta of each contestant."""
        contestants = self.contestants
        n = len(contestants)

        contestants.sort(key=lambda o: -o.rating)
        correction = intdiv(-sum(c.delta for c in contestants), n) - 1
        for contestant in contestants:
            contestant.delta += correction

        zero_sum_count = min(4 * round(n ** 0.5), n)
        delta_sum = -sum(contestants[i].delta for i in range(zero_sum_count))
        correction = min(0, max(-10, intdiv(delta_sum, zero_sum_count)))
        for contestant in contestants:
            contestant.delta += correction


def predict(rows, prev_ratings):
    calc = CodeforcesRatingCalculator(rows, prev_ratings)
    return calc.calculate_rating_changes()


def ratingcal(standings, prev_rating):
    record = standings
    rows = []
    for i in record:
        st = ""
        for j in i['Who']:
            if(not j.isalnum() and j != "." and j != "_"):
                break
            st += j
        rows += [(st, i['#'], i['#ERROR!'], i['Penalty'])]

    predicted = predict(rows, prev_rating)
    new_rating = defaultdict(int)
    for i in predicted:
        new_rating[i] = prev_rating[i]+predicted[i]

    return new_rating


############### Firebase Connection ##############


class firebase:

    def __init__(self,uid=None):

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

        self.user = uid
        self.auth = pyrebase.initialize_app(self.firebaseConfig).auth()
        self.db = pyrebase.initialize_app(self.firebaseConfig).database()
        self.data = {}

    def Clear(self):

        self.user = None
        self.auth = pyrebase.initialize_app(self.firebaseConfig).auth()
        self.db = pyrebase.initialize_app(self.firebaseConfig).database()
        self.data = {}

    def SignIn(self, email, password):
        self.user = self.auth.sign_in_with_email_and_password(email, password)['localId']

        # print(self.user)
        # print('---------')

    def SignUp(self, email, password):
        self.user = self.auth.create_user_with_email_and_password(
            email, password)['localId']

    def PushData(self, data):

        self.db.child('users').child(self.user).set(data)

        ratings = {'CF': data['CF_rating'],
                   'CC': data['CC_rating'], 'PB': data['PB_rating']}
        self.db.child('Ratings').child(self.user).set(ratings)

    def UpdateData(self, data):

        self.db.child('users').child(self.user).remove()
        self.db.child('Ratings').child(self.user).remove()
        self.PushData(data)

    def UpdateCFRatings(self, CF):
        self.db.child('Ratings').child(self.user).update({'CF': CF})

    def UpdateCCRatings(self, CC):
        self.db.child('Ratings').child(self.user).update({'CC': CC})

    def UpdatePBRatings(self, PB):
        self.db.child('Ratings').child(self.user).update({'PB': PB})

    def GetData(self):
        res = self.db.child("users").child(self.user).get()
        self.data = res.val()


    def GetRatings(self):
        return self.db.child('Ratings').child(self.user).get().val()

    def EmailExist(self, emailid):

        users = self.db.child("users").get().val()
        if(users == None):
            return False

        for i in users:
            if(users[i]['email'] == emailid):
                return True

        return False

    def getPBRating(self, id):
        res = self.db.child("PBhustle").child(
            id.replace('.', '*')).child('curRating').get().val()

        if(res == None):
            return -10000
        return res

    def getPBcontests(self, id):
        res = self.db.child("PBhustle").child(
            id.replace('.', '*')).child('contests').get().val()
        return res

    def updateHustle(self):

        cur_page = self.db.child("PBhustle").child('PageIndex').get().val()

        while(True):

            try:
                sheet = sh.get_worksheet(cur_page).get_all_records()
            except:
                break

            curRating = {}
            have = []
            name = sh.get_worksheet(cur_page).title
            name = name[name.index(" ")+1:].replace('.', '_')
            # print(name)

            for i in sheet:

                here = i['Who']

                j = 0
                while(j < len(here) and here[j] != " "):
                    j += 1
                here = here[:j]

                curRating[here] = self.getPBRating(here)
                if(curRating[here] == None):
                    curRating[here] = 500
                have.append(here)

            newRating = ratingcal(sheet, curRating)

            for rank in range(1, len(have)+1):

                user = have[rank-1].replace('.', '*')
                data = {'rank': rank, 'rating': newRating[have[rank-1]]}

                self.db.child('PBhustle').child(user).child(
                    'contests').child(name).set(data)
                self.db.child('PBhustle').child(user).update(
                    {'curRating': data['rating']})

            cur_page += 1

        self.db.child('PBhustle').update({'PageIndex': cur_page})

        self.GetData()
        user = self.data['CF_id'].replace('.', '*')
        PB = self.db.child('PBhustle').child(
            user).child('curRating').get().val()
        if(PB == None):
            PB = -10000
        self.UpdatePBRatings(PB)


    def UpdateCodeforce(self):

        users=self.db.child("users").get().val()
        # print(users)

        for uid in users:
            url= "https://codeforces.com/api/user.info?handles="+users[uid]['CF_id']
            r = requests.get(url)
            rating = r.json()
            if(rating['status']=='OK'):
                if ('rating' in rating['result'][0]):

                    new_rating=str(rating['result'][0]['rating']) + ' ( ' + rating['result'][0]['rank'] + ' )'

                    self.db.child('Ratings').child(uid).update({'CF': new_rating})
                    self.db.child('users').child(uid).update({'CF_rating': new_rating})

    def UpdateCodechef(self):

        users=self.db.child("users").get().val()
        # print(users)

        for uid in users:

            if(users[uid]['CC_id']=='N/A'): continue
            
            try:
                url= 'https://competitive-coding-api.herokuapp.com/api/codechef/' + users[uid]['CC_id']
                r = requests.get(url)
                rating = r.json()
            except: continue
            if(rating['status']!='Success'):  continue
            
            new_rating=rating['rating']
            
            self.db.child('Ratings').child(uid).update({'CC': new_rating})
            self.db.child('users').child(uid).update({'CC_rating': new_rating})
    

# f=firebase()
# f.UpdateCodechef()


# f=firebase()
# print(f.getPBcontests('deepanshu_pali'))
# print(f.EmailExist('deepanshukumarpali7@gmail.com'))
#

# f.SignIn('deepanshukumarpali7@gmail.com','1234567')
# f.GetData()
# print(f.data)
