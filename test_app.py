import re
import base64
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, Input, Output, dcc, html, State
from numpy import full
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
li = {'admin': ['admin', 'teacher'],
      'student': ['student']}

darker = "#242F9B"
dark = "#646FD4"
white = "#E8F9FD"
lighter = "#ea6c36"
light = "#DBDFFD"
file = "data/dbs/data_merged_cet.feather"
red = "#C85C5C"
orange = "#F9975D"
yellow = "#FBD148"
green = "#B2EA70"

app = Dash("EduFit", external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

def load_dataframe(file):
    df = pd.read_feather(file)
    

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
            dbc.CardBody(html.I(className="fa-solid fa-person", style={"font-size": "40px", "color": "white"}), className=""), width={"size": 2}, align="top"
        ),
        dbc.Col(
            dbc.CardBody([html.H4(children="Student Studentov", id="subname", className="card-header", style={"color": "white", "font-size": "20px"}),
                          html.Ul([
                              html.Li(children="Class: Student's class"),
                              html.Li(children="Age: Student's age"),
                              html.Li(children="Gender: Student's gender"),
                          ], className="card-text", style={"color": "white", "font-size": "20px"})]))], justify="right")],
    color=dark, style={"border-radius": "25px"}
)

login = dbc.Container([
    dbc.Row([dbc.Col(html.H1("EduFit: Student fitness tracker", className=""), xs={"size": 12}, sm={"size": 12}, md={"size": 8}, width={"size": 6})],
            style={'margin-top': '100px', "font-size": "30px", "text-align": "center", "color": darker}, justify="center"),
    dbc.Row([dbc.Col(html.Div(html.Img(src="/static/images/logo.png")))],
            style={'textAlign': 'center'}, justify="center"),
    dbc.Row([dbc.Col(
        dbc.Input(id="user", type="text", placeholder="Enter Username",
            class_name="alert-primary"), xs={"size": 10}, sm={"size": 8}, md={"size": 5}, width={
            "size": 5}, style={'padding': '10px', 'margin-top': '30px',
                               'font-size': '16px', 'border-width': '3px', "color":dark})], justify="center"),
    dbc.Row([dbc.Col(
            dbc.Input(id="passw", type="password", placeholder="Enter Password", className="alert-primary mt-3", valid=False, invalid=False),  xs={"size": 10}, sm={"size": 8}, md={"size": 5}, width={
                "size": 5}, style={'padding': '10px',
                                   'font-size': '16px', 'border-width': '3px', "color":dark})], justify="center"),
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
                dbc.NavLink(children=["Log out ", html.I(className="bi bi-box-arrow-right ml-2")], href="/", active=True)], brand="EduFit", dark=True, color=dark, style={"color": "white", "font-size": "20px", "border-radius": "25px"}, class_name="mt-3", expand="sm", fluid=True), width={"size": 12})
    ], justify="center"),
    html.Div(id="admin"),
    # dbc.Row([
    # dbc.Col(html.H3("Choose class(es)",
    # className="mt-3 mb-3", style={"font-size": "20px", "color":darker}), xs={"size": 5}, sm={"size": 4}, md={"size": 2}, width={
    # "size": 2}, align="center", className="text-center mr-0"),
    # dbc.Col(dcc.Dropdown(id="cls-dpdn", value="",
    # options=["1", "2", "3", "4", "5", "6"]), xs={"size": 7}, sm={"size": 5}, md={"size": 3}, width={"size": 3}, className="mt-3 mb-3"),
    # dbc.Col(html.H3("Choose student(s)",
    # className="mt-3 mb-3 ", style={"font-size": "20px", "color":darker}), xs={"size": 5}, sm={"size": 4}, md={"size": 2}, width={
    # "size": 2}, align="center", className="text-center mr-0"),
    # dbc.Col(dcc.Dropdown(id="cls-dpdn", value="", options=["1", "2", "3", "4", "5", "6"]), xs={"size": 7}, sm={"size": 5}, md={"size": 3}, width={"size": 3}, className="mt-3 mb-3")], justify="center"),
    dbc.Col(html.Hr(style={'borderWidth': "0.3vh", "width": "100%",
            "backgroundColor": "#B4E1FF", "opacity": "1"}), width={'size': 10, 'offset': 1}),
    html.Div([
        dbc.Row([
            dbc.Col(info_card, xs={"size": 12}, sm={"size": 12}, md={"size": 4}, width={"size": 4}, className="m-3", align="center"),
            dbc.Col([
                html.I(className="fa-solid fa-person-walking", style={
                       "font-size": "30px", "color": darker, 'margin-bottom': 25, 'margin-right': 30, 'margin-top': 30, 'margin-left': 20}),
                html.I(className="fa-solid fa-bed", style={
                       "font-size": "30px", "color": darker, 'margin-bottom': 25, 'margin-right': 30, 'margin-left': 10}),
                html.I(className="fa-solid fa-heart-circle-check", style={
                       "font-size": "30px", "color": darker, 'margin-bottom': 30, 'margin-right': 30, 'margin-left': 10})
            ], xs={"size": 3}, sm={"size": 1}, md={"size": 1}, width={"size": 1}, align="center"),
            dbc.Col([
                # dcc.RadioItems(id="freqvaltype", value="Denní průměr", options=[
                #     "Týdenní průměr", "Denní průměr", "Hodinový průměr"], labelClassName="m-1", inputClassName="m-1", inline=True),
                # html.Div(children="", id="bars")], width={"size": 5}, className="text-center", align="center")
                #  dbc.Col([
                #     dcc.RadioItems(id="valbar", value="%", options=[{'label': 'Procenta', 'value': '%'},
                #                                                     {'label': 'Hodnoty', 'value': 'num'}], inputClassName="m-1", className="mt-4 mb-2", inline=False)
                dbc.Progress(
                    value=40, color=red, striped=True, label="4000/10000", className="mb-3", id="step", style={"height": "40px", "font-size": "20px", "border-radius": "25px", 'margin-top': 20}),
                dbc.Progress(
                    value=94, color=green, striped=True, label=f"9h/10h", className="mb-3", style={"height": "40px", "font-size": "20px", "border-radius": "25px"}),
                dbc.Progress(
                    value=65, color=yellow, striped=True, label="Zvýšený", className="mb-3", style={"height": "40px", "font-size": "20px", "border-radius": "25px"}
                )], xs={"size": 9}, sm={"size": 6}, width={"size": 6}, className="text-center", align="center"),
            dbc.Col(html.Hr(style={'borderWidth': "0.3vh", "width": "100%",
                    "backgroundColor": "#B4E1FF", "opacity": "1"}), width={'size': 10}),
            # ], width={"size": 1}, align="center")
        ], justify="center"),
        dbc.Row([
            dbc.Col(html.H3("Fitness doporučení: ", className="text-center m-4"), align="center", style={"color": dark}, xs={"size": 8}, sm={"size": 6}, md={"size": 3}, width={"size": 3}),
            dbc.Col(dbc.Alert("Velmi nízký denní průměr kroků", color=red, className="mt-4 mb-4"), align="center", style={"color": "white"}, xs={"size": 8}, sm={"size": 5}, md={"size": 4}, width={"size": 4}),
            dbc.Col(dbc.Alert("Mírně podprůměrná délka spánku", color=yellow, className="mt-4 mb-4"), align="center", style={"color": "white", "border-radius": "25px"}, xs={"size": 8}, sm={"size": 5}, md={"size": 4}, width={"size": 4}),
            dbc.Col(html.Hr(style={'borderWidth': "0.3vh", "width": "100%", "backgroundColor": "#B4E1FF", "opacity": "1", "margin-bottom":30}), width={'size': 10}),
        ], justify="center"),
    ]),
    html.Div([
        dbc.Row([dbc.Col(html.H1(" "))]),
        dbc.Row([dbc.Col(html.H1(" "))]),
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
                }, className="border border-dark"), className="m-2", width={"size": 4}, xs={"size": 10}, sm={"size": 8}, md={"size": 5}
            ),
            dbc.Col(
                dcc.Graph(id="sleepgraph", figure={}, className="border border-dark"), className="m-2", width={"size": 4}, xs={"size": 10}, sm={"size": 8}, md={"size": 5}
            ),
            dbc.Col(
                dcc.Graph(id="rategraph", figure={}, className="border border-dark"), className="m-2", width={"size": 4}, xs={"size": 10}, sm={"size": 8}, md={"size": 5}
            )

        ], className="g-0", justify="evenly")
    ], style={"background":dark, "border-radius": "25px", "margin-top":10})
], fluid=True)


