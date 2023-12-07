import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask, send_from_directory, request, send_file
import plotly.graph_objs as go
import pandas as pd
import base64
import io
from flask_cors import CORS
from dash.exceptions import PreventUpdate
from flask import send_file
import xlsxwriter
import csv
from scipy.signal import lfilter
from scipy import signal
from datetime import datetime

import usb.core
import scope_interface
import numpy as np
import time

from scipy.fftpack import fft, ifft, fftfreq

#scope_interface.connect_to_scope()

server = Flask(__name__)
CORS(server)
app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/')

# Define initial empty trace and layout for the graph
initial_trace = go.Scatter(x=[], y=[], mode='lines')
layout = go.Layout(
    title="Input Signal",
    xaxis=dict(title='Time'),
    yaxis=dict(title='Amplitude (V)'),
    autosize=True
)

# Define your CSS styles inside a style tag
styles = {
    'graphControl': {
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'margin': '40px 0',
        'gap': '15px'
    },
    'buttonGroup': {
        'display': 'flex',
        'gap': '1px'
    },
    'chartDiv': {
        'borderTop': '1px solid rgba(0, 0, 0, 0.3)',
        'borderBottom': '1px solid rgba(0, 0, 0, 0.3)',
        'margin': '20px 0'
    },
    'cornerButtons': {
        'position': 'absolute',
        'left': '10px',
        'bottom': '10px',
        'display': 'flex',
        'gap': '10px'
    },
    'switch': {
        'display': 'flex',
        'alignItems': 'center'
    },
    'switchInput': {
        'display': 'none'
    },
    'switchLabel': {
        'position': 'relative',
        'display': 'inline-block',
        'width': '60px',
        'height': '34px'
    },
    'switchLabelBefore': {
        'content': '""',  # This might not work as expected, pseudo-elements may need to be handled differently
        'position': 'absolute',
        'top': '0',
        'left': '0',
        'width': '100%',
        'height': '100%',
        'backgroundColor': '#ccc',
        'borderRadius': '34px',
        'transition': '.4s'
    },
    'switchLabelAfter': {
        'content': '""',  # Same issue with content property here
        'position': 'absolute',
        'top': '4px',
        'left': '4px',
        'width': '26px',
        'height': '26px',
        'backgroundColor': 'white',
        'borderRadius': '50%',
        'transition': '.4s'
    },
    'switchInputChecked': {
        'backgroundColor': '#2196F3'
    },
    'switchLabelAfterChecked': {
        'transform': 'translateX(26px)'
    }
}

# Define a vertical layout style
vertical_layout_style = {
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'left',
    'justifyContent': 'center',
    'gap': '10px',  # Adjust the gap to your liking
}

# Define a style for the buttons and upload to make them less wide
button_style = {
    'width': 'auto',  # Set the width to 'auto' or specific value to make buttons less wide
    'maxWidth': '300px',  # Adjust the max width as needed
    'margin': '0 auto 10px auto'  # Add margins to center the buttons in the parent container
}

# App layout definition including Upload component and Graph component
# Define the layout of your app
app.layout = html.Div([
    html.Div([
        html.Button('Toggle View', id='view-mode', style={'width': '10%'}),
        html.Button('Enable Filter: Off', id='filter-toggle', n_clicks=0, style={'width': '10%'}),
        html.Button('Reset', id='reset-button', style={'width': '10%'}),
        html.Button('Export Data', id='export-button', style={'width': '10%'}),
        html.Button('Connect to Scope', id='connect-button', style={'width': '10%'}),
        html.Button('Collect Datapoints', id='get-data', style={'width': '10%'}),
    ], style=vertical_layout_style),
    
    # Graph control buttons (styled as per your CSS)
    # Graph control buttons (styled as per your CSS)
    html.Div(id='graphControl', style=styles['graphControl'], children=[
        html.Div(id='buttonGroup1', style=styles['buttonGroup'], children=[
            html.Button('↑', id='zoom-in1'),
            html.Button('Sub 3', id='sub-31'),
            html.Button('↓', id='zoom-out1'),
        ]),
        html.Div(id='buttonGroup2', style=styles['buttonGroup'], children=[
            html.Button('↑', id='zoom-in2'),
            html.Button('↓', id='zoom-out2'),
            html.Button('Sub 3', id='sub-32')
        ]),
        html.Button('Button 3', id='btn-3'),
        html.Button('Button 4', id='btn-4'),
    ]),

    
    # Placeholder for the graph with division lines (styled as per your CSS)
    html.Div(id='chartDiv', style=styles['chartDiv'], children=[
        dcc.Graph(id='my-graph', figure={'data': [initial_trace], 'layout': layout}),
    ]),
    
    # Small buttons in the lower left corner (styled as per your CSS)
    html.Div(id='cornerButtons', style=styles['cornerButtons'], children=[
        html.Button('Vert', id='vert-button'),
        html.Button('Horz', id='horz-button'),
    ]),

    html.Div(id='upload-timestamp', style={'display': 'none'}),
    
    # Component for triggering downloads
    dcc.Download(id='download-dataframe-csv')
])

