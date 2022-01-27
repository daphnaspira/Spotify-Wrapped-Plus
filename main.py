import functions as f

def main():
    df = f.get_listening_history('MyData/StreamingHistory0.json')
    df = f.merge_songs(df, "MONTERO (Call Me By Your Name) - SATAN'S EXTENDED VERSION",'MONTERO (Call Me By Your Name)')

    months = df['Month-Year'].unique()

    monthly_song_freqs_df = f.play_frequencies(df, months, 'Month-Year', 'song')
    monthly_artist_freqs_df = f.play_frequencies(df, months, 'Month-Year', 'artist')

    top_songs_df = f.top_per_month(df, months, 'song')
    top_artists_df = f.top_per_month(df, months, 'artist')

    f.print_top_per_month(df, months, 'song')
    f.print_top_per_month(df, months, 'artist')    

    f.plot_top_over_time(top_songs_df, monthly_song_freqs_df, months, 'Month-Year', 'song')
    f.plot_top_over_time(top_artists_df, monthly_artist_freqs_df, months, 'Month-Year', 'artist')

if __name__ == "__main__":
    main()