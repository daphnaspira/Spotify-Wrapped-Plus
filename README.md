# Spotify-Wrapped-Plus

## Setting up:
Call the `get_listening_history()` function to load in your Spotify history as a Pandas dataframe.

### Optional: song name merging
In some cases, you might listen to two versions of the same song that have slightly varied names. The variation in name means that the songs will be counted separately.The `merge_songs()` function will take in the two different song names and rename them all as the second name that you input so that their play counts are counted together.

## Functions:
**All functions can be used to access information about songs or artists.** The `song_or_artist` parameter in each function determines which dataset will be evaluated.

### To find out how many times you listened to each song/artist in a given time period
`play_frequencies()` returns a dataframe containing each song or artist and the number of times it was played in the given time period (day or month).
Requires that the range of periods in your listening history exist as a list/array to pass into the function.

Example for finding song frequency each month:
```
months = df['Month-Year'].unique()
monthly_song_freqs_df = play_frequencies(df, months, 'Month-Year', 'song')
```

### To see (printed out) your top songs/artists each month
`print_top_per_month()` prints out each month in your history and the top n songs or artists (default 5) played during that month with the number of plays for each one.
Requires that the range of months in your listening history exist as a list/array to pass into the function (same as for play_frequencies())

### To get a dataframe with your top songs/artists each month
`top_per_month()` returns a dataframe containing your top n song or artist names, number of plays, and month.
Requires that the range of months in your listening history exist as a list/array to pass into the function (same as for play_frequencies())

### To get a plot showing the play frequency over time for each song/artist that was your top played in at least one time period
`plot_top_over_time()` returns an overlaid line plot with one line for each song or artist over the time period range that you specify. x-axis is the time period and y-axis is number of times that song or artist was played in the time period
