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


warpIfLenIsMoreThan = 55


def getSubreddit(subreddit = "/r/all",limit = 15,sort = "hot"):
    limit = int(limit)
    limit = limit if limit > 0 else 1
    params = {"limit": limit}
    if(len(subreddit)>3):
        r = requests.get("http://reddit.com" + subreddit + "/" + sort + ".json", params=params)
        try: 
            page = json.loads(r.content)
            if "data" in page:
                sourcePosts = [dict() for x in range(limit)]    #holy shit this is really bad, i need to use classes
                for i,singlePost in enumerate(page["data"]["children"]):
                    if i>=limit:
                        break
                    sourcePosts[i]["title"] = singlePost["data"]["title"]
                    sourcePosts[i]["score"] = singlePost["data"]["score"]
                    sourcePosts[i]["subreddit"] = singlePost["data"]["subreddit"]
                    sourcePosts[i]["url"] = singlePost["data"]["url"]
                    sourcePosts[i]["permalink"] = singlePost["data"]["permalink"]
                return sourcePosts
            else:
                return False
        except ValueError:
            return False
    return False

def printPosts(sourcePosts,subreddit = "all"):
    print("\n\n")
    print(subreddit)
    if sourcePosts:
        i = 0 
        for post in sourcePosts:
            if "score" in post:
                print (str(i+1) + ")\t" + str(post["score"]) + "\t- " +(post["title"] if len(post["title"])<warpIfLenIsMoreThan else post["title"][:warpIfLenIsMoreThan]+"..."))
                i+=1
    else:
        print ("Impossible to fetch the requested subreddit!\nCheck if it exists or if you are requesting too much in a small time or if reddit is down")

def execute(command):
    global posts
    

    command = command.lower().strip()
    ##############VISIT /R/#############
    if command.startswith("/r/"):
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
    elif command == "exit" or command == "quit":
        sys.exit(0)
    ###############HELP#################
    elif command == "help":
        print("/r/subredditName\t\tto view the subreddit called subredditName")
        print("open<number>\t\t\tto open in a browser the link at <number>th position, first post is position 1")
        print("exit\t\t\t\tto exit this program")
        print("help\t\t\t\tshow this")
        print("\nadditional parameters for /r/subredditName command:")
        print("<number of posts to show>\tto show only a limited number of posts, default is 15")
        print("hot / new\t\t\tto display the hot or new section of the subreddit, default is hot")
        print("Example: /r/all new 25\t\tShows 25 posts from the /new page of /r/all")
    ###############OPEN##################   #I could use a regex
    elif command.startswith("open"):
        openArguments = command.split()
        if openArguments[0] == "open" and len(openArguments) == 2:
            if not posts:
                print("Posts are not loaded!")
                return True

            which = openArguments[1]
            if which.isdigit():
                if len(posts)>int(which)-1 and int(which)>0:
                    webbrowser.open("http://www.reddit.com" + posts[int(which)-1]["permalink"],2)
                else:
                    print ("The post is out of index")
            else:
                print (which + " is not a valid number!")
        elif command == "open":
            print ("Invalid number of arguments for the command open")
        else:
            return False
    else:
        return False

    return True
################################################################################

print("Getting /r/python")
execute("/r/python")

cmd = None

while True:
    if cmd and len(cmd)>0:
        if not execute(cmd):
            print (cmd + " is not a valid command! Write 'help' to see a list of avaible commands")
    cmd = raw_input("\n>> ")
