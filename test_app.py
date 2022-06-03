import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, Input, Output, dcc, html, State
from numpy import full
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
li = {'admin': ['admin', 'teacher']}

app = Dash("EduFit", external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# def generate_progress(steps, sleep, rate, frequency):
#     rec_steps = 10000
#     step_percent = 0
#     rec_sleep = 8
#     sleep_percent = 0
#     if steps <= rec_steps:
#         steps = int((steps/rec_steps)*100)
#         step_percent = steps
#     elif steps > rec_steps:
#         step_percent = int((steps/rec_steps)*100)
#         steps = 100
#     if sleep <= rec_sleep:
#         sleep = int((sleep/rec_sleep)*100)
#         sleep_percent = sleep
#     elif sleep > rec_sleep:
#         sleep_percent = int((sleep/rec_sleep)*100)
#         sleep = 100

#     return [
#         dbc.Progress(
#             value=steps, label=f"{step_percent} % doporučené {frequency} hodnoty", className="mt-1 mb-3", style={"height": "30px", "font-size": "20px"}),
#         dbc.Progress(
#             value=sleep, label=f"{sleep_percent} % doporučené {frequency} hodnoty", className="mt-3 mb-3", style={"height": "30px", "font-size": "20px"}),
#         dbc.Progress(
#             value=rate, label="Normální", className="mt-3 mb-3", style={"height": "30px", "font-size": "20px"},
#             color="success")
#     ]


def generate_values(steps, sleep, rate, freq):
    return [
        html.H4(f"{steps} kroků (doporučeno: 10 000)", style={
                "height": "30px", "font-size": "25px"}, className="mt-1 mb-3"),
        html.H4(f"{sleep} hodin (doporučeno: 8 h)", style={
                "height": "30px", "font-size": "25px"}, className="mt-3 mb-3"),
        html.H4(f"{rate} tepů/min (normál 60-70)",
                style={"height": "30px", "font-size": "25px"}, className="mt-3 mb-3")
    ]


def generate_card(name, age, classname, sex):
    return None


info_card = dbc.Card([
    dbc.Row([
        dbc.Col(
            dbc.CardBody(html.I(className="bi bi-person-square card-text", style={"font-size": "80px"}), className=""), width={"size": 3}, align="center"
        ),
        dbc.Col(
            dbc.CardBody([html.H4(children="Student Studentov", id="subname", className="card-title"),
                          html.Ul([
                              html.Li(children="Class: Student's class"),
                              html.Li(children="Age: Student's age")
                          ], className="card-text")]), width={"size": 7})], justify="center")],
    color="dark", outline=True
)

login = dbc.Container([
    dbc.Row([dbc.Col(html.H1("EduFit: Student fitness tracker", className="text-primary"), xs={"size": 12}, sm={"size": 12}, md={"size": 8}, width={"size": 6})],
            style={'margin-top': '100px', "font-size": "30px", "text-align": "center"}, justify="center"),
    dbc.Row([dbc.Col(html.I(className="bi bi-person-circle text-primary"), xs={"size": 6}, sm={"size": 4}, md={"size": 2}, width={
            "size": 1}, className="text-center", style={'margin-top': '10px', "font-size": "100px"})], justify="center"),
    dbc.Row([dbc.Col(
        dbc.Input(id="user", type="text", placeholder="Enter Username",
            class_name="alert-primary"), xs={"size": 10}, sm={"size": 8}, md={"size": 5}, width={
            "size": 5}, style={'padding': '10px', 'margin-top': '30px',
                               'font-size': '16px', 'border-width': '3px'})], justify="center"),
    dbc.Row([dbc.Col(
            dbc.Input(id="passw", type="password", placeholder="Enter Password", className="alert-primary mt-3", valid=False, invalid=False),  xs={"size": 10}, sm={"size": 8}, md={"size": 5}, width={
                "size": 5}, style={'padding': '10px',
                                   'font-size': '16px', 'border-width': '3px'})], justify="center"),
    dbc.Row([
        dbc.Col([
            dbc.Button(children="Log in", color="primary", id='verify', href='',
                       n_clicks=0)], xs={"size": 8}, sm={"size": 6}, md={"size": 3}, width={
                "size": 4}, className="text-center mt-3")
    ], justify="center"),
])

index = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.NavbarSimple(children=[
                dbc.NavLink(children=["Log out ", html.I(className="bi bi-box-arrow-right ml-2")], href="/", active=True)], brand="EduFit", dark=True, color="primary", style={"color": "white", "font-size": "20px", "border-radius": "5px"}, class_name="mt-3", expand="sm", fluid=True), width={"size": 12})
    ], justify="center"),
    dbc.Row([
            dbc.Col(html.H3("Choose class(es)",
                    className="text-primary mt-3 mb-3", style={"font-size": "20px"}), xs={"size": 5}, sm={"size": 4}, md={"size": 2}, width={
                "size": 2}, align="center", className="text-center mr-0"),
            dbc.Col(dcc.Dropdown(id="cls-dpdn", value="",
                    options=["1", "2", "3", "4", "5", "6"]), xs={"size": 7}, sm={"size": 5}, md={"size": 3}, width={"size": 3}, className="mt-3 mb-3"),
            dbc.Col(html.H3("Choose student(s)",
                    className="text-primary mt-3 mb-3 ", style={"font-size": "20px"}), xs={"size": 5}, sm={"size": 4}, md={"size": 2}, width={
                "size": 2}, align="center", className="text-center mr-0"),
            dbc.Col(dcc.Dropdown(id="cls-dpdn", value="", options=["1", "2", "3", "4", "5", "6"]), xs={"size": 7}, sm={"size": 5}, md={"size": 3}, width={"size": 3}, className="mt-3 mb-3")], justify="center"),
    html.Div([
        dbc.Row([
            dbc.Col(info_card, xs={"size": 12}, sm={"size": 8}, md={"size": 4}, width={"size": 4},
                    className="m-3", align="center"),
            dbc.Col([
                html.H3("Kroky",
                    className="text-primary mt-4 mb-4", style={"font-size": "20px"}),
                html.H3("Spánek",
                    className="text-primary mb-4", style={"font-size": "20px"}),
                html.H3("Tep",
                    className="text-primary mb-4", style={"font-size": "20px"})
            ], xs={"size": 2}, sm={"size": 1}, md={"size": 1}, width={"size": 1}, align="center"),
            dbc.Col([
                # dcc.RadioItems(id="freqvaltype", value="Denní průměr", options=[
                #     "Týdenní průměr", "Denní průměr", "Hodinový průměr"], labelClassName="m-1", inputClassName="m-1", inline=True),
                # html.Div(children="", id="bars")], width={"size": 5}, className="text-center", align="center")
                #  dbc.Col([
                #     dcc.RadioItems(id="valbar", value="%", options=[{'label': 'Procenta', 'value': '%'},
                #                                                     {'label': 'Hodnoty', 'value': 'num'}], inputClassName="m-1", className="mt-4 mb-2", inline=False)
                dbc.Progress(
                    value=79, label="79 % doporučené denní hodnoty", className="mt-3 mb-3", style={"height": "30px", "font-size": "20px"}),
                dbc.Progress(
                    value=94, label=f"94 % doporučené denní hodnoty", className="mt-3 mb-3", style={"height": "30px", "font-size": "20px"}),
                dbc.Progress(
                    value=65, label="Normální", className="mt-3 mb-3", style={"height": "30px", "font-size": "20px"},
                    color="success")], xs={"size": 10}, sm={"size": 6}, width={"size": 6}, className="text-center", align="center")

            # ], width={"size": 1}, align="center")
        ], justify="center"),
        dbc.Row([
            dbc.Col(
                html.H3("Fitness doporučení: ", className="text-primary text-center m-4"), width={"size": 3}, align="center"
            ),
            dbc.Col(
                dbc.Alert("Doporučení 1", color="success", className="mt-4 mb-4"), align="center", width={"size": 4}
            ),
            dbc.Col(
                dbc.Alert("Doporučení 2", color="primary", className="mt-4 mb-4"), align="center", width={"size": 4}
            )
        ], justify="start"),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id="stepgraph", figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5],
                         'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'title': 'Dash Data Visualization'
                    }
                }, className="border border-dark"), className="m-2", width={"size": 4}
            ),
            dbc.Col(
                dcc.Graph(id="sleepgraph", figure={}, className="border border-dark"), className="m-2", width={"size": 4}
            ),
            dbc.Col(
                dcc.Graph(id="rategraph", figure={}, className="border border-dark"), className="m-2", width={"size": 4}
            )

        ], className="g-0", justify="evenly")
    ], style={"background": "gainsboro", "border-radius": "5px"})
], fluid=True)


@ app.callback(
    [Output('verify', 'color'), Output('verify', 'href'),
     Output('verify', 'children'), Output('passw', 'valid'), Output('passw', 'invalid')],
    [Input('verify', 'n_clicks')],
    [State('user', 'value'),
     State('passw', 'value')], prevent_initial_call=True)
def update_output(n_clicks, uname, passw):
    # if uname == '' or uname == None and passw == '' or passw == None:
    #     return "primary", dash.no_update, dash.no_update, dash.no_update, dash.no_update
    if uname not in li:
        return "warning", dash.no_update, "Not a user", dash.no_update, dash.no_update
    if li[uname][0] == passw:
        return "success", '/dashboard', "Success!", True, False
    if uname in li.keys() and passw != li[uname][0]:
        return "danger", dash.no_update, "Wrong credentials", False, True


# @ app.callback([Output('bars', 'children')], [Input('freqvaltype', 'value'), Input('valbar', 'value')])
# def update_bars(freqvaltype, valbar):
#     freq = ""
#     if freqvaltype == "Denní průměr":
#         freq = "denní"
#     if freqvaltype == "Týdenní průměr":
#         freq = "týdenní"
#     if freqvaltype == "Hodinový průměr":
#         freq = "hodinové"

#     if valbar == "%":
#         content = generate_progress(10000, 9, 65, freq)
#     elif valbar == "num":
#         content = generate_values(10000, 9, 65, freq)
#     return [content]


@ app.callback(dash.dependencies.Output('page-content', 'children'),
               [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboard':
        return index
    else:
        return login


if __name__ == "__main__":
    app.run_server(debug=True)
