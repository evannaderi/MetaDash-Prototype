from flask import Flask 
import dash 
from dash import dcc, html 
from dash.dependencies import Input, Output 
import plotly.express as px 
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go 
 
# Flask server 
server = Flask(__name__) 
app = dash.Dash(__name__, server=server, url_base_pathname='/') 
 
# Load the data 
import os
print(os.getcwd())
df = pd.read_csv('app/data.csv') 
df = df.sort_values(by='Student Name', ascending=True) 
 
# Colors for each emotion 
colors = { 
    'Engaged (%)': 'green', 
    'Confused (%)': 'yellow', 
    'Frustrated (%)': 'orange', 
    'Annoyed (%)': 'red' 
} 
 
# Dash layout 
app.layout = html.Div([ 
    html.H1("Teacher View", style={'textAlign': 'center', 'color': 'white'}), 
    html.H2("Chemistry 101", style={'textAlign': 'center', 'color': 'white'}), 
    html.H3("Phase 1: Definition of Task", style={'textAlign': 'center', 'color': 'white'}), 
    html.Br(), 
    html.Div([html.Div(dcc.Graph(id='live-graph',), style={'width': '40%', 'display': 'inline-block'}), 
              html.Div(dcc.Graph(id='live-graph2'), style={'width': '20%', 'display': 'inline-block'}), 
              html.Div(dcc.Graph(id='live-graph3'), style={'width': '20%', 'display': 'inline-block'}), 
              html.Div(dcc.Graph(id='live-graph4'), style={'width': '20%', 'display': 'inline-block'}) 
             ]), 
    dcc.Interval( 
        id='interval-component', 
        interval=1 * 1000, 
        n_intervals=0 
    ) 
], style={'backgroundColor': 'black', 'color': 'white'}) 

@app.callback( 
    [Output('live-graph', 'figure'), 
     Output('live-graph2', 'figure'), 
     Output('live-graph3', 'figure'), 
     Output('live-graph4', 'figure')], 
    Input('interval-component', 'n_intervals') 
) 

def update_graph(n):
    # Randomly adjust values for simulation
    df['Engaged (%)'] += np.random.randint(-1, 2, df.shape[0])
    df['Confused (%)'] += np.random.randint(-1, 2, df.shape[0])
    df['Frustrated (%)'] += np.random.randint(-1, 2, df.shape[0])
    df['Annoyed (%)'] += np.random.randint(-1, 2, df.shape[0])

    # Ensure individual values remain between 0 and 100
    df[['Engaged (%)', 'Confused (%)', 'Frustrated (%)', 'Annoyed (%)']] = \
        df[['Engaged (%)', 'Confused (%)', 'Frustrated (%)', 'Annoyed (%)']].clip(0, 100)
    
    # Ensure engagement remains above 45
    df['Engaged (%)'] = df['Engaged (%)'].apply(lambda x: max(x, 45))
    
    # Ensure total doesn't exceed 100%
    for index, row in df.iterrows():
        total = row['Engaged (%)'] + row['Confused (%)'] + row['Frustrated (%)'] + row['Annoyed (%)']
        if total > 100:
            overflow = total - 100
            emotions = ['Engaged (%)', 'Confused (%)', 'Frustrated (%)', 'Annoyed (%)']
            for emotion in emotions:
                if row[emotion] >= overflow:
                    df.at[index, emotion] -= overflow
                    break
                    
        # Ensure engagement remains above 45
        df['Engaged (%)'] = df['Engaged (%)'].apply(lambda x: max(x, 45))

    # Create the bar chart
    fig = px.bar(df, 
                 x=['Engaged (%)', 'Confused (%)', 'Frustrated (%)', 'Annoyed (%)'], 
                 y='Student Name', 
                 labels={'value': 'Emotion'}, 
                 barmode='stack', 
                 orientation='h', 
                 color_discrete_map=colors, 
                 height=320, 
                 width=560)

    # Create the Engaged donut chart
    engaged_percentage = df['Engaged (%)'].mean()
    fig2 = go.Figure(data=[go.Pie(labels=["Engaged", "Other"], 
                                  values=[engaged_percentage, 100 - engaged_percentage], 
                                  hole=.3, marker_colors=["green", "lightgray"], 
                                  textinfo='none')])
    fig2.update_traces(textfont_size=20, hoverinfo='label+percent')
    fig2.add_annotation(text=str(round(engaged_percentage)) + "%", 
                        x=0.5, y=0.5, font_size=10, showarrow=False)

    # Create the Confused donut chart
    confused_percentage = df['Confused (%)'].mean()
    fig3 = go.Figure(data=[go.Pie(labels=["Confused", "Other"], 
                                  values=[confused_percentage, 100 - confused_percentage], 
                                  hole=.3, marker_colors=["yellow", "lightgray"], 
                                  textinfo='none')])
    fig3.update_traces(textfont_size=20, hoverinfo='label+percent')
    fig3.add_annotation(text=str(round(confused_percentage)) + "%", 
                        x=0.5, y=0.5, font_size=10, showarrow=False)

    # Create the Frustrated donut chart
    frustrated_percentage = df['Frustrated (%)'].mean()
    fig4 = go.Figure(data=[go.Pie(labels=["Frustrated", "Other"], 
                                  values=[frustrated_percentage, 100 - frustrated_percentage], 
                                  hole=.3, marker_colors=["orange", "lightgray"], 
                                  textinfo='none')])
    fig4.update_traces(textfont_size=20, hoverinfo='label+percent')
    fig4.add_annotation(text=str(round(frustrated_percentage)) + "%", 
                        x=0.5, y=0.5, font_size=10, showarrow=False)

    # Update layouts for each doughnut chart for colors and size
    for doughnut_fig in [fig2, fig3, fig4]:
        doughnut_fig.update_layout({
            'plot_bgcolor': 'black',
            'paper_bgcolor': 'black',
            'font': {
                'color': 'white'
            }
        })
        doughnut_fig.update_traces(marker=dict(line=dict(color='black', width=2)))

    return fig, fig2, fig3, fig4


@server.route('/') 
def index(): 
    return app.index() 

# if __name__ == '__main__': 
#     server.run(debug=True) 
