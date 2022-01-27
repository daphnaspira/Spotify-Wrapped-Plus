import pandas as pd
from matplotlib import pyplot as plt


def print_top_per_month_seconds(df, months, song_or_artist, n=5):
    
    for month in months:
        
        months_songs = df[df["Month-Year"] == month]        
        months_artists = months_songs['artistName'].unique()
        x = months_songs[['artistName','seconds']].drop_duplicates(subset = 'artistName').reset_index(drop=True)
        
        for artist in months_artists:
            a = months_songs.loc[df['artistName'] == artist]['seconds'].sum()//1000
            x.loc[x[x['artistName'] == artist].index[0],'seconds'] = round(a/60,2)
            
        print(month)
        print(x.sort_values('seconds', ascending=False).reset_index(drop=True).head(n))
        print()   

        
def percent_top_per_month(df, months, song_or_artist, n=3):
    for month in months:
        
        months_songs = df[df["Month-Year"] == month]        
        months_artists = months_songs['artistName'].unique()
        x = months_songs[['artistName','seconds']].drop_duplicates(subset = 'artistName').reset_index(drop=True)
        
        for artist in months_artists:
            a = months_songs.loc[df['artistName'] == artist]['seconds'].sum()
            x.loc[x[x['artistName'] == artist].index[0],'seconds'] = a
          
        total = months_songs['seconds'].sum()    
        top = x.sort_values('seconds', ascending=False).reset_index(drop=True).head(n)
        top['percent'] = round(top['seconds']/total,2)
        
        print(month)
        print('Total minutes per month: ', round(total/60000,2))
        print(top)
        print()

import calendar
def percent_given(df, song_or_artist, name, y, m=0, artistName=0):
    
    ## month=0 for entire year, artistname if doing song instead of artist
    
    if m == 0: month_songs = df[df['Month-Year'].astype(str).str.contains(str(y))]
    else:
        month = str.title(str(m)+'-'+str(y))        
        month_songs = df[df["Month-Year"] == month]
    
    total = month_songs['seconds'].sum()        
    
    if song_or_artist == 'song': check = 'trackName'
    elif song_or_artist == 'artist': check = 'artistName'
    
    if artistName: count = month_songs.loc[((df[check] == name) & (df['artistName'] == artistName))]['seconds'].sum()
    else: count = month_songs.loc[df[check] == name]['seconds'].sum()
    

    print('Total minutes per month: ', round(total/60000,2))   
    
    if artistName: print('In '+calendar.month_name[m]+' '+str(y)+', '+'{:.2%}'.format(count/total)+' of total listening time was spent with the '+str(song_or_artist)+' '+str(name)+' by '+str(artistName))
    else: print('In '+calendar.month_name[m]+' '+str(y)+', '+'{:.2%}'.format(count/total)+' of total listening time was spent with the '+str(song_or_artist)+' '+str(name))
    print()
    

def replays_per_time(df, song_or_artist, month_or_year, months, n=5):
    
    '''
    get current song
    if next song is the same name + artist, add count and listening time to some df
    once its not the same keep it as next song and go to next row in df
    
    index one off and end time is within an hour or something
    '''
    
    if month_or_year == 'month':
        
        for month in months:
            months_songs = df[df["Month-Year"] == month]
            months_songs.drop(months_songs[months_songs['seconds'] < 30000].index, inplace=True)
            
            
            duplicate = months_songs[months_songs.duplicated('trackName')]
            songs = duplicate['trackName'].unique()
            artists = duplicate['artistName'].unique()
            
            for song in songs:
                s = duplicate[duplicate['trackName'] == song]
                print(s)
                
                
            
    if month_or_year == 'year':
        
        month_songs = df[df['Month-Year'].astype(str).str.contains('2021')]
    
    #if song_or_artist == 'song':
        #return
    #if song_or_artist == 'artist':
        #return
    
    ## return the top n songs/artists that were played in a row the most, with number of replays in longest string, listening time in string of listens, month/year
    # top = x.sort_values('count', ascending=False).reset_index(drop=True).head(n)

def plot_top_over_time(top_df, play_freqs_df, dates, date_column_name, song_or_artist):
    """
    top_df = (df) the dataframe result of calling top_per_month()
    play_freqs_df = (df) the dataframe result of calling play_frequencies()
    dates = (list) the range of time periods to use (month-year or days)
    date_column_name = (str) the name of the time period column to use ('Date' or 'Month-Year')
    
    Returns an overlaid line plot with one line for each song/artist over the time period range that you specify
    x-axis is the time period and y-axis is number of times that song/artist was played in the time period
    """
    
    if song_or_artist == 'song':
        item_column_name = 'trackName'
    if song_or_artist == 'artist':
        item_column_name = 'artistName'
        
    top = top_df[item_column_name].unique()
    
    all_top_plays_df = pd.DataFrame()
    for item in top:
        all_plays = play_freqs_df[play_freqs_df[item_column_name]==item]
        all_top_plays_df = all_top_plays_df.append(all_plays)
    
    plt.figure(figsize=(15,10))

    for item in top:
        one_item_freqs = all_top_plays_df[all_top_plays_df[item_column_name]==item]
        freq_list = []
        for date in dates:
            if (one_item_freqs[date_column_name]==date).any():
                that_day = one_item_freqs[one_item_freqs[date_column_name]==date]
                freq_list.append(int(sum(that_day['Number of Plays'])))
            else:
                freq_list.append(0)
        dates_and_freqs_df = pd.DataFrame(data=freq_list, index=dates)
        dates_and_freqs_df.index = dates_and_freqs_df.index.to_timestamp()
        plt.plot(dates_and_freqs_df, label=item)
        plt.legend()
     
    plt.savefig(f'top_{song_or_artist}_per_month_over_time.png')
    plt.show()
    
