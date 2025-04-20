# season-series-bot
This project visualizes the progress of a target MLB team over the course of the current season, but with the games broken down by opponent. The bot portion then posts to the team's subreddit (or another if desired) then follows up with an explantory comment. Opponents are sorted into columns by league, then by division (both fetched in the MLB StatsAPI call), then by games played, then finally alphabetically. Games played are grouped by won/lost, and games yet to be played are broken up into Home/Away. An aggregate sum of those 4 categories is plotted over top of the breakdown.

Example:
![Stacked bar graph for the New York Mets](test.jpg)

All records/teams/statistics are pulled from MLB via `MLB-StatsAPI`, stored as `pandas` DataFrames, analyzed using `pandas` and `numpy`, then finally plotted with `matplotlib` using their FiveThirtyEight theme, but with colors set to the Mets' team colors. In the future I may make this easier to modify for other teams, since many things are hardcoded right now, but anyone is welcome to convert it to their own team and post it to their subreddits (just please acknowledge u/just-an-astronomer in the comment).