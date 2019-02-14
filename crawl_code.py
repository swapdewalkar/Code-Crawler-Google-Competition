from urllib.request import urlopen
import os
import os.path
import urllib.request
import json
import sys


NO_OF_USER_ON_ONE_PAGE=30

if len(sys.argv)==1:
	print("Usage: python crawl_code.py OUTPUT_FOLDER")

output_folder=sys.argv[1]
token="MjdhMTU1ZWJhMjQxYzBhZjE1OTBiNDVjNTliMzIwNDZ8fDE1NTAwODk1NDY2NDcyMzI="
problem_id="5753053697277952"
contest_id="4314486"
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
		links+=['https://code.google.com/codejam/contest/'+str(contest_id)+'/scoreboard/do/?cmd=GetSourceCode&problem='+str(problem_id)+'&io_set_id=0&username='+username+'&csrfmiddlewaretoken='+str(token)]
	print("No of usernames found: "+str(len(links)))
	return links

pagelinks=get_page_links(no_of_participants,contest_id,token)
usernames=[]
i=1
for link in pagelinks:
	print("Fetching Page "+str(i)+"/"+str(len(pagelinks)))
	res=json.load(urlopen(link))
	for row in res['rows']:
		usernames+=[row['n']]
	i += 1
	break
os.mkdir(output_folder)
code_no=1
userlinks=get_user_links(usernames,contest_id,token,problem_id)
for link,username in zip(userlinks,usernames):
	if FLAG==1:
		name = username
	else:
		name= "Code"+str(code_no)
	print("Fetching code "+str(code_no)+"/"+str(len(userlinks)))
	urllib.request.urlretrieve(link,output_folder+"/"+name+".zip")
	code_no+=1
	