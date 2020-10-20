import gspread




sheet_id='1DHh5jPufmWLyPrYngpORRWAtslzbUA_o_8OBdGI3So4'

class PBHustle:

    def __init__(self,user):
        self.user=user
        self.contests=[]
    
    def fetch_data(self):

        gc = gspread.service_account(filename='credentials.json')
        sh = gc.open_by_key('1DHh5jPufmWLyPrYngpORRWAtslzbUA_o_8OBdGI3So4')


        contest_no=1

        while(True):
            
            sheet=sh.get_worksheet(contest_no)
            contest_no+=1

            try: name=sheet.title
            except: break

            here={}
            here['name']=name
            contest=sheet.get_all_records()

            for place in contest:
                if(self.user in  place['Who']):

                    here['rank']=place['#']
                    here['solved']=place['#ERROR!']

                    self.contests.append(here)
                    break
                        



# a=PBHustle('deepanshu_pali')
# a.fetch_data()
# print(a.contests)