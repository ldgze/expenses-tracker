"""
1. draw a bar chart with the dataframe
2. draw a pie chart with the dataframe
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def draw_bar_chart(df):
    df['Year_month'] = pd.to_datetime(df['Date']).dt.to_period('M')
    df = df[["Year_month", "Amount", "Category"]].groupby(
        by="Year_month").sum().reset_index()
    print("Total expenses by month:\n")
    print(df)
    plt.figure(figsize=(8, 6))
    plt.bar(df.index, df.Amount, 0.4)
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.title("Total expenses by month")
    plt.xticks(df.index, df.Year_month)
    plt.show()
    plt.tight_layout()


def draw_pie_chart(df):
    df = df[["Category", "Amount"]].groupby(by="Category").sum().reset_index()
    print("Total expenses by category:\n")
    print(df)
    cmap = plt.get_cmap("tab20c")
    plt.figure(figsize=(8, 8))
    plt.pie(df.Amount, explode=(0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1),
            colors=cmap(np.arange(8)),
            labels=df.Category, autopct="%.2f%%", pctdistance=0.88,
            shadow=True)
    plt.title('Expenses proportion by category')
    plt.show()
    plt.tight_layout()