@ app.callback(
    [Output('verify', 'color'), Output('url', 'pathname'),
     Output('verify', 'children'), Output('passw', 'valid'), Output('passw', 'invalid')],
    [Input('verify', 'n_clicks')],
    [State('user', 'value'),
     State('passw', 'value')], prevent_initial_call=True)
def update_output(n_clicks, uname, passw):
    # if uname == '' or uname == None and passw == '' or passw == None:
    #     return "primary", dash.no_update, dash.no_update, dash.no_update, dash.no_update
    if n_clicks>0:
        if uname not in li:
            return "warning", dash.no_update, "Not a user", dash.no_update, dash.no_update
        if li[uname][0] == passw:
            return "success", '/dashboard%'+base64.b64encode(uname.encode("utf-8")).decode("utf-8"), "Success!", True, False
        if uname in li.keys() and passw != li[uname][0]:
            return "danger", dash.no_update, "Wrong credentials", False, True
    else:
        return "primary", dash.no_update, "Log In", dash.no_update, dash.no_update


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
               [dash.dependencies.Input('url', 'pathname'), ])
def display_page(pathname):
    if re.findall("\A/dashboard", pathname) == ["/dashboard"]:
        if len(re.split("%",pathname)[1]) % 4 == 0:
            return index
        else:
            return login
    else:
        return login


