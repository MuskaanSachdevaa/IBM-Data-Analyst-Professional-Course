import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)

# Create a Dashboard application layout
app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Airline Performance Dashboard',
                                        style={
                                            'textAlign' :'center',
                                            'color' : '#503D36',
                                            'font-size' : 40
                                        }
                                ),
                                html.Div(
                                    ['Input Year: ', dcc.Input(
                                        id='input-year', value='2010', type='number',
                                        style={'height':'50px', 'font-size':35,})
                                    ],
                                    style={'font-size':40}),
                                    html.Br(),
                                    html.Br(),
                                    html.Div(dcc.Graph(id='line_plot')),
                                ])

# add callback decorator
@app.callback(Output(component_id='line_plot', component_property='figure'),
                Input(component_id='input-year', component_property='value'))

# Computation to be performed by callback function to return results.
def get_graph(entered_year):

    df = airline_data[airline_data['Year'] == int(entered_year)]

    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

    fig = go.Figure(data=go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8001, host='127.0.0.1', debug=True)
