# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import os
from datetime import date
from PIL import Image
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, html, dcc, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def import_dataset(df=r'Archive\Modeling\Interactive Dashboard\dataset_ri.csv') -> pd.DataFrame:
    """
    Read the merged dataset csv and store in variables with the correct datatypes
    Returns a pd.Dataframe of the combined jobs and supply data
    """
    dataset = pd.read_csv(df, low_memory=False)

    dataset['uic'] = dataset['uic'].astype('string')
    dataset['apl'] = dataset['apl'].astype('string')
    dataset['cdm_rin'] = dataset['cdm_rin'].astype('string')
    dataset['csmp_narrative_summary'] = dataset['csmp_narrative_summary'].astype('string')

    dataset['date_closing'] = pd.to_datetime(dataset['date_closing'], errors='coerce')
    dataset['date_closing'] = dataset['date_closing'].dt.date

    dataset['date_maintenance_action'] = pd.to_datetime(dataset['date_maintenance_action'], errors='coerce')
    dataset['date_maintenance_action'] = dataset['date_maintenance_action'].dt.date

    dataset['eic'] = dataset['eic'].astype('string')
    dataset['equipment_nomenclature'] = dataset['equipment_nomenclature'].astype('string')
    dataset['eswbs_opening'] = dataset['eswbs_opening'].astype('string')
    dataset['identification_number_closing'] = dataset['identification_number_closing'].astype('string')
    dataset['iuc_screening_code'] = dataset['iuc_screening_code'].astype('string')
    dataset['location'] = dataset['location'].astype('string')
    dataset['safety_code'] = dataset['safety_code'].astype('string')
    dataset['tycom_screening_code'] = dataset['tycom_screening_code'].astype('string')
    dataset['type_availability_code'] = dataset['type_availability_code'].astype('int')
    dataset['type_of_maintenance_action'] = dataset['type_of_maintenance_action'].astype('string')
    dataset['work_center'] = dataset['work_center'].astype('string')
    dataset['def_narrative'] = dataset['def_narrative'].astype('string')
    dataset['nondef_narrative'] = dataset['nondef_narrative'].astype('string')
    dataset['closing_narrative'] = dataset['closing_narrative'].astype('string')
    dataset['ima_narrative'] = dataset['ima_narrative'].astype('string')
    dataset['job_status'] = dataset['job_status'].astype('string')
    dataset['priority'] = dataset['priority'].astype('string')
    dataset['component_status'] = dataset['component_status'].astype('string')
    dataset['type_of_availability_needed'] = dataset['type_of_availability_needed'].astype('string')
    dataset['tycom_screening'] = dataset['tycom_screening'].astype('string')
    dataset['when_discovered'] = dataset['when_discovered'].astype('string')
    dataset['intermediate_unit_commander_screening'] = dataset['intermediate_unit_commander_screening'].astype('string')
    dataset['deferral_reason'] = dataset['deferral_reason'].astype('string')
    dataset['opening_ship_system'] = dataset['opening_ship_system'].astype('string')
    dataset['closing_ship_system'] = dataset['closing_ship_system'].astype('string')
    dataset['action_taken'] = dataset['action_taken'].astype('string')
    dataset['cause'] = dataset['cause'].astype('string')
    dataset['ship'] = dataset['ship'].astype('string')
    dataset['jcn'] = dataset['jcn'].astype('string')

    dataset['issue_date'] = pd.to_datetime(dataset['issue_date'], errors='coerce')
    dataset['issue_date'] = dataset['issue_date'].dt.date

    dataset['issue_apl'] = dataset['issue_apl'].astype('string')
    dataset['issue_eic'] = dataset['issue_eic'].astype('string')
    dataset['niin_nomenclature'] = dataset['niin_nomenclature'].astype('string')
    dataset['unit_of_issue'] = dataset['unit_of_issue'].astype('string')
    dataset['source_code'] = dataset['source_code'].astype('string')
    dataset['jsn'] = dataset['jsn'].astype('string')

    dataset['demand_date'] = pd.to_datetime(dataset['demand_date'], errors='coerce')
    dataset['demand_date'] = dataset['demand_date'].dt.date

    dataset['Deck'] = dataset['Deck'].astype('string')
    dataset['Frame'] = dataset['Frame'].astype('string')
    dataset['Centerline (Distance)'] = dataset['Centerline (Distance)'].astype('string')
    dataset['Usage'] = dataset['Usage'].astype('string')

    dataset['date_closing'] = dataset['date_closing'].fillna('2022-06-16') #fill with last date so that we can display Open jobs as well

    dataset['totMaterialCost'] = dataset['totMaterialCost'].round(2) #Round for cleaner representation

    dataset['Supplies Ordered'] = dataset['totPrice'].notna().map({True: 'Yes', False: 'No'})

    

    return dataset

