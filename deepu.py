import gspread

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1DHh5jPufmWLyPrYngpORRWAtslzbUA_o_8OBdGI3So4')

worksheet = sh.sheet1.get_all_records()
for i in worksheet:
    print(i)
    print()