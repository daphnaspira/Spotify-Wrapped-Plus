import pandas as pd
from datetime import datetime

def main():
    data = pd.read_json("./StreamingHistory0.json")
    data["date"] = [n[:10] for n in data["endTime"]]
    data["month"] = [datetime.strptime(date[:10], "%Y-%m-%d").month for date in data["endTime"]]

    # data.to_csv("data.csv")

    for month in range(1, 13):
        months_songs = data[data["month"] == month]
        freq = months_songs["trackName"].value_counts()
        top = freq.keys()[0]
        print(top)
        print(freq.head())

    # for day in pd.date_range(start=params["start"],end=params["end"])


if __name__ == "__main__":
    main()