import functions as f

def main():
    df = f.get_listening_history('MyData/StreamingHistory0.json')
    df = f.merge_songs(df, "MONTERO (Call Me By Your Name) - SATAN'S EXTENDED VERSION",'MONTERO (Call Me By Your Name)')

    months = df['Month-Year'].unique()

    monthly_song_freqs_df = f.song_play_frequencies(df, months, 'Month-Year')

    top_songs_df = f.top_songs_per_month(df, months)

    f.print_top_songs_per_month(df, months)

    f.plot_top_songs_over_time(top_songs_df, monthly_song_freqs_df, months, 'Month-Year')

if __name__ == "__main__":
    main()