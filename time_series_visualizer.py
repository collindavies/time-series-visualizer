import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data
df_raw = pd.read_csv('fcc-forum-pageviews.csv', parse_dates = ['date'])

# Clean data
df = df_raw[(df_raw.value < df_raw.value.quantile(0.975)) & (df_raw.value > df_raw.value.quantile(0.025))]
df.index = pd.to_datetime(df.index)

def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(20,6))
    plt.plot(df.index, df['value'], 'r')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar = df.groupby(df.date.dt.strftime('%Y-%m')).value.agg(['mean'])
    df_bar.index = pd.to_datetime(df_bar.index)
    df_bar['month'] = df_bar.index.month
    df_bar['year'] = df_bar.index.year
    
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        
    df_bar['month'] = df_bar['month'].apply(lambda data: months[data-1])
    df_bar['month'] = pd.Categorical(df_bar['month'], categories = months)
    df_pivot = pd.pivot_table(df_bar, values = "mean", index = "year", columns = "month")
    
    # Draw bar plot
    ax = df_pivot.plot(kind = 'bar')
    fig = ax.get_figure()
    fig.set_size_inches(10, 8)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views') 

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(ncols = 2)
    fig.set_size_inches(15, 6)
    sns.boxplot(x="year", y="value", data=df_box, ax=axs[0]).set(title="Year-wise Box Plot (Trend)", xlabel="Year", ylabel="Page Views")
    sns.boxplot(x="month", y="value", data=df_box, order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ax=axs[1]).set(title="Month-wise Box Plot (Seasonality)", xlabel="Month", ylabel="Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
