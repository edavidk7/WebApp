import datetime as dt
import re
import base64
from turtle import color
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Dash, Input, Output, dcc, html, State
from numpy import full
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.io import write_image
import plotly.graph_objs as go

li = {'admin': ['admin', 'teacher'],
      'student': ['student']}
kind_codes = {"Running": [98, 50, 66, 82],
              "Walking": [1, 16, 17, 33, 49, 18, 34, 65],
              "Light_Sleep": [112],
              "Heavy_Sleep": [122],
              "Sit": [80, 96, 99],
              "Standing": [96],
              "SedentaryInLast5Minutes": [90],
              "NotWorn": [3],
              "NotWorn_Charging": [6],
              "NotWorn_FaceUp": [83],
              "NotWorn_FaceDown": [115]}
darker = "#242F9B"
dark = "#646FD4"
white = "#E8F9FD"
lighter = "#ea6c36"
light = "#DBDFFD"
file1 = "data/dfs/week1.feather"
file2 = "data/dfs/week2.feather"
red = "danger"
orange = "#F9975D"
yellow = "warning"
green = "success"
alert_text = " "

app = Dash("EduFit", external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


def generate_piechart(file, _stu):
    merged_all = load_dataframe(file)
    new_kind_codes = {}
    for key in kind_codes.keys():
        arr = kind_codes[key]
        for code in arr:
            new_kind_codes[code] = key
    merged_all = merged_all[merged_all["ALIAS"] == _stu]
    merged_all["KIND"] = merged_all["RAW_KIND"].map(
        lambda x: new_kind_codes.get(x))
    sleep_df = merged_all.loc[(merged_all["KIND"] == "Heavy_Sleep") | (
        merged_all["KIND"] == "Light_Sleep")]
    sleep_df = merged_all.copy().loc[(merged_all["KIND"] == "Heavy_Sleep") | (
        merged_all["KIND"] == "Light_Sleep")]
    sleep_df["HOURLY"] = sleep_df["DATETIME_CET"].dt.time
    sleep_df_alt = sleep_df[np.logical_or(
        sleep_df["HOURLY"] >= dt.time(20, 0), sleep_df["HOURLY"] < dt.time(8, 0))]
    thing = sleep_df_alt.groupby(by="KIND").count()
    thing.reset_index(inplace=True)
    fig = px.pie(thing, names=["Hluboký spánek", "Lehký spánek"],
                 values="Weight", title="Kvalita spánku")
    return fig


def generate_average(file, stu):
    df = load_dataframe(file)
    df_person = df[df["ALIAS"] == stu]
    ys2 = []
    for weekday in df["WEEK_DAY"].unique():
        daily_entries = df_person[df_person["WEEK_DAY"] == weekday]
        total_steps = daily_entries["STEPS"].sum()
        ys2.append(total_steps)
    ys2 = sum(ys2)/7
    ys3 = []
    for weekday in df["WEEK_DAY"].unique():
        daily_entries = df_person[df_person["WEEK_DAY"] == weekday]

        def inner_func(x):
            return x < 250 and x > 30

        def inner_func2(x):
            return x in kind_codes["Walking"] or x in kind_codes["Standing"] or x in kind_codes["Sit"]
        valid_entries = daily_entries[daily_entries["HEART_RATE"].map(
            inner_func)]
        valid_entries = valid_entries[valid_entries["HEART_RATE"].map(
            inner_func2)]
        total_heart_rate = valid_entries["HEART_RATE"].sum()
        ys3.append(total_heart_rate/valid_entries["HEART_RATE"].count())
    ys3 = sum(ys3)/7
    return ys3, ys2


def daily_sleep(file, person):
    merge_all = load_dataframe(file)
    all_time = []
    light_time = []
    heavy_time = []
    merge_all["HOURLY"] = merge_all["DATETIME_CET"].dt.time
    sleep_df_alt = merge_all[np.logical_or(
        merge_all["HOURLY"] >= dt.time(20, 0), merge_all["HOURLY"] < dt.time(8, 0))]

    new_kind_codes = {}
    for key in kind_codes.keys():
        arr = kind_codes[key]
        for code in arr:
            new_kind_codes[code] = key
    # new_kind_codes
    sleep_df_alt["KIND"] = sleep_df_alt["RAW_KIND"].map(
        lambda x: new_kind_codes.get(x))
    sleep_df_alt = sleep_df_alt[np.logical_or(
        sleep_df_alt["KIND"] == "Heavy_Sleep", sleep_df_alt["KIND"] == "Light_Sleep")]
    sleep_df_alt = sleep_df_alt[sleep_df_alt["ALIAS"] == person]
    for day in sleep_df_alt["DATETIME_CET"].dt.date.unique():
        new_df = sleep_df_alt[sleep_df_alt["DATETIME_CET"].dt.date == day]
        series = new_df["KIND"]
        all_time.append(series.count())
        light_time.append(series[series == "Light_Sleep"].count())
        heavy_time.append(series[series == "Heavy_Sleep"].count())
    return all_time, light_time, heavy_time


def generate_graphs(file, stu):
    df = load_dataframe(file)
    df_person = df[df["ALIAS"] == stu]
    xs = []
    ys = []
    for weekday in df["WEEK_DAY"].unique():
        daily_entries = df_person[df_person["WEEK_DAY"] == weekday]

        def inner_func(x):
            return x < 250 and x > 30
        valid_entries = daily_entries[daily_entries["HEART_RATE"].map(
            inner_func)]
        max_heart_rate = valid_entries["HEART_RATE"].max()
        xs.append(weekday)
        ys.append(max_heart_rate)

    fig1 = px.bar(x=xs, y=ys, title="Maximální srdeční tep", text_auto=True)
    xs = []
    ys = []
    for weekday in df["WEEK_DAY"].unique():
        daily_entries = df_person[df_person["WEEK_DAY"] == weekday]
        total_steps = daily_entries["STEPS"].sum()
        xs.append(weekday)
        ys.append(total_steps)

    fig2 = px.bar(x=xs, y=ys, title="Denní kroky")
    xs = []
    ys = []

    for weekday in df["WEEK_DAY"].unique():
        daily_entries = df_person[df_person["WEEK_DAY"] == weekday]

        def inner_func(x):
            return x < 250 and x > 30

        def inner_func2(x):
            return x in kind_codes["Walking"] or x in kind_codes["Standing"] or x in kind_codes["Sit"]
        valid_entries = daily_entries[daily_entries["HEART_RATE"].map(
            inner_func)]
        valid_entries = valid_entries[valid_entries["HEART_RATE"].map(
            inner_func2)]
        total_heart_rate = valid_entries["HEART_RATE"].sum()
        xs.append(weekday)
        ys.append(int(total_heart_rate/valid_entries["HEART_RATE"].count()))

    fig3 = px.bar(x=xs, y=ys, title="Průměrný srdeční tep", text_auto=True)

    return fig1, fig2, fig3


def load_dataframe(file):
    df = pd.read_feather(file)
    return df


def generate_dropdown(file):
    df = load_dataframe(file)
    names = df["ALIAS"].unique()
    return dbc.Row([
        dbc.Col(html.H3("Výběr třídy",
                        className="mt-3 mb-3", style={"font-size": "20px", "color": darker}), xs={"size": 5}, sm={"size": 4}, md={"size": 2}, width={
                "size": 2}, align="center", className="text-center mr-0"),
        dbc.Col(dcc.Dropdown(id="cls-dpdn", value="3.B",
                             options=["3.B"]), xs={"size": 7}, sm={"size": 5}, md={"size": 2}, width={"size": 2}, className="mt-3 mb-3"),
        dbc.Col(html.H3("Výběr týdne",
                        className="mt-3 mb-3", style={"font-size": "20px", "color": darker}), xs={"size": 5}, sm={"size": 4}, md={"size": 2}, width={
                "size": 2}, align="center", className="text-center mr-0"),
        dbc.Col(dcc.Dropdown(id="wk-dpdn", value="Prezenční",
                             options=["Distanční", "Prezenční"]), xs={"size": 7}, sm={"size": 5}, md={"size": 2}, width={"size": 2}, className="mt-3 mb-3"),
        dbc.Col(html.H3("Výběr studenta",
                        className="mt-3 mb-3 ", style={"font-size": "20px", "color": darker}), xs={"size": 5}, sm={"size": 4}, md={"size": 2}, width={
                "size": 2}, align="center", className="text-center mr-0"),
       
        dbc.Col(dcc.Dropdown(id="st-dpdn", options=names, value="Band 20",), xs={"size": 7}, sm={"size": 5}, md={"size": 2}, width={"size": 2}, className="mt-3 mb-3")], justify="center"),

def generate_alerts(alert1,color1):
    return  dbc.Alert(alert1,color=color1, class_name="mt-4 mb-4")
    

info_card = dbc.Card([
    dbc.Row([
        dbc.Col(
            dbc.CardBody(html.I(className="fa-solid fa-person", style={"font-size": "40px", "color": "white"}), className=""), width={"size": 2}, align="top"
        ),
        dbc.Col(
            dbc.CardBody([html.H4(children="Student Studentov", id="subname", className="card-header", style={"color": "white", "font-size": "20px"}),
                          html.Ul([
                              html.Li(children="Class: Student's class",
                                      id="stuclass"),
                              html.Li(children="Age: Student's age",
                                      id="stuage"),
                              html.Li(
                                  children="Gender: Student's gender", id="stusex"),
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
                               'font-size': '16px', 'border-width': '3px', "color": dark})], justify="center"),
    dbc.Row([dbc.Col(
            dbc.Input(id="passw", type="password", placeholder="Enter Password", className="alert-primary mt-3", valid=False, invalid=False),  xs={"size": 10}, sm={"size": 8}, md={"size": 5}, width={
                "size": 5}, style={'padding': '10px',
                                   'font-size': '16px', 'border-width': '3px', "color": dark})], justify="center"),
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
                dbc.NavLink(children=["Odhlásit se ", html.I(className="bi bi-box-arrow-right ml-2")], href="/", active=True)], brand="EduFit", dark=True, color=dark, style={"color": "white", "font-size": "20px", "border-radius": "25px"}, class_name="mt-3", expand="sm", fluid=True), width={"size": 12})
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
            dbc.Col(info_card, xs={"size": 12}, sm={"size": 12}, md={
                    "size": 4}, width={"size": 4}, className="m-3", align="center"),
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
                    value=10, color=red, striped=True, label=" ", className="mb-3", id="steps", style={"height": "40px", "font-size": "20px", "border-radius": "25px", 'margin-top': 20}),
                dbc.Progress(
                    value=10, color=red, striped=True, label=" ", className="mb-3", id="sleep", style={"height": "40px", "font-size": "20px", "border-radius": "25px"}),
                dbc.Progress(
                    value=10, color=red, striped=True, label=" ", className="mb-3", id="heartrate", style={"height": "40px", "font-size": "20px", "border-radius": "25px"}
                )], xs={"size": 9}, sm={"size": 6}, width={"size": 6}, className="text-center", align="center"),
            dbc.Col(html.Hr(style={'borderWidth': "0.3vh", "width": "100%",
                    "backgroundColor": "#B4E1FF", "opacity": "1"}), width={'size': 10}),
            # ], width={"size": 1}, align="center")
        ], justify="center"),
        dbc.Row([
            dbc.Col(html.H3("Fitness doporučení: ", className="text-center m-4"), align="center",
                    style={"color": dark}, xs={"size": 8}, sm={"size": 6}, md={"size": 3}, width={"size": 3}),
            dbc.Col(html.Div(children=[],id="alert_1"), align="center",
                    style={"color": "white"}, xs={"size": 8}, sm={"size": 5}, md={"size": 4}, width={"size": 4}),
            dbc.Col(html.Div(children=[],id="alert_2"), align="center",
                    style={"color": "white"}, xs={"size": 8}, sm={"size": 5}, md={"size": 4}, width={"size": 4}),
        ], justify="center"),
        dbc.Row([
            dbc.Col(html.Hr(style={'borderWidth': "0.3vh", "width": "100%",
                    "backgroundColor": "#B4E1FF", "opacity": "1", "margin-bottom": 30}), width={'size': 10}),
        ], justify="center")
    ]),
    html.Div([
        dbc.Row([dbc.Col(html.H1(""))]),
        dbc.Row([dbc.Col(html.H1(""))]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id="graph-1", figure={}, className="border border-dark"), className="m-2", width={"size": 4}, xs={"size": 10}, sm={"size": 8}, md={"size": 5}
            ),
            dbc.Col(
                dcc.Graph(id="graph-2", figure={}, className="border border-dark"), className="m-2", width={"size": 4}, xs={"size": 10}, sm={"size": 8}, md={"size": 5}
            ),
            dbc.Col(
                dcc.Graph(id="graph-3", figure={}, className="border border-dark"), className="m-2", width={"size": 4}, xs={"size": 10}, sm={"size": 8}, md={"size": 5}
            ),
            dbc.Col(
                dcc.Graph(id="graph-4", figure={}, className="border border-dark"), className="m-2", width={"size": 4}, xs={"size": 10}, sm={"size": 8}, md={"size": 5}
            )

        ], className="g-0", justify="evenly")
    ], style={"background": dark, "border-radius": "25px", "margin-top": 10})
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
    if n_clicks > 0:
        if uname not in li:
            return "warning", dash.no_update, "Not a user", dash.no_update, dash.no_update
        if li[uname][0] == passw:
            return "success", '/dashboard%'+base64.b64encode(uname.encode("utf-8")).decode("utf-8"), "Success!", True, False
        if uname in li.keys() and passw != li[uname][0]:
            return "danger", dash.no_update, "Wrong credentials", False, True
    else:
        return "primary", dash.no_update, "Log In", dash.no_update, dash.no_update


