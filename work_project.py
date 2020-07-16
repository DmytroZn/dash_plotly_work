from datetime import datetime as dt
from datetime import datetime
import plotly.offline as pyo
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import re
from get_df import GetDF



# import locale

# locale.getlocale()
# ('en_US', 'UTF-8')
# locale.setlocale(locale.LC_TIME, locale.getlocale())

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([
        html.Div([
            html.P('Оберіть дату: '),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                display_format='DD.MM.Y',
                min_date_allowed=dt(2018, 1, 1),
                max_date_allowed=dt(2020, 12, 1),
                # initial_visible_month=dt(2020, 11, 15),
                start_date = dt(2019,2,5).date(),
                end_date = str(datetime.now()).split(' ')[0],
                with_portal=True,
                number_of_months_shown=2,
                start_date_id='date-d',
                style={ },
            )],
            style={
                
                'width': '300px',
                'height': '80px',
                'padding': '50px',
                'border': '1px solid red',
                'text-align':'center',
                'border-radius': '21px',
                'background': '#A9A9A9',
            },


            lang='uk_UA.UTF-8'),
    ], 
    style={'display':'flex', 'justify-content':'center'}),

    dcc.RadioItems(
        id='my-radio-range',
        options=[
            {'label': 'Зона 1', 'value':'zona_1'},
            {'label': 'Зона 2', 'value':'zona_2'},
            {'label': 'Зона 3', 'value':'zona_3'},
            {'label': 'Зона 4', 'value':'zona_4'},
            {'label': 'Зона 5', 'value':'zona_5'},
            {'label': 'Зона 6', 'value':'zona_6'},
            {'label': 'Зона 7', 'value':'zona_7'},
        ],
        value='zona_1',
        # labelStyle={'display':'inline-block'}
    ),

    html.Div([
        html.Div(
            dcc.Graph(
                    id='output-graph',
                    animate=True,
                    style={'width':'700px'}    
            ),
        ),

        html.Div(
            dcc.Checklist(
                id='my-checklist',
                options=[
                    {'label':'t_input', 'value':'t_input'},
                    {'label':'t_output', 'value':'t_output'},
                    {'label':'capacity_current', 'value':'capacity_current'},
                    {'label':'w_current', 'value':'w_current'},
                    {'label':'pressure_x', 'value':'pressure_x'},
                ],
                value=['t_input'],
                style={'color':'#7FDBFF'}
            ),
            style={ 'display':'flex',
                    'align-items':'center',
                    'backgroundColor':'#111111'}
        )

    ],    
    lang='RU',
    style={ 'display':'flex',
            'justify-content':'center',
            'backgroundColor':'#111111'},
), 
],lang='uk_UA.UTF-8')
    
    # style={'backgroundColor':'green',
    #             'display':'flex',
    #             'justify-content':'space-between',} ),
    

    

colors = dict(t_input='rgb(128,0,0)', 
                t_output='rgb(255,165,0)', 
                capacity_current='rgb(0,128,0)', 
                w_current='rgb(0,0,255)', 
                pressure_x='rgb(255,0,255)' )

@app.callback(
    Output('output-graph', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('my-radio-range', 'value'),
     Input('my-checklist', 'value'),
     ])
def update_output(start_date, end_date, value, value2):
    start_date = str(datetime.strptime(start_date, "%Y-%m-%d"))
    end_date = str(datetime.strptime(end_date, "%Y-%m-%d"))
    res = GetDF(start_date, end_date)
    num = int(value.split('_')[1])
    df = res.controller(num)
    
    data  = [ {'x': df.index, 'y': df[col], 'name': col, 'marker':dict(color=colors[col])} for col in value2]
    layout = go.Layout(title='Графік залежностей', 
                        plot_bgcolor='#111111',
                        paper_bgcolor='#111111',
                        # xaxis=dict(range=[min('0'), max('50')]),
                        # yaxis=dict(range=[min(0), max(100)]),
                        font=dict(
                            color='#7FDBFF'
                        ))

    return {'data':data, 'layout':layout}
   
if __name__ == '__main__':
    app.run_server(debug=True)

    

