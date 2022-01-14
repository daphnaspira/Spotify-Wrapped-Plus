# Spotify-Wrapped-Plus

## Setting up:
Call the `get_listening_history()` function to load in your Spotify history as a Pandas dataframe.

### Optional: song name merging
In some cases, you might listen to two versions of the same song that have slightly varied names. The variation in name means that the songs will be counted separately.The `merge_songs()` function will take in the two different song names and rename them all as the second name that you input so that their play counts are counted together.

## Functions:
### To find out how many times you listened to each song in a given time period
`song_play_frequencies()` returns a dataframe containing each song, artist, and the number of times that song was played in the given time period (day or month).
Requires that the range of periods in your listening history exist as a list/array to pass into the function.

Example for finding song frequency each month:
```
months = df['Month-Year'].unique()
monthly_song_freqs_df = song_play_frequencies(df, months, 'Month-Year')
```

### To see (printed out) your top songs each month
`print_top_songs_per_month()` prints out each month in your history and the top n songs (default 5) played during that month with the number of plays for each song.
Requires that the range of months in your listening history exist as a list/array to pass into the function (same as for song_play_frequencies())

### To get a dataframe with your top songs each month
`top_songs_per_month()` returns a dataframe containing your top n song names, artists, number of songs, and month.
Requires that the range of months in your listening history exist as a list/array to pass into the function (same as for song_play_frequencies())

### To get a plot showing the play frequency each month for each song that was your top played song at least one month
`plot_top_songs_over_time()` returns an overlaid line plot with one line for each song over the time period range that you specify. x-axis is the time period and y-axis is number of times that song was played in the time period