@ app.callback(dash.dependencies.Output('page-content', 'children'),
               [dash.dependencies.Input('url', 'pathname'), ])
def display_page(pathname):
    if re.findall("\A/dashboard", pathname) == ["/dashboard"]:
        if len(re.split("%", pathname)[1]) % 4 == 0:
            return index
        else:
            return login
    else:
        return login


@ app.callback(Output(component_id="subname", component_property="children"),
               [dash.dependencies.Input("st-dpdn", "value"), ])
def set_name(input_value):
    if not input_value == None:
        return input_value
    else:
        return "Třída"


@ app.callback(
    Output(component_id="admin", component_property="children"),
    Input(component_id="url", component_property="pathname"),
)
def update_output_row(pathname):
    if not li.__contains__(base64.b64decode(re.split("%", pathname)[1]).decode("utf-8")):
        return None
    if li[base64.b64decode(re.split("%", pathname)[1]).decode("utf-8")].__contains__("teacher"):
        return generate_dropdown(file1)
    else:
        return None


@ app.callback([Output("stuclass", "children"), Output("stuage", "children"), Output("stusex", "children"),
                Output("graph-1", "figure"), Output("graph-2",
                                                    "figure"), Output("graph-3", "figure"),
                Output("steps", "value"), Output(
                    "steps", "label"), Output("steps", "color"),
                Output("heartrate", "value"), Output("heartrate", "label"), Output("heartrate", "color"),
                Output("alert_1", "children")],
               [Input("cls-dpdn", "value"), Input("wk-dpdn", "value"), Input("st-dpdn", "value")])