# Initialize 'df' as a global variable outside of your callbacks
global df
df = pd.DataFrame()

global fft_on
fft_on = False

# Callback to handle filter toggle button
@app.callback(
    Output('filter-toggle', 'children'),
    [Input('filter-toggle', 'n_clicks')]
)
def toggle_filter(n_clicks):      
    if n_clicks % 2 == 0:  # If even number of clicks, filter is off
        return 'Enable Filter: Off'
    else:  # If odd number of clicks, filter is on
        return 'Enable Filter: On'


# Combined callback for updating graph with uploaded CSV data, resetting the graph, and applying a filter
@app.callback(
    Output('my-graph', 'figure'),
    [Input('view-mode', 'n_clicks'),
     Input('reset-button', 'n_clicks'),
     Input('connect-button', 'n_clicks'),
     Input('get-data', 'n_clicks')],
    [State('filter-toggle', 'children')],  # Add the switch's value as State
    prevent_initial_call=True
)
def update_graph(view, reset_clicks, connect, get_data, filter_toggle_label):
    global df 
    ctx = dash.callback_context

    global fft_on

    # Determine which input was triggered
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'view-mode':
        fft_on = not fft_on
        print(fft_on)

        if fft_on == True:
            # Number of sample points
            sig = df['data']
            X = fft(sig)
            N = len(X)
            n = np.arange(N)
            # sample spacing
            sr = 1000
            T = N/sr
            freq = n/T 

            n_oneside = N//2
            f_oneside = freq[:n_oneside]

            yf = fft(df['data'].values)
            xf = fftfreq(N, T)[:N//2]

            X_oneside =X[:n_oneside]/n_oneside

            trace = go.Scatter(x=f_oneside, y= np.abs(X_oneside), mode='lines', name='Frequency Spectrum')

        else:
            trace = go.Scatter(x=df['t'], y=df['data'], mode='lines', name='Original Data')

        return {'data': [trace], 'layout': layout}

    # If the reset button is clicked, clear the graph
    if triggered_id == 'reset-button':
        df = pd.DataFrame()  # Reset the 'df' variable
        return {'data': [initial_trace], 'layout': layout}

    if triggered_id == 'connect-button':
        scope_interface.program_scope()
        time.sleep(1)
        scope_interface.connect_to_scope()

    # If new file data is uploaded, update the graph
    if triggered_id == 'get-data':

        fft_on = False
        
        # Generate a timestamp to force the update
        timestamp = datetime.now()
        
        """
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        #df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        """

        trig = 1.234
        trig_bin = "{0:012b}".format(int(trig*1000))
        trig_low = int(trig_bin[4:12], 2)
        trig_hi = int(trig_bin[0:4], 2)

        rise = 0
        force = 0

        coupl = 1
        atten = 0

        trig_condition = "".join([str(rise), str(force)])

        configs = [1, int(trig_condition, 2), trig_low, trig_hi, atten, coupl]
        #configs = [1, 2, 3, 4, 5, 6]
        print('Configs are: ' + str(configs))

        try:
            scope_interface.configure_scope(configs)
            print('Device Configured!')
        except usb.core.USBError:
            print('Device Not Ready')
            pass

        v_data = []
        t_data = []

        data_ready = None
        while(data_ready == None):
            try:
                data_ready = scope_interface.check_for_data()
            except usb.core.USBError:
                print('Data Not Ready - Retrying in 3 Seconds')
                time.sleep(3)
                pass

        print('Interrupt Received From Device - Requesting Data...')

        v_data = scope_interface.get_samples()
        t_data = np.arange(0, len(v_data), 1)

        d = {'t': t_data, 'data': v_data}
        df = pd.DataFrame(d)

        print(len(v_data))
        
        # Check if the filter switch is enabled and apply the filter
        if 'On' in filter_toggle_label:
            # Define filter coefficients here for smoothing
            """
            b = [1, -0.95]  # Numerator coefficients
            a = [1]         # Denominator coefficients
            """
            b, a = signal.butter(3, 0.025)
            zi = signal.lfilter_zi(b, a)
            filtered_data = signal.filtfilt(b, a, df['data'])
            trace = go.Scatter(x=df['t'], y=filtered_data, mode='lines', name='Filtered Data')
        else:
            trace = go.Scatter(x=df['t'], y=df['data'], mode='lines', name='Original Data')

        return {'data': [trace], 'layout': layout}

    # Prevents update if not triggered by the inputs we're interested in
    raise PreventUpdate

@server.route('/download-csv')
def download_csv():
    global df  
    # This function uses the 'df' global DataFrame to create a CSV in memory
    output = io.BytesIO()
    df.to_csv(output, index=False, encoding='utf-8')
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='data.csv'
    )

# Callback to trigger a download when the 'Export Data' button is clicked
@app.callback(
    Output('download-dataframe-csv', 'data'),
    [Input('export-button', 'n_clicks')],
    prevent_initial_call=True
)
def export_data(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    # Trigger download
    return dcc.send_data_frame(df.to_csv, "data.csv", index=False)

if __name__ == '__main__':
    app.run_server(debug=True)
