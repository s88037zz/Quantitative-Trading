import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook


def main():
    # load dataset
    data_path = os.path.join("..", "data", "S&P500.csv")
    print("data path is %s" % data_path)
    df = pd.read_csv(data_path)
    print(df.head())

    # set plt variable
    months = mdates.MonthLocator()
    years = mdates.YearLocator()
    years_fmt = mdates.DateFormatter("%Y")


    plt.figure(figsize=(15, 9), dpi=200)
    def show_open_price(df):
        fig, ax = plt.subplots()
        ax.plot("Date", "Open", data=df)
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.xaxis.set_minor_locator(months)

    show_open_price(df)


if __name__ == '__main__':
    main()
