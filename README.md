# season-series-bot
A bot that creates a jpg image of stacked bar graph of an MLB team using `MLB-StatsAPI`, `pandas`, and `matplotlib`. Currently set to the New York Mets but can be tweaked to cover any MLB team. To use the bot functionality, you must provide your own bot credentials and store them in a file called `credentials.txt`. The file also assumes the credentials file has a flair id (since r/NewYorkMets requires flairs upon submission). People using this need to either to find the correct flair ID ([which I found here](https://www.reddit.com/r/redditdev/comments/ovte4q/praw_flair_a_post/)) or to remove references to the flair in the code.

Example:
![Stacked bar graph for the New York Mets](test.jpg)