@ app.callback(Output(component_id="subname", component_property="children"),
               [dash.dependencies.Input('url', 'pathname'), ])
def set_name(pathname):
    if re.findall("\A/dashboard", pathname) == ["/dashboard"]:
        return base64.b64decode(re.split("%", pathname)[1]).decode("utf-8")
    else:
        return None


@ app.callback(
    Output(component_id="admin", component_property="children"),
    Input(component_id="subname", component_property="children"),
)
def update_output_row(input_children):
    if not li.__contains__(input_children):
        return None
    if li[input_children].__contains__("teacher"):
        return generate_dropdown()
    else:
        return None
    

def generate_dropdown():
    return dbc.Row([
        dbc.Col(html.H3("Choose class(es)",
                        className="mt-3 mb-3", style={"font-size": "20px", "color": darker}), xs={"size": 5}, sm={"size": 4}, md={"size": 2}, width={
                "size": 2}, align="center", className="text-center mr-0"),
        dbc.Col(dcc.Dropdown(id="cls-dpdn", value="",
                             options=["1", "2", "3", "4", "5", "6"]), xs={"size": 7}, sm={"size": 5}, md={"size": 3}, width={"size": 3}, className="mt-3 mb-3"),
        dbc.Col(html.H3("Choose student(s)",
                        className="mt-3 mb-3 ", style={"font-size": "20px", "color": darker}), xs={"size": 5}, sm={"size": 4}, md={"size": 2}, width={
                "size": 2}, align="center", className="text-center mr-0"),
        dbc.Col(dcc.Dropdown(id="cls-dpdn", value="", options=["1", "2", "3", "4", "5", "6"]), xs={"size": 7}, sm={"size": 5}, md={"size": 3}, width={"size": 3}, className="mt-3 mb-3")], justify="center"),


if __name__ == "__main__":
    app.run_server(debug=True)
