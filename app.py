# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_table
from Code.graph import anova
from Code.utils_mail import utils
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
#Fonctions pour charger les donénes
df_mail = utils.get_df_from_csv("data_clean_sample.csv",10,["Date", "From", "To","Subject"])#TODO mieux presentr le tableau
df_anova = anova.load_data(number_head=5)
df_all_data = anova.load_data()
fig = anova.box_plot(df_all_data)
anova_table = anova.anova_table(df_all_data)

#Text du site
presentation_site = '''
# Présentation du projet
Cette page présente ce que nous avons réalisé ddurant notre projet DataScience
...
'''
presentation_donnee = '''
## Présentation des donnés
Ici un extrait des données de base que nous disposions : 
'''

app.layout = html.Div(children=[
    dcc.Markdown(children=presentation_site),
    dcc.Markdown(children=presentation_donnee),
    html.Div(children=dash_table.DataTable(
        id='table_mail',
        columns=[{"name": i, "id": i} for i in df_mail.columns],
        data=df_mail.to_dict('records'),
    )),
    dcc.Markdown(children=presentation_site),
    html.Div(children=dash_table.DataTable(
        id='data_anova',
        columns=[{"name": i, "id": i} for i in df_anova.columns],
        data=df_anova.to_dict('records'),
    )),
    html.Div([
        dcc.Graph(
            id='box-plot',
            figure=fig
        ),
        dcc.RangeSlider(
            id='range-slider',
            min=0,
            max=df_all_data["theme"].count(),
            step=1,
            value=[0, df_all_data["theme"].count()],
        ),
        html.Div(id='slider-output-container')
    ]),
    html.Div(children=dash_table.DataTable(
        id='table_anova',
        columns=[{"name": i, "id": i} for i in anova_table.columns],
        data=anova_table.to_dict('records'),
    )),

])

@app.callback(
    Output('box-plot', 'figure'),
    Input('range-slider', 'value')
)

def update_graph(number):
    fig = anova.box_plot(anova.load_data(number[0], number[1]))
    return fig

if __name__ == '__main__':
    app.run_server()