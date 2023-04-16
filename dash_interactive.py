
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input,Output

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)

# Pie Chart Creation
fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')


# Create a dash application
app = Dash(__name__)

app.layout = html.Div(
    children = [
        html.H1("Airline Performance Dashboard",
        style={"textAlign":'center','color':"#503D36" , 'font-size':40}
        ),
        
        html.Div(
            [ "Input Year" , dcc.Input(
                id="input_year",
                value="2010",
                type="number",
                style={"height":"30px","font-size":"20px","width": "80px","margin-left":"10px"}),
            
            ],
            style={"font-size":25}
        ),

        html.Br(),
        html.Br(),
        html.Div(dcc.Graph(id="line_plot")),
    ]
)


@app.callback(
    Output("line_plot","figure"),
    Input("input_year","value")
)
def get_graph(entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]

    line_data = df.groupby("Month")["ArrDelay"].mean().reset_index()

    fig = go.Figure(data=go.Scatter(y=line_data["ArrDelay"], x=line_data["Month"], mode="lines",  marker=dict(color='green'))   )
    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig


# Run the application                   
if __name__ == '__main__':
    app.run_server(debug=True)