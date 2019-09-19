# conda env create -f environment.yml
# pip install jupyter
# python -m ipykernel install --user --name scraper_env
# pip install requests
# pip install cufflinks
# pip install openpyxl
# pip install xlrd

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
start = datetime.datetime(Y,M-1,D)

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

df_excel = pd.read_excel("API_output.xlsx")
df_excel.index.name = 'Date'
df_excel.index = df_excel['Date']
df_excel = df_excel.drop(['Date'] , axis='columns')


last_row = df[-1:]
last_row.index.name = 'Date'
last_row.index = [end]


result = pd.DataFrame()
if not last_row.index.isin(df_excel.index)[0]:
    result = pd.concat([df_excel, last_row],ignore_index=False)
    result.index.name = 'Date'
    result.to_excel("API_output.xlsx")