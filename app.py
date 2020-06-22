import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server #to deploy on Heroku

df = pd.read_csv('assets/data.csv')
list_of_names = df['students'].unique()

info1='No course clicked in grades graph'
info2='No course clicked in weekly hours graph'


def generate_Dropdown(list_of_students):
    return dcc.Dropdown(
        id='student_name',
        options=[{'label': i, 'value': i} for i in list_of_students],
        value=''
    )

def getSum(subjectName):
    sum=0
    GroupDataSubject=df[df['courses'] == subjectName]
    Marks=GroupDataSubject['grades']
    for mark in Marks:
        sum +=mark
    avg= sum/ (len(Marks))
    return round(avg,2)

mAdvWebTech = getSum('AdvWebTech')
mBDLA = getSum('BDLA')
mLA = getSum('LA')
mLAVA = getSum('LAVA')



def getDuration(subjectName):
    sum=0
    GroupDataSubject=df[df['courses'] == subjectName]
    Durations=GroupDataSubject['week_hours']
    for duration in Durations:
        sum +=duration
    avg= sum/ (len(Durations))
    return round(avg,2)

dAdvWebTech = getDuration('AdvWebTech')
dBDLA = getDuration('BDLA')
dLA = getDuration('LA')
dLAVA = getDuration('LAVA')

app.layout = html.Div(children=[
    html.Div(className=' container row', children=[
        html.Div(className='row', children=[
            html.Div(className='six columns',
                children=[
                    html.H1('Dash Assignment', style={'color': 'black','float':'left'})
                ])
        ]),
        html.Div(className='row', children=[
            html.Div(className='four columns',
                children=[
                    html.H1('Select Students', style={'color': 'black','float': 'left','font-size':'16pt'})
                ]),
            html.Div(className='four columns',
                children=[
                    html.H1('Last clicked course information', style={'color': 'black', 'float': 'left','font-size':'16pt'})
                ]),
        ]),
        html.Div(className='row', children=[
            html.Div(className='four columns',
                children=[
                    generate_Dropdown(list_of_names),
                ]),
            html.Div(className='five columns', id='status'),
        ]),
            html.Div(className='twelve columns', style={'marginTop': 50, },
            children=([

                dcc.Graph(id='bar_chart', className='six columns', clickData={'points': []}),
                dcc.Graph(id='dot_chart', className='six columns', clickData={'points': []})

            ])),

    ])
])

colors = {'marker_color': '#6495ED', 'menBar': '#00008B', 'text': '#FFFFF'}

@app.callback(
    Output('bar_chart', 'figure'),
    [Input('student_name', 'value')])
def update_graph(student_name_value):
    group_data_by_name = df[df['students'] == student_name_value]
    if group_data_by_name.empty:
        return{
                'data': [dict(
                x=['AdvWebTech', 'LA' , 'LAVA','BDLA'],
                y=[ mAdvWebTech, mLA, mLAVA, mBDLA],

                marker={'color': colors['marker_color']},
                type = 'bar'

            )],
                        'layout': dict(
                xaxis={
                    'title': 'Grades',
                    'style': {
                        'marginRight': 30,
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                },
                yaxis={
                    'title': 'Courses',
                    'style': {
                        'margin': {'l': 0, 'b': 50, 't': 0, 'r': 50},
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                    'dtick': 0.5, #scale y-axis
                },
                margin={'l': 40, 'b': 60, 't': 30, 'r': 0},
                title='Students average grades',
            )
            }
    else:
        return {
            'data': [dict(
                x=group_data_by_name['courses'].unique(),
                y=group_data_by_name['grades'],
                marker={'color': colors['marker_color']},
                type = 'bar'

            )],
            'layout': dict(
                xaxis={
                    'title': 'Grades',
                    'style': {
                        'marginRight': 30,
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                },
                yaxis={
                    'title': 'Courses',
                    'style': {
                        'margin': {'l': 0, 'b': 50, 't': 0, 'r': 50},
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                    'dtick': 0.5, #scale y-axis
                },
                margin={'l': 40, 'b': 60, 't': 30, 'r': 0},
                title='{} grades'.format(student_name_value),
            )
        }



@app.callback(
    Output('dot_chart', 'figure'),
    [Input('student_name', 'value')])
def dot_Chart(student_name_value):
    group_data_by_name = df[df['students'] == student_name_value]
    if group_data_by_name.empty:
        return{
                'data': [dict(
                x=['AdvWebTech', 'LA' , 'LAVA','BDLA'],
                y=[ dAdvWebTech, dLA, dLAVA,dBDLA],
                mode='markers',
                marker={
                    'size':15,
                    'line':{'width':0.5,'color': colors['marker_color'] }
                    },
                type = 'scatter'

            )],
                        'layout': dict(
                xaxis={
                    'title': 'Hours spend per week',
                    'style': {
                        'marginRight': 30,
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                },
                yaxis={
                    'title': 'Courses',
                    'style': {
                        'margin': {'l': 0, 'b': 50, 't': 0, 'r': 50},
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                    'dtick': 0.5, #scale y-axis
                },
                margin={'l': 40, 'b': 60, 't': 30, 'r': 0},
                title='Average weekly hours spend by students',
            )
            }
    else:
        return {
            'data': [dict(
                x=group_data_by_name['courses'].unique(),
                y=group_data_by_name['week_hours'],
                mode='markers',
                marker={
                    'size':15,
                    'line':{'width':0.5,'color': colors['marker_color'] }
                    },
                type = 'scatter'

            )],
            'layout': dict(
                xaxis={
                    'title': 'Hours spend per week',
                    'style': {
                        'marginRight': 30,
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                },
                yaxis={
                    'title': 'Courses',
                    'style': {
                        'margin': {'l': 0, 'b': 50, 't': 0, 'r': 50},
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                    'dtick': 1, #scale y-axis
                },
                margin={'l': 40, 'b': 60, 't': 30, 'r': 0},
                title='Average weekly hours spend by ' + student_name_value,
            )
        }
        
@app.callback(
    Output('status', 'children'),
    [Input('dot_chart', 'clickData'), Input('bar_chart', 'clickData')])
def state_one(clickdataValue1,clickdataValue2):
    info1='No course clicked in grades graph'
    info2='No course clicked in weekly hours graph'

    clickData1 = clickdataValue1
    clickData2 = clickdataValue2
    
    if clickData1["points"] != [] :
        data= clickdataValue1
        msgX=data['points'][0]['x']
        msgY=data['points'][0]['y']
        infoMsg2= 'Course: '+msgX+'-Hours/Week: '+ str(msgY)
        info2 = infoMsg2

    if clickData2["points"] != [] :
        data= clickdataValue2
        msgX=data['points'][0]['x']
        msgY=data['points'][0]['y']
        infoMsg1= 'Course: '+msgX+'- Grade: '+ str(msgY)
        info1 = infoMsg1

    return  html.Div([
        html.H6(info1, id='info1', style={ 'float': 'left','font-size':'12pt', 'margin-top': '0', 'margin-bottom': '0'}),
        html.Br(),
        html.H6(info2, id='info2', style={ 'float': 'left','font-size':'12pt', 'margin-top': '0', 'margin-bottom': '0'})
    ])
    
    

if __name__ == '__main__':
    app.run_server(debug=True)
