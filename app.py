import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#df = pd.read_excel("API_output.xlsx")
#print(df.head())
import urllib.request, json
from requests.exceptions import ConnectionError
import plotly.plotly as py
import cufflinks as cf
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#cf.go_offline
#init_notebook_mode(connected=True)
import pandas as pd
import numpy as np
import datetime
#import plotly
#print(plotly.__version__)
#print(cf.__version__)

def get_data(x):
    year = x.strftime("%Y")
    month = x.strftime("%m")
    day = x.strftime("%d")
    URL = 'http://apims.doe.gov.my/data/public/CAQM/hours24/' + year + '/' + month + '/' + day + '/0000.json'
    try:
        with urllib.request.urlopen(URL) as url:
            data = json.loads(url.read().decode())

            df = pd.DataFrame(data['24hour_api'])
            df.columns = df.iloc[0]
            df.index = df['State'] + ' - ' + df['Location']
            df = df.drop(['State - Location'])
            df = df.replace('\**', '', regex=True)
            df = df.drop(columns='State')
            df = df.drop(columns='Location')
            df = df.T
            df.index.name = x.strftime("%Y-%b-%d")
            df.index = pd.date_range(start=pd.datetime(int(year), int(month), int(day), 1),
                                     end=pd.datetime(int(year), int(month), int(day), 1) + pd.DateOffset(1),
                                     freq="H")[:24]
            return df
    except IOError:
        print("404 Not Found")
        pass

    df = pd.DataFrame()
    return df


Y = pd.to_datetime('today').year
M = pd.to_datetime('today').month
D = pd.to_datetime('today').day
H = pd.to_datetime('today').hour
start = datetime.datetime(Y-3,M,D)

end = datetime.datetime(Y,M,D,H)
daterange = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]


#print(start)
df = get_data(start)
for i,x in enumerate(daterange[1:]):
    #print(x)
    df=df.append(get_data(x))
#print(end)
# delete all rows after
indexNames = df[df.index > end].index
df.drop(indexNames , inplace=True)
df.index.name = 'Date'

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