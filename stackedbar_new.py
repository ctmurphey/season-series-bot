import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from matplotlib import gridspec
from matplotlib import gridspec
import statsapi as mlbstats
from matplotlib import rcParams

plt.style.use('fivethirtyeight')


def fetch_games(teamname='nyn', year=2025):
    '''Fetch data from MLB Stats API and generate a dataframe of the regular season games.
    Params:
        teamname (str): team of interest to get games for
        year (int): season to get data for
    Returns:
        sched_df (pandas.DataFrame): dataframe of games in the season'''
    
    team = mlbstats.lookup_team(teamname)[0]
    sched = mlbstats.schedule(start_date='01/01/'+str(year), end_date='12/31/'+str(year), team=str(team['id']))

    sched_df = pd.DataFrame(sched)
    sched_df = pd.DataFrame(sched_df.loc[sched_df['status'] != 'Postponed'])  #remove postponed games
    sched_df = pd.DataFrame(sched_df.loc[sched_df['game_type'] == 'R']) #remove spring training

    return sched_df, team


def reduce_data(schedule, team):
    '''Take schedule dataframe and convert it into the stats we want to plot.
    Params:
        schedule (pandas.DataFrame): dataframe of season schedule generated in fetch_games
    Returns:
        team_df (pandas.DataFrame): dataframe with the home/away stats by opponent team'''
    
    teamname = team['name']

    ### First, get all of the opponents
    opponents = list(set(schedule[['home_name', 'away_name']].values.flatten()))
    opponents.remove(teamname)
    team_df = pd.DataFrame(index=opponents)
    for x in ['home_wins', 'away_wins', 'home_losses', 'away_losses', 'incomplete_home', 'incomplete_away']:
        team_df[x] = [0]*len(opponents)
    for x in ['division', 'record']:
        team_df[x] = ''
    for ind, game in schedule.iterrows():

        if game['home_name'] in [teamname]:
            if game['winning_team'] in [teamname]:
                team_df.loc[game['losing_team'], 'home_wins'] += 1
            elif game['status'] in ['Final', 'Completed Early: Rain', 'Game Over']:
                team_df.loc[game['winning_team'], 'home_losses'] += 1
                pass
            else:
                team_df.loc[game['away_name'], 'incomplete_home'] += 1
                pass
        else:
            if game['winning_team'] in [teamname]:
                team_df.loc[game['losing_team'], 'away_wins'] += 1
            elif game['status'] in ['Final', 'Completed Early: Rain', 'Game Over']:
                team_df.loc[game['winning_team'], 'away_losses'] += 1
            else:
                team_df.loc[game['home_name'], 'incomplete_away'] += 1
    team_df['total_wins'] = team_df['home_wins'] + team_df['away_wins']
    team_df['total_losses'] = team_df['home_losses'] + team_df['away_losses']
    team_df['total_games'] = team_df['total_wins'] + team_df['total_losses'] + \
                                team_df['incomplete_home'] + team_df['incomplete_away']
    team_df['nickname'] = [x.split()[-1] if x.split()[-1] not in ['Sox', 'Jays']
                           else ' '.join(x.split()[-2:])
                            for x, i in team_df.iterrows()]

    ### basic team info (division record, nickname)
    divs = ['ALE', 'ALC', 'ALW', 'NLE', 'NLC', 'NLW']
    divisions = pd.DataFrame(list(mlbstats.standings_data().values()))

    for i, division in divisions.iterrows():
        for div_team in division['teams']:
            if div_team['name'] != teamname:
                team_df.loc[div_team['name'], 'division'] = division['div_name']
                team_df.loc[div_team['name'], 'record'] = str(div_team['w']) + '-' + str(div_team['l'])
    team_df['division'] = pd.Categorical(team_df['division'], 
                                         ['National League East', 'National League Central', 'National League West',
                                          'American League East', 'American League Central', 'American League West'])
    team_df.sort_values(['division', 'total_games', 'nickname'], ascending=[True, False, True], inplace=True)

    return team_df, teamname

