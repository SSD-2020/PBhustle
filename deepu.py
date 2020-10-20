import gspread

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1DHh5jPufmWLyPrYngpORRWAtslzbUA_o_8OBdGI3So4')
sheet_ins=sh.get_worksheet(1)
print(sheet_ins.col_count)
record = sheet_ins.get_all_records()
for i in record:
    print(i)
    print()