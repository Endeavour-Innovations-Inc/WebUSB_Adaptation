#wave_viewer.py

import usb_reader

import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# load data
df = pd.read_csv('data.csv')

# make plot
fig = px.histogram(df, x='Age')
# initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
# set app layout
app.layout = html.Div(children=[
    html.H1('Test Dash App', style={'textAlign':'center'}),
    html.Br(),
    dcc.Dropdown(
        options=[{'label': i, 'value': i} for i in df.columns],
        value='Age',
        id='dropdown',
        style={"width": "50%", "offset":1,},
        clearable=False,
    ),
    dcc.Graph(id='histogram', figure=fig)
])
if __name__ == "__main__":
    app.run_server(debug=True)

usb_reader.get_device_info()