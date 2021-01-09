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
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
import pandas as pd

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

# Fonctions pour charger les donénes
df_mail = utils.get_df_from_csv("data_clean_sample.csv", 10,
                                ["Date", "From", "To", "Subject"])  # TODO mieux presentr le tableau
df_anova = anova.load_data(number_head=10)
df_all_data = anova.load_data()
fig = anova.box_plot(df_all_data)
anova_result = anova.anova_table(df_all_data)

# Text du site
presentation_site = '''
# Présentation du projet





'''
table_mail = dbc.Table.from_dataframe(df_mail, striped=True, bordered=True, hover=True)

presentation_donnee = dbc.Jumbotron([
    html.H1("Présentation des données"),
    html.P("Ici un extrait des données de base dont nous disposions :"),
    html.P(""),
    table_mail,

])
apres_traitement = dbc.Container([
    html.P(""),
    html.P("Après avoir traité et mis en forme les données pour répondre à notre problématique, nous avons"
           " obtenu des données sous cette forme :"),
    html.P(""),
    html.P("Chaque thème correspond à une conversation et à un temps moyen de réponse pour cette conversation")
])

jumbotron_presentation = dbc.Jumbotron(
    [
        html.H1("Présentation du projet", className="display-3"),
        html.P(
            "Sujet 1.2 : analyse de la dynamique des échanges entre les différentes personnes ",
            className="lead",
        ),
        html.P(

            "A partir du sujet que nous avons choisi, notre objectif était de réussir à déterminer "
            "si le thème abordé dans le contenu d’un mail avait une influence sur le temps de réponse du destinataire. "
            ,
        ),
        html.Hr(className="my-2"),
        html.P(
            "Nous avons donc déterminé la problématique suivante :"

        ),
        html.P(
            "En analysant les caractéristiques principales d'un mail et de la personne qui le reçoit, peut on estimer "
            "le temps de réponse par rapport à la thématique abordée ?",
            className="alert-link",
        ),

        html.P(dbc.Button("Visualiser les données", color="primary", block=True), className="lead"),
    ]
)


@app.callback(Output("page-content", "children"), [dash.dependencies.Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return dbc.Container(jumbotron_presentation)
    elif pathname == "/data":
        return dbc.Container(children=[presentation_donnee, apres_traitement, table_anova])
    elif pathname == "/resultats":
        return dbc.Container(children=[dbc.Container(
            [
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
            ]

        ),

            anova_result,

        ])
        # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


table_anova = dbc.Table.from_dataframe(df_anova, striped=True, bordered=True, hover=True)
anova_result = dbc.Table.from_dataframe(anova_result, striped=True, bordered=True, hover=True)

app.layout = dbc.Container(children=[
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(

        children=[
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Voir les données", href="/data", active="exact"),
            dbc.NavLink("Résultats", href="/resultats", active="exact"),
        ],
        brand="Data-Science",
        color="dark",
        dark=True,
    ),
    html.Div(id="page-content", className="pt-4"),

]

)


@app.callback(
    Output('box-plot', 'figure'),
    Input('range-slider', 'value')
)
def update_graph(number):
    fig = anova.box_plot(anova.load_data(number[0], number[1]))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
