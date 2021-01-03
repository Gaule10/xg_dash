#!/usr/bin/env python
# coding: utf-8

# ## Melita FC Expected Goals Tracker Website

# In[13]:


import pandas as pd
import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# In[14]:


def assign_xG(df):
    d = {'N':0,'F':0.01,'E':0.05,'D':0.09,'C':0.15,'B':0.24,'A':0.4,'A+':0.6,'Corner':0.18}
    
    Melita = df.columns[0]
    Opposition = df.columns[1]
    
    df[Melita + '_xG'] = df[Melita].apply(lambda x: d.get(x)).astype('float')
    df[Opposition + '_xG'] = df[Opposition].apply(lambda x: d.get(x)).astype('float')
    
    return df


# In[15]:


df = pd.read_csv('game_data.csv')
df['Time'] = pd.to_numeric(df['Time'])
df['Date'] = pd.to_datetime(df['Date'],dayfirst=True)
df.set_index('Time',inplace=True)
df = assign_xG(df)


# In[12]:


app = dash.Dash(__name__)
server = app.server
team_names = df['Date'].dt.date.unique()
team_names.sort()
app.layout = html.Div([
    html.Div([dcc.Dropdown(id='select_team', options=[{'label': i, 'value': i} for i in team_names],
                           value=team_names[0], style={'width': '140px'})]),
    dcc.Graph("line-chart", config={'displayModeBar': True})])
@app.callback(
    Output("line-chart", 'figure'),
    [Input('select_team', 'value')]
)

def update_graph(grpname):
    import plotly.express as px
    fig = px.line(df[df.Date == grpname], x=df[df.Date == grpname].index, 
                   y=[df[df.Date == grpname].Opp_Reg_xG,df[df.Date == grpname].Mel_Reg_xG],labels={'x':'Time','value':'xG'})
    fig.update_layout(title_text="Expected Goals Tracker", legend_title="Teams")
    d = {'2020-12-14':'St Andrews','2020-12-07': 'Lija','2020-12-21':'Valletta'}
    nameswap = {'wide_variable_0': d.get(grpname),'wide_variable_1': 'Melita'}
    
    for i, dat in enumerate(fig.data):
        for elem in dat:
            if elem == 'name':
                fig.data[i].name = nameswap[fig.data[i].name]
    return fig
    

if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:




