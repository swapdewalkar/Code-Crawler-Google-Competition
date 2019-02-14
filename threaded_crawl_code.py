from urllib.request import urlopen
import os
import os.path
import urllib.request
import json
import sys
from multiprocessing import Process, Queue, Lock, Pipe

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

# q = []
THREADS=int(sys.argv[2])
NO_OF_PAGES_PER_THREAD=int(len(pagelinks)/THREADS)+1
def extractPages(id,):
	file=open("TEMP/T"+str(id),'w')
	usernames=[]
	start=id*NO_OF_PAGES_PER_THREAD
	end=min((id+1)*NO_OF_PAGES_PER_THREAD,len(pagelinks))
	print(start,end-1)
	i=1
	length=len(pagelinks[start:end])
	for link in pagelinks[start:end]:
		while True:
			try:
				print("Thread "+str(id)+" Fetching Page "+str(i)+"/"+str(length))
				res=json.load(urlopen(link))
				for row in res['rows']:
					usernames+=[row['n']]
				i += 1
			except KeyboardInterrupt:
				exit()
			except :
				continue
			break
	for user in usernames:
		file.write(user+"\n")
	file.close()
	# lock.acquire()
	# q.put(usernames)
	# print(q)
	# lock.release()
os.system("rm -rf TEMP")
os.mkdir("TEMP")
os.mkdir(output_folder)


def extractCode(id):
	start=id*NO_OF_USER_PER_THREAD
	end=min((id+1)*NO_OF_USER_PER_THREAD,len(usernames))
	print(start,end-1)
	length=len(usernames[start:end])
	code_no=1
	userlinks=get_user_links(usernames[start:end],contest_id,token,problem_id)
	for link,username in zip(userlinks,usernames[start:end]):
		try:
			if FLAG==1:
				name = username
			else:
				name= "Code"+str(code_no)
			print("Thread "+str(id)+" Fetching code "+str(code_no)+"/"+str(length))
			urllib.request.urlretrieve(link,output_folder+"/"+name+".zip")
			code_no+=1
		except KeyboardInterrupt:
				exit()
		except:
			print("Error for user: "+username+" Link:"+link)

p = []
usernames = []
for id in range(0,THREADS):
	p += [Process(target=extractPages, args=(id,))]
print(len(p))
for thread in p:
	thread.start()
for thread in p:
	thread.join()
usernames=[]
for id in range(0,THREADS):
	with open("TEMP/T"+str(id)) as f:
		for user in f:
			usernames+=[user.rstrip()]

print(len(usernames))
NO_OF_USER_PER_THREAD=int(len(usernames)/THREADS)+1


p = []
for id in range(0,THREADS):
	p += [Process(target=extractCode, args=(id,))]
for thread in p:
	thread.start()
for thread in p:
	thread.join()