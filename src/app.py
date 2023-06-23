from asyncio.constants import SSL_HANDSHAKE_TIMEOUT
from cgi import test



import gspread
from oauth2client.service_account import ServiceAccountCredentials


import pandas as pd

import dash_auth
from dash import dash_table,dcc,html,ctx

from dash.exceptions import PreventUpdate
from dash_extensions.enrich import MultiplexerTransform, Output, Input, State, DashProxy
import pywhatkit

credential = ServiceAccountCredentials.from_json_keyfile_name("assets/credentials.json",
                                                              ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)




app = DashProxy(prevent_initial_callbacks=True,transforms=[MultiplexerTransform()])
server = app.server
auth = dash_auth.BasicAuth(app,{'test':'test'})
x=1


columns = ['Category','Company','Name','F_Index','Position','PhoneNo','Email']

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)





gsheet = client.open("sample market").get_worksheet(x)
df=pd.DataFrame(gsheet.get_all_records())

app.layout = html.Div([
    html.Div([
        html.H1("Client DB", style={'text-align':'center','font-family':'Roboto'}),
        dash_table.DataTable(
            id='dtb',
            columns=[
                {'name':i,'id':i} for i in df.columns
            ],
            data=df.to_dict('records'),
            filter_action='native',
            sort_action='native',
            sort_mode='multi',
            row_selectable='single',
            selected_rows=[],
            page_action='native',
            page_current=0,
            page_size=10,
            style_cell={'minWidth':95,'maxWidth':95, 'width':95},
            style_cell_conditional=[{'textAlign':'center'}],
            style_data={'whiteSpace':'normal','height':'auto'},
            editable=False                          
        ),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])]+ [
    html.Div(
        #[html.H3("Add Client",style={'font-family':'Roboto','margin-bottom':'10px'})] + 
    [ html.H3("Add Client",style={'font-family':'Roboto','margin-bottom':'10px'}),
        html.H4("Category",style={'font-family':'Roboto','display':'inline-block','width': '10%'}),
        #dcc.Input(id="Industry", placeholder="enter industry", type="text", style={'font-family':'Roboto','display':'inline-block','width': '89%'}, debounce=True),
        dcc.Dropdown(id='Category',options=[{'label':i,'value':i} for i in df['Category'].unique()],value=None, style={'font-family':'Roboto','display':'inline-block','width': '89%'}),
        html.H4("Add new category",style={'font-family':'Roboto','display':'inline-block','width': '16%'}),
        dcc.Input(id="add_category", placeholder="enter category", type="text", style={'font-family':'Roboto','display':'inline-block','width': '40%'}, debounce=True),
        html.Button('Add Category', id='add_cat', n_clicks=0,style={'width':'15%','display':'inline-block','margin-left':'10px','margin-right':'10px','margin-bottom':'10px'}),
        html.Div(id='output5', style={'width':'25%','display':'inline-block'}),
        html.H4("Company",style={'font-family':'Roboto','display':'inline-block','width': '10%'}),
        dcc.Input(id="Company", placeholder="enter company", type="text", style={'font-family':'Roboto','display':'inline-block','width': '89%'}, debounce=True),
        html.H4("Name",style={'font-family':'Roboto','display':'inline-block','width': '10%'}),
        dcc.Input(id="Name", placeholder="enter name", type="text", style={'font-family':'Roboto','display':'inline-block','width': '89%'}, debounce=True),
        html.H4("F Index",style={'font-family':'Roboto','display':'inline-block','width': '10%'}),
        dcc.Input(id="F_Index", placeholder="enter F index", type="text", style={'font-family':'Roboto','display':'inline-block','width': '89%'}, debounce=True),
        html.H4("Position",style={'font-family':'Roboto','display':'inline-block','width': '10%'}),
        dcc.Input(id="Position", placeholder="enter position", type="text", style={'font-family':'Roboto','display':'inline-block','width': '89%'}, debounce=True),
        html.H4("Phone No.",style={'font-family':'Roboto','display':'inline-block','width': '10%'}),
        dcc.Input(id="PhoneNo", placeholder="enter phone number", type="number", style={'font-family':'Roboto','display':'inline-block','width': '89%'}, debounce=True),
        html.H4("Email",style={'font-family':'Roboto','display':'inline-block','width': '10%'}),
        dcc.Input(id="Email", placeholder="enter email", type="email", style={'font-family':'Roboto','display':'inline-block','width': '89%'}, debounce=True)    
    ]
    + [html.Button("Add", id='add-button', n_clicks=0,style={'width':'10%','display':'inline-block','margin-right':'10px','margin-bottom':'10px'}),html.Div(id="output1",style={'width':'80%','display':'inline-block'})]
    + [html.Br()]
    + [html.Div(id="output6"),html.Button("Update", id='update-button', n_clicks=0,style={'width':'10%','display':'inline-block','margin-right':'10px','margin-bottom':'10px'}),html.Div(id="output7",style={'width':'80%','display':'inline-block'})]
    + [html.Br()]
    + [html.Div(id="output2"), html.Button("Delete", id='del-button', n_clicks=0,style={'width':'10%','display':'inline-block','margin-right':'10px','margin-bottom':'10px'}),html.Div(id="output3",style={'width':'80%','display':'inline-block'})]
    + [html.Br()]
    + [ html.Button("Clear Selection", id='clr-button', n_clicks=0,style={'width':'10%','display':'inline-block','margin-right':'10px','margin-bottom':'10px'}),html.Div(id="output8",style={'width':'80%','display':'inline-block'})]
    + [html.Br()],
    style={'width':'49.5%','display':'inline-block'}
    )]+ [ 
    html.Div([
        html.H3("Message Client",style={'font-family':'Roboto','margin-bottom':'10px'}),
        dcc.Input(id="Subject", placeholder="enter subject", type="text", style={'font-family':'Roboto','width': '99%'}, debounce=True),
        dcc.Textarea(
            id='textarea',
            #value='Message typed here will get sent directly on a new whatsapp web tab',
            placeholder='Message typed here will get sent directly on a new whatsapp web tab',
            style={'width': '99%','height':400},
        ),
        html.Button(
            "Send Whatsapp Message", id='whatsapp',
            n_clicks=0, style={'width':'30%','display':'inline-block','margin-right':'10px','margin-bottom':'10px'}),
        html.Div(
            id="output4",
            style={'width':'89%','display':'inline-block'})]
        , style = {'width':'49%','display':'inline-block','padding':'10px'}
    )
    ]
)
    


