"""
	Console based reddit client by /u/cris9696

	Released under MIT license, do what you want but if I was useful please mention me! ;)
"""

import sys
import getpass
import requests
import json
import os
import webbrowser


warpIfLenIsMoreThan = 65


def getSubreddit(subreddit = "/r/all",limit = 15,sort = "hot"):
	limit = int(limit)
	limit = limit if limit > 0 else 1
	params = {"limit": limit}
	if(len(subreddit)>3):
		r = requests.get("http://reddit.com" + subreddit + "/" + sort + ".json", params=params)
		try: 
			page = json.loads(r.content)
			if "data" in page:
				ps = [dict() for x in range(limit)]
				for i,c in enumerate(page["data"]["children"]):
					if i>=limit:
						break
					ps[i]["title"] = c["data"]["title"]
					ps[i]["score"] = c["data"]["score"]
					ps[i]["subreddit"] = c["data"]["subreddit"]
					ps[i]["url"] = c["data"]["url"]
					ps[i]["permalink"] = c["data"]["permalink"]
				return ps
			else:
				return False
		except ValueError:
			return False
	return False

def printPosts(ps,subreddit = "all"):
	print("\n\n")
	print(subreddit)
	if ps:
		for post in ps:
			print (str(post["score"]) + "\t- " +(post["title"] if len(post["title"])<warpIfLenIsMoreThan else post["title"][:warpIfLenIsMoreThan]+"..."))
	else:
		print ("Impossible to fetch the requested subreddit!\nCheck if it exists or if you are requesting too much in a small time or if reddit is down")

def execute(command):
	global posts

	##############VISIT /R/#############
	if command.lower().startswith("/r/"):
		params = command.split()
		if len(params) is 1:
			posts = getSubreddit(params[0])
			printPosts(posts,params[0])

		elif len(params) is 2:
			if params[1].isdigit():
				posts = getSubreddit(params[0],limit = params[1])
				printPosts(posts,params[0])
			else:
				sort = params[1]
				if sort.lower() == "hot" or sort.lower() == "new":
					posts = getSubreddit(params[0],sort = sort.lower())
					printPosts(posts,params[0])
				else:
					return False

		elif len(params) is 3:
			if params[1].isdigit():
				sort = params[2]
				if sort.lower() == "hot" or sort.lower() == "new":
					posts = getSubreddit(params[0],sort = sort.lower(),limit = params[1])
					printPosts(posts,params[0])
				else:
					return False
			else:
				sort = params[1]
				if sort.lower() == "hot" or sort.lower() == "new":
					posts = getSubreddit(params[0],sort = sort.lower(),limit = params[2])
					printPosts(posts,params[0])
				else:
					return False
		else:

			return False
	###############EXIT##################
	elif command.lower() == "exit":
		sys.exit(0)
	elif command.lower() == "help":
		print("/r/subredditName\t\tto view the subreddit called subredditName")
		print("open<number>\t\t\tto open in a browser the link at <number>th position, first post is position 1")
		print("exit\t\t\t\tto exit this program")
		print("help\t\t\t\tshow this")
		print("\nadditional parameters for /r/subredditName command:")
		print("<number of posts to show>\tto show only a limited number of posts, default is 15")
		print("hot / new\t\t\tto display the hot or new section of the subreddit, default is hot")
		print("Example: /r/all new 25\t\tShows 25 posts from the /new page of /r/all")
	###############OPEN##################
	elif command.lower().startswith("open"):
		which = command.lower().split()[1]
		if which.isdigit():
			if len(posts)>int(which)-1 and int(which)>0:
				webbrowser.open("http://www.reddit.com" + posts[int(which)-1]["permalink"],2)
			else:
				print ("The post is out of index")
		else:
			print (which + " is not a valid number!")

	else:
		return False
	return True
################################################################################

print("Getting /r/all")
execute("/r/all")

cmd = None

while True:
	if cmd and len(cmd)>0:
		if not execute(cmd):
			print (cmd + " is not a valid command! Write 'help' to see a list of avaible commands")
	cmd = raw_input("\n: ")
	




	
