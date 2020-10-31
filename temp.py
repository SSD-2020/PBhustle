#leaderboard function
#add the header files
def get_all():
	res=db.child("users").get().val()
	data={} #return user_id as key and latest rating as value
	for i in res:
		url= "https://codeforces.com/api/user.info?handles="+res[i]['CF_id']
		r = requests.get(url)
		rating = r.json()
		if(rating['status']=='OK'):
			if 'rating' in rating['result'][0]:
				data[i]=rating['result'][0]['rating']
			else:
				data[i]=0 #default value as 0
	#print(data)
	return data