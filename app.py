#!/usr/bin/env python
# coding: utf-8

# In[3]:


import dash
import plotly
import pandas as pd
import numpy as np
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# In[4]:


def assign_xG(df):
    d = {'N':0,'F':0.01,'E':0.05,'D':0.09,'C':0.15,'B':0.24,'A':0.4,'A+':0.6,'Corner':0.18}
    
    Melita = df.columns[0]
    Opposition = df.columns[1]
    
    df[Melita + '_xG'] = df[Melita].apply(lambda x: d.get(x)).astype('float')
    df[Opposition + '_xG'] = df[Opposition].apply(lambda x: d.get(x)).astype('float')
    
    return df


# In[5]:


df = pd.read_csv('game_data.csv')
df['Time'] = pd.to_numeric(df['Time'])
df['Date'] = pd.to_datetime(df['Date'],dayfirst=True)
df.set_index('Time',inplace=True)
df = assign_xG(df)


# In[ ]:


app = dash.Dash(__name__)
server = app.server
team_names = df['Date'].dt.date.unique()
team_names.sort()
app.layout = html.Div([
    html.Div([dcc.Dropdown(id='select_team', options=[{'label': i, 'value': i} for i in team_names],
                           value=team_names[0], style={'width': '140px'})]),
    dcc.Graph("fig_1", config={'displayModeBar': False}),
    dcc.Graph("fig_2",config={'displayModeBar': False})])
@app.callback(
    [Output("fig_1", 'figure'),Output("fig_2", 'figure')],
    [Input('select_team', 'value')]
)

def update_graph(grpname):
    import plotly.express as px
    fig1 = px.line(df[df.Date == grpname], x=df[df.Date == grpname].index, 
                   y=[df[df.Date == grpname].Opp_Reg_xG,df[df.Date == grpname].Mel_Reg_xG],labels={'x':'Time','value':'xG'})
    fig1.update_layout(title_text="Expected Goals Cumulative & Tracker", legend_title="Teams")
    d = {'2020-12-14':'St Andrews','2020-12-07': 'Lija','2020-12-21':'Valletta'}
    nameswap = {'wide_variable_0': d.get(grpname),'wide_variable_1': 'Melita'}
    
    for i, dat in enumerate(fig1.data):
        for elem in dat:
            if elem == 'name':
                fig1.data[i].name = nameswap[fig1.data[i].name]
                
    fig2 = px.line(df[df.Date==grpname],x=df[df.Date == grpname].index,y=[df[df.Date == grpname]['Opp_Reg_xG'].cumsum(),
                                                                          df[df.Date == grpname]['Mel_Reg_xG'].cumsum()],
                   labels={'x':'Time','value':'Cumulative xG'})
    fig2.update_layout(title_text="Melita vs "+d.get(grpname)+" " + "("+(df[df.Date==grpname].H_A[1]+")"), legend_title="Teams")
    d = {'2020-12-14':'St Andrews','2020-12-07': 'Lija','2020-12-21':'Valletta'}
    nameswap = {'wide_variable_0': d.get(grpname),'wide_variable_1': 'Melita'}
    for i, dat in enumerate(fig2.data):
        for elem in dat:
            if elem == 'name':
                fig2.data[i].name = nameswap[fig2.data[i].name]
                
    
    return [fig1,fig2]
    

if __name__ == '__main__':
    app.run_server(debug=False)


# In[15]:


df[df.Date=='2020-12-14'].H_A[1]


# In[ ]:




