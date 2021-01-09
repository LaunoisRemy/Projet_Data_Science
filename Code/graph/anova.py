# lien de cet exemple anova : https://www.reneshbedre.com/blog/anova.html
import json
import os

import pandas as pd
import plotly.express as px


def load_data(number_start=0, number_head=None):
    # load data file
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(ROOT + "/../Generated Data/dataForAnova5.json") as f:
        data = json.load(f)
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))
        df = pd.melt(df, value_vars=list(df.columns), var_name='theme', value_name='time')

    df = df[df['time'].notna()]
    i = 0
    for index, row in df.iterrows():
        i += 1
        df.at[index, 'time'] = row["time"] / 86400
        if i > 1000:
            break
    time_filter = df['time'] < 182.5
    df = df[time_filter]
    df = df[df['theme'].map(df['theme'].value_counts()) > 2]

    if number_head is not None:
        df = df[number_start:number_head]

    return df


def box_plot(df, n=None):
    if n != None:
        df = df.head(n=10)
    return px.box(df, x='theme', y='time')


def anova_table(df):
    model = ols('time ~ C(theme)', data=df).fit()
    return sm.stats.anova_lm(model, typ=2)


import statsmodels.api as sm
from statsmodels.formula.api import ols