def make_plots(df, team, savefig=True, savefile='test.jpg'):
    '''Makes the plots and optionally saves by default. Top row total season progress. Middle row
    home/away splits, bottom row broken down by team
    Params:
        df (pandas.DataFrame): dataframe of opponent win/loss/incompletes
        savefig (bool, default True): whether to save or just display the figure
        savefile (str, default test.jpg): name to save file as if savefig enabled'''
    
    w = 0.9 #main bar width
    # bar colors
    wincolor = 'cornflowerblue'
    losscolor = 'darkorange'
    inchomecolor = 'silver'
    incawaycolor = 'gray'

    # fig = plt.figure(figsize=(16.75, 10), constrained_layout=True)
    fig = plt.figure(figsize=(18, 13), constrained_layout=True)
    gs = gridspec.GridSpec(
        3, 2,  # 3 rows, 2 columns
        height_ratios=[1, 1, 15],
        width_ratios=[1, 1],  # Initial, for rows that need it
        figure=fig
    )
    ### Setting the correct axes proportions
    ax_top = fig.add_subplot(gs[0, :])
    ax_mid1 = fig.add_subplot(gs[1, 0])
    ax_mid2 = fig.add_subplot(gs[1, 1])
    gs_bottom = gridspec.GridSpecFromSubplotSpec(
        1, 2, 
        subplot_spec=gs[2, :], 
        width_ratios=[13, 6]
    )

    ax_bot1 = fig.add_subplot(gs_bottom[0, 0])
    ax_bot2 = fig.add_subplot(gs_bottom[0, 1])

    ### First plot: the top (total season progress win/loss/inc_home/inc_away)
    total_wins = df['home_wins'].sum()+df['away_wins'].sum()
    total_loss = df['home_losses'].sum()+df['away_losses'].sum()
    inc_home = df['incomplete_home'].sum()
    inc_away = df['incomplete_away'].sum()

    left = 0
    colors = [wincolor, losscolor, inchomecolor, incawaycolor]
    labels = ['won', 'lost', 'incomplete home', 'incomplete_away']
    for i, stat in enumerate([total_wins, total_loss, inc_home, inc_away]):
        if stat != 0:
            ax_top.barh(0, stat, left=left, color=colors[i], label=labels[i], edgecolor='k')
            ax_top.text(left+stat/2, -0.05, round(stat), weight='bold', va='center', ha='center',
                        size=24)
            left += stat
    ax_top.axis('off')
    ax_top.set_title('Total Season:', size=32, weight='bold')
    ax_top.set_xlim(0, left+0.5)

    ### Next plots: home/away splits
    left = 0
    for i, stat in enumerate([df['home_wins'].sum(), df['home_losses'].sum(), df['incomplete_home'].sum()]):
        if stat != 1:
            ax_mid1.barh(0, stat, left=left, color=colors[i], label=labels[i], edgecolor='k')
            ax_mid1.text(left+stat/2, -0.05, round(stat), weight='bold', va='center', ha='center',
                        size=24)
            left += stat
    ax_mid1.axis('off')
    ax_mid1.set_title('Home:', size=28, weight='bold')
    ax_mid1.set_xlim(0, left+0.5) # extra 0.5 makes sure the black border goes around the bar
    
    left = 0
    colors = [wincolor, losscolor, incawaycolor]
    labels = ['won', 'lost', 'incomplete_away']
    for i, stat in enumerate([df['away_wins'].sum(), df['away_losses'].sum(), df['incomplete_away'].sum()]):
        if stat != 1:
            ax_mid2.barh(0, stat, left=left, color=colors[i], label=labels[i], edgecolor='k')
            ax_mid2.text(left+stat/2, -0.05, round(stat), weight='bold', va='center', ha='center',
                        size=24)
            left += stat
    ax_mid2.axis('off')
    ax_mid2.set_title('Away:', size=28, weight='bold')
    ax_mid2.set_xlim(0, left+0.5)

    
    ### Finally, the breakdown-by-team plots
    ax_bot = (ax_bot1, ax_bot2)
    lengths = [14, 15]
    leagues = ["National League", "American League"]
    locs = ["center", "center"]
    colors = [wincolor, losscolor, inchomecolor, incawaycolor]

    for i in [0,1]:
        left = pd.Series([0]*lengths[i]) # left bound of the next bars

        for k, stat in enumerate(['total_wins', 'total_losses', 'incomplete_home', 'incomplete_away']):
            x = np.arange(lengths[i])

            ax_bot[i].barh(x, df[stat][14*i : 14+i*15], w, left=left,
                        color=colors[k], edgecolor='k')
            for j in x:
                if int(df[stat].iloc[i*lengths[0]+j]) != 0:
                    ax_bot[i].text(left.iloc[j]+df[stat].iloc[i*lengths[0]+j]/2, j+0.05, int(df[stat].iloc[i*lengths[0]+j]), weight='bold', va='center', ha='center',
                            size=24)
            left += df[stat].iloc[14*i : 14+i*15].values


    
        ax_bot[i].set(xlim=(0, max(left)+0.5), ylim=(-0.5, lengths[i]-0.4))
        ax_bot[i].set_title(leagues[i], loc=locs[i], weight='bold', va='center', ha='center', size=24)
        ax_bot[i].set_yticks(ticks = x, labels=df['nickname'][14*i : 14+i*15] + [' ('] + df['record'][14*i : 14+i*15] + [')'],
                              size=22)


        ax_bot[i].invert_yaxis()
        ax_bot[i].spines['bottom'].set_visible(False)
        ax_bot[i].spines['right'].set_visible(False)
        ax_bot[i].set_xticks([])

    ### Creating the suptitle:
    fig.suptitle(f"{team} Current Season Series Progress\n{date.today()} ({total_wins}-{total_loss}, {inc_home+inc_away} GR)"
                 , size=32
                 , weight='bold',)# va='bottom')


    if savefig:
        plt.savefig(savefile)
    else:
        plt.show()       


if __name__ == "__main__":
    schedule, team = fetch_games()
    df = reduce_data(schedule, team)
    make_plots(df[0], df[1], savefile='test2.jpg')
    