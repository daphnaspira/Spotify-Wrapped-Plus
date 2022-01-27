import pandas as pd
from matplotlib import pyplot as plt

def get_listening_history(filename):
    """
    filename: (str) the path to the .json file containing the spotify listening history
    
    Loads in the listening history as a pandas dataframe
    Adds columns to the dataframe based on the information in the 'endTime' column of the df:
    'Date' contains the year-month-day date that the song was played
    'Time' contains the hour-minute-second time that the song finished playing
    'Month-Year' contains the year-month date that the song was played
    """
    df = pd.read_json(filename)
    df['Date'] = pd.to_datetime(df['endTime']).dt.date
    df['Time'] = pd.to_datetime(df['endTime']).dt.time
    df['Month-Year'] = pd.to_datetime(df['endTime']).dt.to_period('m')
    return df

def merge_songs(df, song_to_merge, original_song):
    """
    song_to_merge = (str) the alternate name for the song (will be replaced)
    original song = (str) the name of the song that you want to display (what to replace with)
    
    Use if the same song exists in two different versions on Spotify and is being counted separately but you want them to be counted as one
    e.g. the original version and extended version of a song
    """
    df.replace(song_to_merge,original_song,inplace=True)
    return df

def play_frequencies(df, dates, date_column_name, song_or_artist):
    """
    df = (dataframe) the name of the dataframe with the listening history
    dates = (list) the range of periods to use (days or months)
    date_column_name = (str) the name of the time period column to use ('Date' or 'Month-Year')
    
    Returns a new dataframe with the number of times each song/artist was played within the time period specified (each day or month)
    """
    play_freqs_df = pd.DataFrame()
    for date in dates:
        if song_or_artist == 'song':
            value_counts_df = df[df[date_column_name]==date][['trackName','artistName']].value_counts().to_frame().reset_index().rename(columns={0:'Number of Plays'})
        if song_or_artist == 'artist':
            value_counts_df = df[df[date_column_name]==date]['artistName'].value_counts().to_frame().reset_index().rename(columns={'index':'artistName','artistName':'Number of Plays'})
        value_counts_df[date_column_name] = date
        play_freqs_df = play_freqs_df.append(value_counts_df)
    play_freqs_df.reset_index(drop=True)
    return play_freqs_df

def print_top_per_month(df, months, song_or_artist, n=5):
    """
    df = (dataframe) the name of the dataframe with the listening history
    months = (list) the range of months-year pairs to use
    n (optional) = (int) the number of top songs/artists to display for each month. default is set to 5.
    
    Prints out the top n songs for each month with the name of the song/artist, and the number of times the song/artist was played in that month.
    """   
    for month in months:
        months_songs = df[df["Month-Year"] == month]
        if song_or_artist == 'song':
            freq = months_songs[['trackName','artistName']].value_counts()
        if song_or_artist == 'artist':
            freq = months_songs['artistName'].value_counts()
        print(month)
        print(freq.head(n))
        print()
        
def top_per_month(df, months, song_or_artist, n=1):
    """
    df = (dataframe) the name of the dataframe with the listening history
    months = (list) the range of month-year pairs to use
    n (optional) = (int) the number of top songs/artists to display for each month. default is set to 1.
    Returns a dataframe containing the top n songs/artists for each month with the name of the song/artist, number of times the song/artist was played in the month, and month.
    """
    top_df = pd.DataFrame()
    for month in months:
        months_songs = df[df["Month-Year"] == month]
        if song_or_artist == 'song':
            freq = months_songs[['trackName','artistName']].value_counts().to_frame().reset_index().rename(columns={0:'Number of Plays'})
        if song_or_artist == 'artist':
            freq = months_songs['artistName'].value_counts().to_frame().reset_index().rename(columns={'index':'artistName','artistName':'Number of Plays'})
        top_n = freq.head(n)
        top_n['Month-Year'] = month
        top_df = top_df.append(top_n)
    return top_df

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