def update_card(_class, wk, stu):
    if not stu == None:
        if wk == "Distanční":
            file = file1
        elif wk == "Prezenční":
            file = file2
        df = load_dataframe(file)
        temp = df[df["ALIAS"] == stu]
        student_age = 2022-int(temp["YoB"].unique()[0])
        student_sex = temp["Sex"].unique()[0]
        figs = generate_graphs(file, stu)
        means = generate_average(file, stu)
        steps_count = str(int(means[1])) + " kroků za den"
        steps_percent = int(means[1]/110)
        heartbeat_count = str(int(means[0])) + " BPM"
        heartbeat_percent = int(means[0]/1.5)

        if steps_percent < 50:
            colorBarSteps = red
            alertOne = generate_alerts("Průměrný počet kroků je velice slabý","danger")
        elif steps_percent >= 50 and steps_percent < 75:
            colorBarSteps = yellow
            alertOne = generate_alerts("Průměrný počet kroků je podprůměrný","warning")
        else:
            colorBarSteps = green

        if heartbeat_percent < 80:
            colorBarHR = green
        elif heartbeat_percent >= 80 and heartbeat_percent < 110:
            colorBarHR = yellow
        else:
            colorBarHR = red

        return f"Třída: 3.B", f"Věk: {student_age}", f"Pohlaví: {student_sex}", figs[0], figs[1], figs[2], steps_percent, steps_count, colorBarSteps, heartbeat_percent, heartbeat_count, colorBarHR, alertOne
    else:
        return "Třída: 3.B","Počet Studentů: 20","", dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


@ app.callback([Output("sleep", "value"), Output("sleep", "label"), Output("sleep", "color"), Output("graph-4", "figure")],
               [Input("cls-dpdn", "value"), Input("wk-dpdn", "value"), Input("st-dpdn", "value")])
def update_sleep(_class, _week, _stu):
    if _week == "Distanční":
        file = file1
    elif _week == "Prezenční":
        file = file2
    sleeps = daily_sleep(file, _stu)
    piechart = generate_piechart(file, _stu)
    sleep_val = int(np.mean(sleeps[0])/60)
    sleep_percent = int((np.mean(sleeps[0])*10/60))
    if sleep_percent < 50:
        colorBarSleep = red
    elif sleep_percent >= 50 and sleep_percent < 75:
        colorBarSleep = yellow
    else:
        colorBarSleep = green
    return sleep_percent, f"{sleep_val} hodin za noc", colorBarSleep, piechart


if __name__ == "__main__":
    app.run_server(debug=True)
