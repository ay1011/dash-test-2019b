import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_excel("API_output.xlsx")
#print(df.head())


available_locations = df.columns[1:].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_locations],
                value=['W.P. KUALA LUMPUR - Cheras', 'W.P. PUTRAJAYA - Putrajaya'],
                multi=True
            )
        ],style={'width': '48%', 'float': 'top', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('yaxis-column', 'value')
    ])

def update_graph(yaxis_column_name): #xaxis_type, yaxis_type,

    return {
        'data': [go.Scattergl(
            x=df['Date'],
            y=df[col],
            name=col,
            #text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='lines+markers',
            marker={
                'size': 5,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for col in yaxis_column_name ],


        'layout': go.Layout(
            #xaxis_range=list(df.index),
            #xaxis = dict(tickformat='%y-%m-%d'),
            yaxis={
                'title': 'Air Pollution Index'#yaxis_column_name
                #'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
            width=1600,
            height =800,
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
#'''