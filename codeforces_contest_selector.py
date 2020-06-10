import os
import requests
from bs4 import BeautifulSoup
al_user=[]
contest_can_be_done=[]
def get_no_users():
	n=int(input("Enter Number of users = "))
	print("Enter Codeforces Handle of each user => ")
	ar=[]
	for i in range(0,n):
		s=input(str(i+1)+" = ")
		ar.append(s.strip())
	return n,ar

def get_contest_done(user_name):
	global al_user
	ur="https://codeforces.com/contests/with/"+user_name;
	#print(ur)
	r=requests.get(ur).text
	soup = BeautifulSoup(r, 'lxml')
	#print(soup)
	dt={}
	con=[]
	for each_contest in soup.find_all('a'):
		#print(each_contest.get('href'))
		contestlink=each_contest.get('href').split('/')
		if len(contestlink)<3:
			continue;
		if contestlink[1]=="contest":
			x=contestlink[2]
			if x not in dt:
				dt[x]=1;
				con.append(x)
	al_user.append(con)

def select_contest():
	global contest_can_be_done
	global al_user
	ur="https://codeforces.com/contests/page/";
	prev=None;
	bsoup=None;
	for i in range(1,10):
		k=ur+str(i)
		if i>1:
			r=requests.get(k).text
			bsoup=BeautifulSoup(r,'lxml');
			if bsoup==prev:
				break
		else:
			r=requests.get(k).text
			bsoup=BeautifulSoup(r,'lxml');
		#print(bsoup)
		for each_contest in bsoup.find_all('a', style='font-size: 0.8em;'):
			contestlink=each_contest.get('href').split('/')
			ss=contestlink[-1]
			count=0
			for i in range(0,len(al_user)):
				lt=al_user[i]
				f=1
				for j in lt:
					if j==ss:
						f=0;
						break;
				if f==1:
					count+=1
			if count==len(al_user) and contestlink[-1]!='virtual':
				contest_can_be_done.append('https://codeforces.com/contest/'+str(contestlink[-1]))
		prev=bsoup
def print_contests():
	global contest_can_be_done
	print("Following are the contests which are not given and can be given by virtually now => ")
	for contest in contest_can_be_done:
		print(contest)
def main():
	n,ar=get_no_users()
	print(n,ar)
	for i in range(0,n):
		get_contest_done(ar[i])
	#for each_user_contest_list in al_user:
	#	print(each_user_contest_list)
	select_contest()
	print_contests()

if __name__=='__main__':
	main()