df = import_dataset()

columns = {
    'Unit Identification Code (UIC)': 'uic',
    'Job Sequence': 'job_seq',
    'Allowance Parts List (APL)': 'apl',
    'Cause Code': 'cause_code',
    'Ship Configuration': 'cdm_rin',
    'CSMP Narrative Summary': 'csmp_narrative_summary',
    'Date Closing': 'date_closing',
    'Date Maintenance Action': 'date_maintenance_action',
    'Deferral Reason Code': 'deferral_reason_code',
    'Due Date': 'due_date',
    'EIC': 'eic',
    'Equipment Nomenclature': 'equipment_nomenclature',
    'Expanded Ship Work Breakdown Structure (ESWBS) Opening': 'eswbs_opening',
    'Identification Number Closing': 'identification_number_closing',
    'IUC Screening Code': 'iuc_screening_code',
    'Location Code': 'location',
    'Man Hours Closing': 'mhc',
    'Man Hours Opening': 'mho',
    'Man Hours Remaining': 'mhr',
    'Priority Code': 'priority_code',
    'Safety Code': 'safety_code',
    'Status Code': 'status_code',
    'Tycom Screening Code': 'tycom_screening_code',
    'Type Availability Code': 'type_availability_code',
    'Type of Maintenance Action': 'type_of_maintenance_action',
    'When Discovered Code': 'when_discovered_code',
    'Total Intermediate Maintenance Action (IMA) Man Hours': 'total_ima_man_hours',
    'Total Ship Force Man Hours': 'total_ship_force_man_hours',
    'Total Replacement Cost': 'total_replacement_cost',
    'Total Repair Replacement Cost': 'total_repair_replacement_cost',
    'Deferred Narrative': 'def_narrative',
    'Deferral Reason': 'deferral_reason',
    'Non-Deferred Narrative': 'nondef_narrative',
    'Closing Narrative': 'closing_narrative',
    'Intermediate Maintenance Action (IMA) Narrative': 'ima_narrative',
    'Total Material Cost': 'totMaterialCost',
    'Opening Ship System': 'opening_ship_system',
    'Closing Ship System': 'closing_ship_system',
    'Job Status': 'job_status',
    'Days Open': 'days_open',
    'Action Taken': 'action_taken',
    'Intermediate Unit Commander Screening': 'intermediate_unit_commander_screening',
    'Priority': 'priority',
    'Component Status': 'component_status',
    'Type of Availability Needed': 'type_of_availability_needed',
    'Tycom Screening': 'tycom_screening',
    'When Discovered': 'when_discovered',
    'Cause of Maintenance': 'cause',
    'Ship': 'ship',
    'Job Sequence Number': 'jsn',
    'Supply Demand Date': 'demand_date',
    'Supply Issue Date': 'issue_date',
    'Supply Issue APL': 'issue_apl',
    'Supply Issue EIC': 'issue_eic',
    'National Item Identification Number (NIIN) Nomenclature': 'niin_nomenclature',
    'Supply Unit of Issue': 'unit_of_issue',
    'Supply Priority': 'supply_pri',
    'Supply Source Code': 'source_code',
    'Supply Quantity': 'quantity',
    'Supply Unit Price': 'unit_price',
    'Supply Total Price': 'totPrice',
    'JCN': 'jcn',
    'Work Center': 'work_center',
    'Deck': 'Deck',
    'Frame': 'Frame',
    'Centerline (Distance From)': 'Centerline (Distance)',
    'Compartment Usage': 'Usage',
    'Supplies Ordered': 'Supplies Ordered'
}

