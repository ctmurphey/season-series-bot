# season-series-bot
A bot for Reddit that automatically posts the season series status of a team over a certain time frame (like at the end of each game day). The non-bot version of this code (and prototype upgrades) can be found in the `mets-season-series` folder in [my baseball repo](https://github.com/ctmurphey/baseball). 

### Planned upgrades:
1. Automating bot to wait until right time to post figure as opposed to once the code is running
    1. Will require constant running/deployment
2. Get to run constantly and only update at appropriate time
    1. Allow time frame to vary (after games/series, daily, weekly, etc.)
    2. Will require database setup
3. Allow handling of multiple teams with potentially unique times for posting

### Non-deployed upgrade plans:
1. Make backend in Julia
2. Use pie charts instead of stacked bar charts