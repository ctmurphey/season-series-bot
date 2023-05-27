import praw
from datetime import date
from stackedbar import make_graph

make_graph() #generate a new plot, saved as test.jpg

f = open("credentials.txt")
client_id = f.readline().split()[1]
secret = f.readline().split()[1]
username = f.readline().split()[1]
pwd = f.readline().split()[1]

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=secret,
    user_agent=username,
    username=username,
    password=pwd
)
today = date.today()
subreddit = reddit.subreddit("NewYorkMets") #uncomment when deploying
# subreddit = reddit.subreddit("PythonSandlot") # for testing/debugging

print(subreddit.display_name)
print(reddit.user.me())
title = "Mets Current Season Series Progress: "+str(today)
my_post = subreddit.submit_image(title=title, image_path='test.jpg')

# comment_str = "If you see any issues, please message u/just-an-astronomer"
comment_str = '''🤖^beep ^boop ^I'm ^a ^bot Hello, I'm u/season-series-bot. I'll 
be taking over the season series graphics from now on. The account change from 
human to bot is so that I can be further automated while keeping the personal 
account more safe/separate. Any prototype upgrades will be tested in r/PythonSandlot 
before being deployed here.

If you do notice any issues, please contact u/just-an-astronomer.

[My Github Repo](https://github.com/ctmurphey/season-series-bot)'''
my_post.reply(comment_str)