ship_name = {
    'CVN68': 'cvn68',
    'CVN69': 'cvn69',
    'CVN70': 'cvn70',
    'CVN71': 'cvn71',
    'CVN72': 'cvn72',
    'CVN73': 'cvn73',
    'CVN74': 'cvn74',
    'CVN75': 'cvn75',
    'CVN76': 'cvn76',
    'CVN77': 'cvn77',
    'CVN78': 'cvn78',
    'All Ships': 'All Ships'}

ship_options = list(ship_name.keys())
ship_options.sort()

feature_options = ['When Discovered', 'Cause of Maintenance', 'Component Status',
        'Priority', 'Type of Maintenance Action', 'Type of Availability Needed',
        'Action Taken', 'Compartment Usage', 'Work Center', 'Deferral Reason', 'Supplies Ordered', 'Job Status']

maintenance_action_type = {'d': 'Deferred', 'n': 'Non-Deferred'}

usage_dict = {
    'q': 'Miscellaneous space',
    'l': 'Living space',
    'a': 'Dry stowage',
    'e': 'Engineering space',
    'k': 'Chemicals and dangerous materials',
    'c': 'Ship control and fire control operating spaces',
    'm': 'Ammunition',
    't': 'Vertical access trunks',
    'v': 'Void Space',
    'w': 'Water stowage',
    'f': 'Fuel stowage',
    'j': 'Jet (aviation) fuel',
    'e(ll)': 'E(LL)',
    'we': 'WE',
    'x': 'X',
    'r': 'R'
}

controls = dbc.Card([
        html.Div([ # ship selection
                dbc.Label("CVN"),
                dcc.Dropdown(
                    ship_options, 'All Ships', id='ship-select')]),

        html.Div([ # feature selection
                dbc.Label("Job Maintenance Feature"),
                dcc.Dropdown(feature_options, 'Compartment Usage',
                    id="features-selection")]),

        html.Div([ # scatter plot point magnitude
                dbc.Label("Point Magnitude"),
                dcc.Dropdown(['None', 'Days Open', 'Total Material Cost', 'Total Ship Force Man Hours'], 
                               'Total Material Cost', id='point-size')]),

        html.Div([ # type of view
                dbc.Label("View"),
                dbc.RadioItems(
                    ['Top', 'Front', 'Side', '3D'], 'Side', id='view', inline=True)]),

        html.Div([ # date range
                dbc.Label("Date Range"),
                dcc.DatePickerRange(id='date-range', min_date_allowed=date(2017, 11, 1),
                                    max_date_allowed=date(2022, 6, 16), initial_visible_month=date(2018, 8, 5),
                                    start_date=date(2017, 11, 1),
                                    end_date=date(2022, 6, 16))])
    ], body=True)

text_card = dbc.Card([
        dbc.Label("Compartment Summary"),
        html.Pre(id="click-dump")], body=True)

controls2 = dbc.Card([
        html.Div([
            dbc.Label("Variable"),
            # feature
            dbc.RadioItems(['Total Material Cost', 'Days Open'], 'Total Material Cost', id='bar-selection'),
            dbc.Label("Statistics"),
            # statistics
            dbc.RadioItems(['Mean', 'Sum'], 'Mean', id='stat-selection')])
    ])

app.layout = dbc.Container([
        html.H1("Navy CVN HVAC Maintenance Dashboard"),
        html.Hr(),
        html.H2("Geo"),

        # -----------------------------------------------
        dbc.Row([
                dbc.Col(controls, md=2),
                dbc.Col(dcc.Graph(id="geo-graph"), md=5)
                
            ], align='center'),

        # -----------------------------------------------
        dbc.Row([
            dbc.Col(text_card, width={'size': 10,'order': 3, 'offset':0}, align='center')
            ], align='center'),
        
        # -----------------------------------------------
        dbc.Row([
            dbc.Col(dcc.Graph(id='pie-chart'), md=1),
            #dbc.Col(text_card, width={'size': 7,'order': 3, 'offset':4})
            ], align='center'),
        
        #------------------------------------------------
        html.Hr(),
        html.H2("Other Statistics"),
        dbc.Row([
                dbc.Col(controls2, md=1),
                dbc.Col(dcc.Graph(id='graph2'), md=3)
            ], align='center')

    ], fluid=True)


