from urllib.request import urlopen
import os
import os.path
import urllib.request
import json
import sys

#If you are getting error use difference token

NO_OF_USER_ON_ONE_PAGE=30

if len(sys.argv)==1:
	print("Usage: python crawl_code.py OUTPUT_FOLDER")

output_folder=sys.argv[1]
token="M2VlMzg3NzY1NmEyODlkMzg2MzdlMzhmYjlkOTAzN2Z8fDE1NTAxMzU0NjA3OTEyNjg%3D"
problem_id="5753053697277952"
contest_id="4314486"
set_id=0  # 0 for small and 1 for large
no_of_participants=5950
FLAG=1 # make 0 if you want to save without username

def get_page_links(NO_OF_PARTICIPANTS,contest_id,token):
	links=[]
	for i in range(int(NO_OF_PARTICIPANTS/NO_OF_USER_ON_ONE_PAGE)):
		start_pos=i*NO_OF_USER_ON_ONE_PAGE+1
		links+=['https://code.google.com/codejam/contest/'+str(contest_id)+'/scoreboard/do/?cmd=GetScoreboard&contest_id='+str(contest_id)+'&show_type=all&start_pos='+str(start_pos)+'&csrfmiddlewaretoken='+str(token)]
	print("Total links :",len(links))
	return links

def get_user_links(usernames,contest_id,token,problem_id):
	links=[]
	for username in usernames:
		links+=['https://code.google.com/codejam/contest/'+str(contest_id)+'/scoreboard/do/?cmd=GetSourceCode&problem='+str(problem_id)+'&io_set_id='+str(set_id)+'&username='+username+'&csrfmiddlewaretoken='+str(token)]
	print("No of usernames found: "+str(len(links)))
	return links

pagelinks=get_page_links(no_of_participants,contest_id,token)
usernames=[]
i=1
for link in pagelinks:
	while True:
		try:
			print("Fetching Page "+str(i)+"/"+str(len(pagelinks)))
			res=json.load(urlopen(link))
			for row in res['rows']:
				usernames+=[row['n']]
			i += 1
		except KeyboardInterrupt:
			exit()
		except :
			continue
		break

os.mkdir(output_folder)
code_no=1
userlinks=get_user_links(usernames,contest_id,token,problem_id)
for link,username in zip(userlinks,usernames):
	try:
		if FLAG==1:
			name = username
		else:
			name= "Code"+str(code_no)
		print("Fetching code "+str(code_no)+"/"+str(len(userlinks)))
		urllib.request.urlretrieve(link,output_folder+"/"+name+".zip")
		code_no+=1
	except KeyboardInterrupt:
			exit()
	except:
		print("Error for user: "+username+" Link:"+link)