@app.callback(
    Output('output1', "children"),
    Output('dtb','data'),
    [Output("{}".format(_),"value") for _ in columns],
    Input('add-button', 'n_clicks'),
    [State("{}".format(_), "value") for _ in columns]
)
def add(*vals):
    
    if "add-button"== ctx.triggered_id:
        gsheet = client.open("sample market").get_worksheet(x)
        row = next_available_row(gsheet)
        cells = gsheet.range(row,1,row,7)
        for n, cell in enumerate(cells):
            cell.value = vals[n+1]
        gsheet.update_cells(cells)
        global df
        df=pd.DataFrame(gsheet.get_all_records())
        return "Added "+ vals[3], pd.DataFrame(gsheet.get_all_records()).to_dict('records'), "","","","","",None,""
    else:
        raise PreventUpdate

@app.callback(
    Output('output2', "children"),
    Output('output6', "children"),
    Output('output3', "children"),
    Output('dtb','data'),
    Input('del-button', 'n_clicks'),
    Input('dtb','selected_rows')
)
def delete(n,row):
    if not row:
       raise PreventUpdate
    else:
        #newrow = next_available_row(gsheet)
        if "del-button"==ctx.triggered_id:
            gsheet = client.open("sample market").get_worksheet(x)
            name = gsheet.cell(row[-1]+2,3).value
            gsheet.delete_rows(row[-1]+2)
            #gsheet.update_cells(cells)
            global df
            df=pd.DataFrame(gsheet.get_all_records())
            return "","", "Deleted "+name+" ", pd.DataFrame(gsheet.get_all_records()).to_dict('records')
        else:
            gsheet = client.open("sample market").get_worksheet(x)
            return "Delete selected client?","Update selected client?", "", pd.DataFrame(gsheet.get_all_records()).to_dict('records')

 
@app.callback(
    Input('dtb','selected_rows'),
    Input('whatsapp', 'n_clicks'),
    Input('textarea','value'),
    Output('output4','children')
)
def whatsapp(row,n,text):
    if not row:
        raise PreventUpdate
    else:
        if "whatsapp"==ctx.triggered_id: 

            gsheet = client.open("sample market").get_worksheet(x)
            name = gsheet.cell(row[-1]+2,3).value
            phno = gsheet.cell(row[-1]+2,5).value
            phno = phno.replace(" ","")
            phno = "+91"+phno
            pywhatkit.sendwhatmsg_instantly(phno,text)
            return "Switch tab to message " + name
        
@app.callback(
    [Output('Category', 'options'),Output('output5','children'),Output('add_category','value')],
    [Input('add_cat', 'n_clicks')],
    [State('add_category', 'value'), State('Category', 'options')]
)
def add_cat(n,new_value, current_options):
    if not new_value:
        return current_options,"",""
    else: 
        if "add_cat"==ctx.triggered_id:
            gsheet = client.open("sample market").get_worksheet(2)
            row=next_available_row(gsheet)
            gsheet.update_cell(row,1,str(new_value))
            df=pd.DataFrame(gsheet.get_all_records())
            return [{'label':i,'value':i} for i in df['Category']], "Added "+new_value, ""
        
@app.callback(
    Output('output6', "children"),
    [Output("{}".format(_),"value") for _ in columns],
    Input('dtb','selected_rows')
)
def update_blank(row):
    if not row:
        raise PreventUpdate
    else:
        return ("Update selected client? "),df.at[row[-1],'Category'],df.at[row[-1],'Company'],df.at[row[-1],'Contact Person'],df.at[row[-1],'F Index'],df.at[row[-1],'Portfolio'],df.at[row[-1],'Mob'],df.at[row[-1],'email']


@app.callback(
    Output('output6', "children"),
    Output('output7', "children"),
    Output('dtb','data'),
    [Output("{}".format(_),"value") for _ in columns],
    Input('update-button', 'n_clicks'),
    Input('dtb','selected_rows'),
    [State("{}".format(_), "value") for _ in columns]
)
def update(*vals):
    
    if "update-button"== ctx.triggered_id:
        gsheet = client.open("sample market").get_worksheet(x)
        row = vals[1][-1]+2
        cells = gsheet.range(row,1,row,7)
        for n, cell in enumerate(cells):
            cell.value = vals[n+2]
        gsheet.update_cells(cells)
        global df
        df=pd.DataFrame(gsheet.get_all_records())
        return "","Updated "+ vals[3], pd.DataFrame(gsheet.get_all_records()).to_dict('records'), "","","","","",None,""
    else:
        raise PreventUpdate

@app.callback(
    Output('output2', "children"),
    Output('output6', "children"),
    Output('output8','children'),
    Output('dtb','selected_rows'),
    Input('clr-button','n_clicks'),
    Input('dtb','selected_rows')
)
def clear(n,row):
    if not row:
        raise PreventUpdate
    else:
        if 'clr-button'==ctx.triggered_id:
            return "","","Cleared Selection",[]
        else:
            raise PreventUpdate

    





if __name__ == '__main__':
    app.run_server(debug=True)