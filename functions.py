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

def song_play_frequencies(df, dates, date_column_name):
    """
    df = (dataframe) the name of the dataframe with the listening history
    dates = (list) the range of periods to use (days or months)
    date_column_name = (str) the name of the time period column to use ('Date' or 'Month-Year')
    
    Returns a new dataframe with the number of times each song was played within the time period specified (each day or month)
    """
    song_freqs_df = pd.DataFrame()
    for date in dates:
        value_counts_df = df[df[date_column_name]==date][['trackName','artistName']].value_counts().to_frame().reset_index().rename(columns={0:'Number of Plays'})
        value_counts_df[date_column_name] = date
        song_freqs_df = song_freqs_df.append(value_counts_df)
    song_freqs_df.reset_index(drop=True)
    return song_freqs_df

def merge_songs(song_to_merge, original_song):
    """
    song_to_merge = (str) the alternate name for the song (will be replaced)
    original song = (str) the name of the song that you want to display (what to replace with)
    
    Use if the same song exists in two different versions on Spotify and is being counted separately but you want them to be counted as one
    e.g. the original version and extended version of a song
    """
    df.replace(song_to_merge,original_song,inplace=True)
    return df

def print_top_songs_per_month(df, months, n=5):
    """
    df = (dataframe) the name of the dataframe with the listening history
    months = (list) the range of months to use
    n (optional) = (int) the number of top songs to display for each month. default is set to 5.
    
    Prints out the top n songs for each month with the name of the song, name of the artist, and the number of times the song was played in that month.
    """
    for month in months:
        months_songs = df[df["Month-Year"] == month]
        freq = months_songs[['trackName','artistName']].value_counts()
        print(month)
        print(freq.head(n))
        print()
        
def top_songs_per_month(df, months, n=5):
    """
    df = (dataframe) the name of the dataframe with the listening history
    months = (list) the range of months to use
    n (optional) = (int) the number of top songs to display for each month. default is set to 5.
    Returns a dataframe containing the top n songs for each month with the name of the song, name of the artist, number of times the song was played in the month, and month.
    """
    top_songs_df = pd.DataFrame()
    for month in months:
        months_songs = df[df["Month-Year"] == month]
        freq = months_songs[['trackName','artistName']].value_counts().to_frame().reset_index().rename(columns={0:'Number of Plays'})
        top_n = freq.head(n)
        top_n['Month-Year'] = month
        top_songs_df = top_songs_df.append(top_n)
    return top_songs_df

def plot_top_songs_over_time(top_songs_df, monthly_song_freqs_df, dates, date_column_name):
    
    top_songs = top_songs_df['trackName'].unique()
    
    all_plays_of_top_songs_df = pd.DataFrame()
    for song in top_songs:
        all_plays = monthly_song_freqs_df[monthly_song_freqs_df['trackName']==song]
        all_plays_of_top_songs_df = all_plays_of_top_songs_df.append(all_plays)
    
    plt.figure(figsize=(20,15))
    pd.plotting.register_matplotlib_converters()

    for song in top_songs:
        one_song_freqs = all_plays_of_top_songs_df[all_plays_of_top_songs_df['trackName']==song]
        freq_list = []
        for date in dates:
            if (one_song_freqs[date_column_name]==date).any():
                that_day = one_song_freqs[one_song_freqs[date_column_name]==date]
                freq_list.append(int(sum(that_day['Number of Plays'])))
            else:
                freq_list.append(0)
        dates_and_freqs_df = pd.DataFrame(data=freq_list, index=dates)
        dates_and_freqs_df.index = dates_and_freqs_df.index.to_timestamp()
        plt.plot(dates_and_freqs_df, label=song)
        plt.legend()
     
    plt.savefig('top_song_per_month_over_time.png')
    plt.show()