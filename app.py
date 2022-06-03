# pip install dash (version 2.0.0 or higher)
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px  # (version 4.7.0 or higher)
import pandas as pd
import dash_bootstrap_components as dbc
import dash
import pandas_datareader.data as web
import datetime

df = pd.read_csv("stonks.csv")
print(df[:15])

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Stock market dashboard"),
                className='text-center text-primary mb-4',
                width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id="my-dpdn", multi=False, value='AMZN', options=[
                         {'label': x, 'value': x} for x in sorted(df['Symbols'].unique())]),
            dcc.Graph(id='line-fig', figure={})
        ], xs=12, sm=12, md=12, lg=5, xl=5),
        dbc.Col([
            dcc.Dropdown(id="my-dpdn2", multi=True, value=["PFE", "BNTX"], options=[
                         {'label': x, 'value': x} for x in sorted(df['Symbols'].unique())]),
            dcc.Graph(id='line-fig2', figure={})
        ],  # width={"size": 5, 'order': 1},
            xs=12, sm=12, md=12, lg=5, xl=5)
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            html.P("Select company stock:", style={
                   "textDecoration": "underline"}),
            dcc.Checklist(id="my-checklist", value=["FB", "AMZN", "GOOGL"], options=[
                {'label': x, 'value': x} for x in sorted(df['Symbols'].unique())], labelClassName='mr-3 text-success'),
            dcc.Graph(id='my-hist', figure={})
        ],  # width={"size": 5, 'offset': 1},
            xs=12, sm=12, md=12, lg=5, xl=5),
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody(
                        html.P(
                            "We're better together. Help each other out!",
                            className="card-text")
                    ),
                    dbc.CardImg(
                        src="https://media.giphy.com/media/Ll0jnPa6IS8eI/giphy.gif",
                        bottom=True),
                ],
                style={"width": "24rem"},
            )
        ],  # width={'size':5, 'offset':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        )
    ], justify="center", align="center")  # Vertical: start, center, end

], fluid=True)


@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'] == stock_slctd]
    figln = px.line(dff, x='Date', y='High')
    return figln


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='Date', y='Open', color='Symbols')
    return figln2


# Histogram
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date'] == '2021-12-01']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    return fighist


if __name__ == "__main__":
    app.run_server(debug=True)
