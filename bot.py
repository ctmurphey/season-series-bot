import praw
from datetime import date
from stackedbar import make_graph
from time import sleep

make_graph() #generate a new plot, saved as test.jpg

f = open("credentials.txt")
client_id = f.readline().split()[1]
secret = f.readline().split()[1]
username = f.readline().split()[1]
pwd = f.readline().split()[1]
flair = f.readline().split()[1]

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=secret,
    user_agent=username,
    username=username,
    password=pwd
)
today = date.today()
subreddit = reddit.subreddit("NewYorkMets") #uncomment when deploying
# subreddit = reddit.subreddit("testingground4bots") # for testing/debugging

print(subreddit.display_name)
print(reddit.user.me())
title = "Mets Current Season Series Progress: "+str(today)
my_post = subreddit.submit_image(title=title, image_path='test.jpg', flair_id=flair)
print("Image posted")
# comment_str = "If you see any issues, please message u/just-an-astronomer"
comment_str = '''beep ^boop beep ^I'm ^a ^bot Hello, I'm u/season-series-bot. I
was off for a while but I'm back now. I post our current record, broken down by
opponent after each series.

If you do notice any issues, please contact u/just-an-astronomer. If you have any 
suggestions for improvement or other things to plot/post with this graph, feel 
free to reply to this comment.

[My Github Repo](https://github.com/ctmurphey/season-series-bot) 
[Creator's Website](https://ctmurphey.github.io/)'''

sleep(3) #giving some time before commenting
my_post.reply(comment_str)
print("Comment posted")