@app.callback(
    Output("geo-graph", "figure"),
    Output("pie-chart", "figure"),  
    Input("ship-select", "value"),
    Input("features-selection", "value"),
    Input("view", "value"),
    Input("point-size", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"))
def update_graphs(ship, feature, view, point_size, start_date, end_date):

    dff = df

    # SUBSET DATAFRAME BASED ON SELECTIONS ===============================
    # ship
    if ship != 'All Ships':
        dff = dff.loc[dff['ship'] == ship_name[ship]]
    
    # remove duplicate jobs and currently open jobs
    dff = dff.drop_duplicates(subset=['job_seq'])
    #dff = dff.loc[dff['job_status'] == 'closed']

    # date range
    if start_date != None:
        dff = dff.loc[pd.to_datetime(dff['date_maintenance_action']) >= start_date]
    dff = dff.loc[pd.to_datetime(dff['date_closing']) <= end_date]

    # PREP AXES =========================================================
    # centerline
    dff['Centerline (Distance)'] = pd.to_numeric(dff['Centerline (Distance)'], errors='coerce')
    dff = dff[dff['Centerline (Distance)'] != 'na']
    # create sorted list of centerline variable to ship [evens,..., 0,...,odds]
    center = [0]
    center_n = (pd.to_numeric(dff['Centerline (Distance)'], errors='coerce')).dropna()
    for item in range(center_n.min(), center_n.max() + 1):
        if item % 2 == 0: # even numbers to the right of centerline (0), odd numbers to the left
            center.append(item)
        else:
            center.insert(0, item)

    # frame
    # get range of frame variable to ship into a list
    frame = pd.to_numeric(dff['Frame'], errors='coerce')
    frame = frame.dropna()
    frame_axis = [item for item in range(frame.min(), frame.max() + 1)]

    # deck
    dff = dff[dff['Deck'] != 'os4']
    deck = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '01', '02', 
            '03', '04', '05', '06', '07', '08', '09', '010', '011']

    # SETUP GRAPHS =======================================================
    geo_title = f"Scatterplot of Maintenance Jobs by Location within {ship} (Color: {feature}, Point Magnitude: {point_size})"
    geo_scatter = px.scatter()
    feature_color = dict(zip(dff[str(columns[feature])].unique(), px.colors.qualitative.G10))

    # point magnitude is tailored based on feature for better interpretability
    point_size_max = None
    if point_size == 'None':
        point_size = None
    elif point_size == 'Days Open':
        point_size = 'days_open'
        point_size_max = 30
    elif point_size == 'Total Material Cost':
        point_size = 'totMaterialCost'
        point_size_max = 50
    elif point_size == 'Total Ship Force Man Hours':
        point_size = 'total_ship_force_man_hours'
        point_size_max = 50

    if view == 'Front': # centerline x deck -------------------------------------------------------------

        geo_scatter = px.scatter(dff, x='Centerline (Distance)', y='Deck', hover_data=['csmp_narrative_summary'],
        height=600, width=1200, color=columns[feature], color_discrete_map=feature_color, size=point_size, size_max=point_size_max,
        title=geo_title,
        labels={'Centerline (Distance)': 'Distance from Centerline', 'Deck': 'Deck (By Level)'})

        # fix axis labels
        geo_scatter.update_xaxes(type='category', categoryorder='array', categoryarray=center, range=[0, 25])
        geo_scatter.update_yaxes(type='category', categoryorder='array', categoryarray=deck)

        geo_title += " - Front View" # graph title
        image_source = Image.open(r'Archive\Modeling\Interactive Dashboard\cvn69-front.png') # add background image
        geo_scatter.add_layout_image(dict(source=image_source, xref="x", x=1, yref="y", y=32, sizex=18,
                                    sizey=35, sizing="stretch", opacity=0.1, layer="below"))

    elif view == 'Side': # frame x deck ----------------------------------------------------------------

        geo_scatter = px.scatter(dff, x='Frame', y='Deck', hover_data=['csmp_narrative_summary'],
        height=500, width=2000, color=columns[feature], color_discrete_map=feature_color, size=point_size, size_max=point_size_max,
        title=geo_title)

        # fix axis labels
        geo_scatter.update_xaxes(categoryorder='array', categoryarray=frame_axis[::-1], range=[-10, 300])
        geo_scatter.update_yaxes(type='category', categoryorder='array', categoryarray=deck, range=[0, 25])

        geo_title += " - Right-Side View" # graph title
        image_source = Image.open(r'Archive\Modeling\Interactive Dashboard\CVN68-side.png') # add background image
        geo_scatter.add_layout_image(dict(source=image_source, xref="x", x=-2, yref="y", y=32, sizex=270,
                                          sizey=35, sizing="stretch", opacity=0.15, layer="below"))
        
    elif view == 'Top': # top - frame x centerline -----------------------------------------------------

        geo_scatter = px.scatter(dff, x='Frame', y='Centerline (Distance)', hover_data=['csmp_narrative_summary'],
        height=800, width=1800, color=columns[feature], color_discrete_map=feature_color, size=point_size, size_max=point_size_max,
        title=geo_title,
        labels={'Frame': 'Frame Number (Bow - Stern)', 'Centerline (Distance)': 'Distance from Centerline'})

        # fix axis labels
        geo_scatter.update_xaxes(categoryorder='array', categoryarray=frame_axis[::-1], range=[-10, 280])
        geo_scatter.update_yaxes(type='category', categoryorder='array', categoryarray=center, range=[0, 25])

        geo_title += " - Top View" # graph title
        image_source = Image.open(r'Archive\Modeling\Interactive Dashboard\CVN68-top.png') # add background image
        geo_scatter.add_layout_image(dict(source=image_source, xref="x", x=0, yref="y", y=18, sizex=280,
                                          sizey=16, sizing="stretch", opacity=0.15, layer="below"))
        
    else: # 3D - view ---------------------------------------------------------------------------------
        point_size_max3d = None
        if point_size == 'days_open':
            point_size_max3d = 20
        elif point_size == 'totMaterialCost':
            point_size_max3d = 60
        elif point_size == 'total_ship_force_man_hours':
            point_size_max3d = 100

        geo_scatter = px.scatter_3d(dff, x='Frame', y='Centerline (Distance)', z='Deck', color=columns[feature], 
                                    color_discrete_map=feature_color, size=point_size, size_max=point_size_max3d, title=geo_title,
                                    hover_data=['csmp_narrative_summary'], height=1000, width=1800)
        
        camera = dict(up = dict(x=0, y=0, z=1),
                      center = dict(x=0, y=0, z=0),
                      eye = dict(x=30, y=-100, z=10))

        # organize axis labels
        geo_scatter.update_layout(scene = dict(
            xaxis = dict(categoryorder='array', categoryarray=frame_axis[::-1], nticks=200, range=[-10, 280]),
            yaxis = dict(type='category', categoryorder='array', categoryarray=center, range=[0, 25]),
            zaxis = dict(type='category', categoryorder='array', categoryarray=deck, range=[0, 25]),
            aspectmode="manual", aspectratio=dict(x=100,y=30,z=20)),
            scene_camera=camera)
        
        
        geo_title += " - 3D View" 
        
    # -------------------------------------------------------------------------------------------------

    # set up pie chart
    pie_chart = px.pie(dff, names=columns[feature], color=columns[feature], color_discrete_map=feature_color, height=400, width=1000,
                       title=f"Percentage of Jobs by {feature} in {ship} ({dff['job_seq'].count()} Jobs)")
    pie_chart.update_traces(textposition='inside')

    # rewrite legend title and items
    geo_scatter.update_layout(legend_title_text=feature)
    if feature == 'Compartment Usage':
        geo_scatter.for_each_trace(lambda t: t.update(name = usage_dict[t.name]))
        pie_chart.for_each_trace(lambda t: t.update(labels = [usage_dict[name] for name in t.labels]))

    return geo_scatter, pie_chart
    
@app.callback(
        Output("click-dump", "children"),
        Input("ship-select", "value"),
        Input("geo-graph", "clickData"),
        Input("view", "value"),
        Input("point-size", "value"),)
def display_jobs(ship, clickData, view, feature):
    if not clickData or view != "3D":
        raise dash.exceptions.PreventUpdate

    frame = clickData["points"][0]['x']
    centerline = clickData["points"][0]['y']
    deck = clickData["points"][0]['z']

    # subset dataframe to this specific compartment
    compartment_jobs = df.loc[(df["Frame"].str.contains(frame)) & 
                          (df["Centerline (Distance)"].str.contains(str(centerline))) & 
                          (df["Deck"].str.contains(deck))]
    usage = (compartment_jobs['Usage'].iloc[0])
    
    compartment_summary = "All Ships\n"

    if ship != 'All Ships':
        compartment_jobs = compartment_jobs.loc[compartment_jobs['ship'] == ship_name[ship]]
        compartment_summary = f"Ship: {ship}\n"

    # aggregate by job_seq
    compartment_jobs = compartment_jobs.groupby('job_seq').agg(set)
    compartment_dict = compartment_jobs.to_dict('index') # dictionary (job_seq) of dictionaries (other columns)
    # example: get apl of job_seq = js > result = compartment_dict[js]['apl']
 
    summary_title = f"Compartment: {deck}-{frame}-{centerline}-{usage.capitalize()} ({usage_dict[usage]})\nTotal HVAC Jobs: {len(compartment_dict)}\n"
    summary_header = f"{'Job Sequence':<20}{'Date Maintenance Action':<30}{'Equipment':<25}{'CSMP Narrative':<30}{'Days Open':<20}{'Total Material Cost':<25}{'Ship Force Total Man Hours':<20}\n"

    compartment_summary += summary_title + summary_header

    compartment_content = ""
    for job in compartment_dict:
        maint_date = compartment_dict[job]['date_maintenance_action']
        equip_nom = compartment_dict[job]['equipment_nomenclature']
        csmp_narr = compartment_dict[job]['csmp_narrative_summary']

        days_open = compartment_dict[job]['days_open']
        mat_tot = compartment_dict[job]['totMaterialCost']
        man_tot = compartment_dict[job]['total_ship_force_man_hours']

        compartment_content = f'{str(job):<20}{str(maint_date.pop()):<30}{equip_nom.pop():<25}{csmp_narr.pop():<30}{str(days_open.pop()):<20}{str(mat_tot.pop()):<25}{str(man_tot.pop()):<20}\n'
        compartment_summary += compartment_content

    #var = json.dumps(clickData)

    return compartment_summary


@app.callback(
    Output("graph2", "figure"),
    [
        Input("bar-selection", "value"),
        Input("stat-selection", "value")
    ]
)
def update_graph(bar, stat):
    aggregated_dataset = df
    bar_title = ''

    if bar == 'Total Material Cost':
        aggregated_dataset = df.groupby('ship')['totMaterialCost']
        bar_title = 'Total Material Cost by Ship'
    else:
        aggregated_dataset = df.groupby('ship')['days_open']
        bar_title = 'Days Open by Ship'
    
    if stat == 'Mean':
        aggregated_dataset = aggregated_dataset.mean()
        bar_title += " (Mean)"
    else:
        aggregated_dataset = aggregated_dataset.sum()
        bar_title += " (Sum)"
    
    aggregated_dataset = aggregated_dataset.sort_index()

    bargraph = px.bar(aggregated_dataset, height=800, width=900,
                      title=bar_title)

    return bargraph

if __name__ == '__main__':
    app.run(debug=True)
