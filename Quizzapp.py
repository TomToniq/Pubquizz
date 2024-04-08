from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import  datetime

from Task import Task
from Team import Team

# Add some dummy Tasks & Solutions
Tasks = [
    Task("Solve 2x=4", 2),
    Task("Anglesum in a triangle", 180),
    Task("Smallest prime", 2)
]
# Add some Teams and their Auth Tokens.

Teams = [Team(Name, Token) for Name, Token in {
        "Blue" : "BERRY",
        "Red": "WHINE",
        "Yellow": "SUN",
        "Green": "TREE"
    }.items()
]

app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

def serve_layout():
    time = datetime.datetime.now()

    # Get Teams-Table
    TeamTable = pd.DataFrame([ {k:v for k, v in T.__dict__.items() if k != 'Submission_History' } for T in Team.Instance_Arr])
    TeamTable.index += 1
    TeamTable = TeamTable.sort_values(by=['Score'], ascending=False).reindex()

    # Get TaskTable

    TaskTable = pd.DataFrame([T.__dict__ for T in Task.Instance_Arr])
    D ={  i: Task[i].get_current_value() for i in  TaskTable['ID']    }
    TaskTable['Value'] = TaskTable['ID'].map(D)

    return dbc.Container(
        [
            dbc.Row(
                html.H1(f'Game State {time:%H:%M:%S}')
            ), 
            
            dbc.Row(
                [
                    dbc.Col(
                            [
                                dcc.Markdown("## Teams"), 
                                dash_table.DataTable(data=TeamTable[['Name', 'Score', 'Joker']].to_dict('records'))
                                
                            ], 
                            width=6,
                        ),
                    dbc.Col(
                            [
                                dcc.Markdown("## Tasks"),
                                dash_table.DataTable(data=TaskTable[['Value', 'ID', 'Text']].to_dict('records'))

                            ], 
                            width = 6,
                        )
                ]
            ),
            html.Br(),
            dbc.Row(
                [

                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id = "Task",
                                options= [f'Task {T.ID}' for T in Task.Instance_Arr] + ['Joker'],
                                style={"width":"100%"},
                                placeholder="Submission",
                            )
                        ],
                        width=3
                    ), 
                    dbc.Col(
                        [
                            dcc.Input(
                                id = "Submission",
                                value = "",
                                type="text", 
                                placeholder="Input",
                                style={"width":"100%"},
                            )
                        ],
                        width=3
                    ),
                    dbc.Col(
                        [
                            dcc.Input(
                                id = "Token",
                                value = "",
                                type="text", 
                                placeholder="Token",
                                style={"width":"100%"},
                            )
                        ],
                        width=3
                    ), 
                    dbc.Button(
                        "OK", id="Submission-Button", className="me-2", n_clicks=0
                    )              
                ]
            ),
            html.Span(id="Response", style={"verticalAlign": "middle"}),        
        ]
    )

app.layout = serve_layout
@callback(
            Output("Response", "children"), 
              Input('Submission-Button', 'n_clicks'),
              State('Task', 'value'),
              State('Submission', 'value'),
              State('Token', 'value')
         )

def on_button_click(n, TaskID, Submission, Token):
    if n == 0:
        return 
    else:
        T = Team.get_Team(Token)
        if T is None:
            return "Invalid Token. No changes made.."
        
        if TaskID == 'Joker':
            result = T.Pick_Joker(Submission)            
            if result:
                return f'Joker set for Task {Submission}.'
            else:
                return f'Joker was not set.'

        # Strip the Label. Get only the number.
        TaskID = int(TaskID[5:])

        result = T.Submit(TaskID, int(Submission))   
        if result == 0:
            return "Data was submitted previously. No changes made."
        if result > 0:
            return f'Correct. {result} Points for Team {T.Name}.'
        if result < 0:
            return f'Incorrect. {result} Points for Team {T.Name}'

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')