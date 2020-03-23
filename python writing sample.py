#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 19:28:54 2019

@author: hanqiuyang
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from scipy import stats
import dash_table


df1 = pd.read_excel('https://s3.amazonaws.com/programmingforanalytics/NBA_data.xlsx')

#Preparation for regression line
xi = df1['Age']
y = df1['Salary']
slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)
line = slope*xi+intercept

###Distribution Scatter Plot Initial
plot1 = go.Scatter(x = df1['Age'],
                   y = df1['Salary'],
                                    
                   mode = 'markers',
                   opacity = 0.8,
                   marker = {
                           'size': 15,
                           'line': {'width': 0.5, 'color': 'white'}
                           },
                   name = 'Actual Distribution')


###Regression Line plt
plot2 = go.Scatter(x = df1['Age'],
                   y = line,
                   mode = 'lines',
                   marker=go.Marker(color='rgb(31, 119, 180)'),
                   name = 'Regression Line'
                   )


###General Layout Setting for plotly
layout = go.Layout(title = 'Regression Analysis Graph',
                   hovermode = 'closest',
                   xaxis = {'title':'Age'})


###Figure setting to put to graph together with the settled layout
fig = go.Figure(data = [plot1,plot2], layout = layout)

###Dictionary for Dropdown Menu
opt = [{'label':i,'value':i} for i in df1.columns]


def generate_table(dataframe, max_rows=20):
    return html.Table(
    
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


###Call out app body
app = dash.Dash(__name__,suppress_callback_exceptions=True)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'font-family': 'cursive',
    'font-size': '20px',
    'text-align': 'center'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#07436D',
    'color': 'white',
    'padding': '6px',
    'font-family': 'cursive',
    'font-size': '20px'
}

app.layout = html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Overview', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Data Display', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Regression Plot', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Bar Chart', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Scatter Plot', value='tab-5', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Histogram', value='tab-6', style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])

@app.callback(Output('tabs-content-inline', 'children'),
              [Input('tabs-styled-with-inline', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
                html.H1('NBA Dataset Overview', style = {'backgroundColor':'skyblue', 'textAlign': 'center'}),
                html.H3('Team Shiny: Guotian Kan, Hanqiu Yang, Ziwei Yang, Elianna Wang, Sean Fan', style = {'backgroundColor':'skyblue', 'textAlign': 'center'}),
                html.P('''This is the Python Dashboard regarding the NBA data set.
                          Data is displayed in dataframe form.
                          An interactive single variable regression graph is displayed.
                          ''', style={'textAlign': 'center'}),
                html.Img(src="https://cdn.vox-cdn.com/thumbor/A96j6bHwcqiYAoE3GavXJgWaGV8=/0x0:3200x1800/1200x675/filters:focal(1248x358:1760x870)/cdn.vox-cdn.com/uploads/chorus_image/image/63069423/nba_25_best_2_getty_ringer.0.jpg", style={'height': '100%','width': '100%'})
        ])
    
    
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Super Stars Information Display'),
            dash_table.DataTable(id='table',
            columns=[{"name": i, "id": i} for i in df1.columns],
            data=df1.to_dict('records'),
            style_header={'backgroundColor': '#07436D','color': 'white','fontWeight': 'bold'},
            style_cell={'textAlign': 'center',
               'backgroundColor': 'white',
               'color': 'black',
               'font-family':'sans-serif'})
                    ])
    elif tab == 'tab-3':
        return html.Div([
            ###Regression graph dropdown    
            html.H3('Interactive Regression Chart'),
            html.Label('Choose an Independent Variable for Regression Analysis Against Salary'),
            html.Div(id = 'reg', style = {'padding':'50px'}),
        
            dcc.Dropdown(id = 'reg-id',
            options=opt,
        value='Age'
    ),
                                     
 ###Regression graph callout part
   
    dcc.Graph(id = 'plot', figure = fig),
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Horizontal Bar Plot of Points per Game'),
            html.Div(id = 'hori', style = {'padding': '35px 70px 50px 120px'}),
            dcc.Graph(id = 'horipart',
                  figure = {
                           'data': [go.Bar(
                               x = df1['Points_per_game'],
                               y = df1['Name'],
                               orientation = 'h')],
                            'layout': go.Layout(
                                    xaxis = {'title': 'Points/Game'},
                                    yaxis = {},
                                    bargap=0.25,
                                     margin = {'l': 190, 'b': 100, 't': 10, 'r': 100})
})
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H3('Scatter Plot of Player and his Points per Game'),
            html.Div(id = 
             'scatter1',
             style = {'padding': '40px'}),
                     dcc.Graph(id = 'scatter2',
                  figure = {
                          'data': [go.Scatter(
                                  y = df1['Points_per_game'],
                                  x = df1['Name'],
                                  mode = 'lines+markers'
                                
                                  )],
                            'layout': go.Layout(
                                    xaxis = {'title':'Points/Game', 'color':'grey', 'showline':True},
                                    yaxis = {'title':'Player','color':'grey', 'showline': True})   
    })                            
])
    elif tab == 'tab-6':
        return html.Div([
                html.H3('Sorted Bar of Salary and Points per Game'),
                html.Div(id = 'bar', style = {'padding':'40px'}),
                dcc.Graph(id = 'barplot',
                     figure = {
                              'data': [go.Bar(
                               x = df1['Points_per_game'],
                               y = df1['Salary'],
                              
                                      marker = {'color': y,
                                                'colorscale': 'Viridis'})],
                                'layout' : go.Layout(
                                        xaxis = {'categoryorder': 'array',
                                                 'categoryarray': [x for _, x in sorted(zip(df1['Salary'],df1['Points_per_game']))],
                                                 'title': 'Points/Game'}
                                        )}
                                )
                ])

@app.callback(Output('plot', 'figure'),
             [Input('reg-id', 'value')])


###Function to Update the Plot after Dropdown Menu Selected
def update_figure(opt):

    
    xi = df1[opt]
    y = df1['Salary']
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)
    line = slope*xi+intercept
    
    plot1 = go.Scatter(x = df1[opt], y = df1['Salary'],
                    
                        mode = 'markers',
                        line = dict(width = 2,
                                    color = 'rgb(229, 151, 50)'),
                        name = 'Actual Distribution of "{}"'.format(opt))
    
    plot2 = go.Scatter(x = df1[opt],
                   y = line,
                   mode = 'lines',
                   marker=go.Marker(color='rgb(31, 119, 180)'),
                   name = 'Salary'
                   )
    
    layout = go.Layout(title = 'Regression Analysis Graph',
                   hovermode = 'closest',
                   xaxis = {'title':'Age'})

    
    fig = go.Figure(data = [plot1,plot2], layout = layout)
    return fig

###Callback Text Description of Selected Dropdown Individual Variables
@app.callback(Output('reg','children'),
              [Input('reg-id','value')])

###Display Text
def display_value(value):
    return 'You selected "{}"'.format(value) + ' against "Salary"'

 
if __name__ == '__main__':
    app.run_server(debug=False)