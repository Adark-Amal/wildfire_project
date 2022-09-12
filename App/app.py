import streamlit as st
from streamlit_option_menu import option_menu
import io 
import pickle
import bz2file as bz2

from dashboard_viz import *
from DBconnect import *



# setting page layout
st.set_page_config(page_title='Wildfire Dashboard', layout='wide')

if 'load_data' not in st.session_state:
    st.session_state.load_data = False


# create instances of class
sv = SimpleViz()
dc = database_conn()


## Function that loads the data
@st.cache(suppress_st_warning=True)
def platform_data():
    get_conn = dc.create_connection(db_file = "../Data/Fire.db")
    fire_data =  dc.get_data(conn = get_conn, table = 'cleaned_fires')

    return fire_data


# maintain the state of the app after changes to code
if st.session_state.load_data:
    st.session_state.load_data = True

# load platform data
wildfire = platform_data()






#-----------------------------------------------------------------------------------------------------------------------------
# SIDEBAR MENU
#-----------------------------------------------------------------------------------------------------------------------------

# creating the sidebar menu
st.sidebar.image('../Images/canonical.png', width=300)
st.sidebar.markdown('##')

with st.sidebar:
    choose = option_menu("Wildfire Platform", ["Home", "Dashboard", "ML Platform"],
                         icons=['building', 'graph-up-arrow', 'cash-coin'],
                         menu_icon="menu-app", default_index=0,
                         styles={"nav-link": {"--hover-color": "#7c355d"}, "nav-link-selected": {"background-color": "#7c355d"}}
                        )










#------------------------------------------------------------------------------------------------
# MAIN CANVAS
#------------------------------------------------------------------------------------------------


if choose == "Home":    
    st.markdown("<h2 style='text-align:center;text-decoration:underline;text-underline-offset:0.3em;text-decoration-color:#7c355d;'>About Wildfire Project</h2>", unsafe_allow_html=True)   
    
    st.markdown('#')

    st.subheader('Context')
    st.markdown('<p style="text-align:justify;">This data publication contains a spatial database of wildfires that occurred in the United \
            States from 1992 to 2015.It is the third update of a publication originally generated to support the national Fire Program \
            Analysis (FPA) system.The wildfire records were acquired from the reporting systems of federal, state, and local fire \
            organizations. The following core data elements were required for records to be included in this data publication: discovery \
            date, final fire size, and a point location at least as precise as Public Land Survey System (PLSS) section (1-square mile grid).\
            The data were transformed to conform, when possible, to the data standards of the National Wildfire Coordinating Group (NWCG).\
            Basic error-checking was performed and redundant records were identified and removed, to the degree possible.\
            The resulting product, referred to as the Fire Program Analysis fire-occurrence database (FPA FOD), includes 1.88 million \
            geo-referenced wildfire records, representing a total of 140 million acres burned during the 24-year period.</p>',
            unsafe_allow_html=True)

    st.markdown('##')
    
    st.subheader('Problem Statement')
    st.markdown('<p style="text-align:justify;">Forest fires and wildfires are natural disasters that continue to make national \
                and global news, including the recent nationwide fires that killed over a billion animals in Australia. \
                Such fires can be very difficult to predict as many different random events like lightning, electrical failures,\
                smoking, or arson are potential causes. Due to the unfortunate circumstances surrounding these fires, they\'re often \
                difficult to contain, and can end up costing governments millions of dollars in relief, as well as the tragic loss \
                of the humans, fauna, and flora.</p>', unsafe_allow_html=True)

    st.markdown('##')

    st.subheader('Project Goals')
    st.write('In this project, I seek to achieve the following goals;')
    st.markdown('* Understand how wildfires have evolved over time \
                \n* Determine which states and counties are fire prone \
                \n* Predict the likely causes of wildfires given size, location and date.')

    st.markdown('##')

    st.subheader('Reference and Acknoledgement')

    st.markdown('* [Scikit Learn Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html)\
                \n* [Machine Learning Mastery](https://machinelearningmastery.com/extra-trees-ensemble-with-python/) \
                \n* [Yellowbrick Library](https://www.scikit-yb.org/en/latest/) \
                \n* [Data Science Infinity DS Templates](https://data-science-infinity.teachable.com/) \
                \n* [Data Science Blog](https://www.reneshbedre.com/blog/anova.html) \
                \n* [Plotly Python Graph Library](https://plotly.com/python/) \
                \n* [Kaggle Wildfire Data](https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires?resource=download)', 
                unsafe_allow_html=True)










#------------------------------------------------------------------------------------------------------------------------------
# DASHBOARD
#-----------------------------------------------------------------------------------------------------------------------------

if choose == "Dashboard":
    
    col1, col2, col3 = st.columns([1, 3, 1])

    # with col2:
    st.markdown("<h2 style='text-align:center;text-decoration:underline;text-underline-offset:0.3em;text-decoration-color:#7c355d;'>Wildfire Dashboard</h2>", unsafe_allow_html=True )
    
    st.markdown('##')
    st.markdown('##')
    st.markdown('##')


    # -------------------------------------------------------------------------
    # KPI AND FILTERING
    # -------------------------------------------------------------------------

    # defining filters
    col1, col2, col3 = st.columns([0.5, 3, 1])
    year = sorted(wildfire['FIRE_YEAR'].unique())

    with col1:
        st.markdown('<h5 style="color:#7c355d;"> Filters </h5>', unsafe_allow_html=True)
        condition = st.checkbox(label='All', value=True)
    with col2:
        state = st.multiselect(label="Select State:", options=wildfire['STATE'].unique(), default=wildfire['STATE'].unique()[0])
    with col3:
        year = st.selectbox(label='Select Year', options=year)


    # select data based on filter
    if condition == True:
        filtered_data = wildfire.iloc[:]

    if condition == False:
        filtered_data = wildfire.query("STATE==@state & FIRE_YEAR==@year")


    st.markdown('##')
    st.markdown('##')
    st.markdown('##')


    # --------------------------------------------------------------------------------
    # DISPLAYING KPIS
    # ----------------------------------------------------------------------------------

    total_occurrence = filtered_data.shape[0]
    average_fire_size = round(filtered_data['FIRE_SIZE'].mean(), 1)
    wildfire_cause = filtered_data['STAT_CAUSE_DESCR'].value_counts().index

    # arrangng KPIs on dashboard
    left_col, middle_col, right_col = st.columns(3)

    with left_col:
        st.markdown('<h2 style="color:#7c355d;"> Total Occurrence</h2>', unsafe_allow_html=True)
        st.markdown(f'<h4> {total_occurrence:,} </h4>', unsafe_allow_html=True)

    with middle_col:
        st.markdown('<h2 style="color:#7c355d;"> Average Fire-size </h2>', unsafe_allow_html=True)
        st.markdown(f'<h4> {average_fire_size} acres </h4>', unsafe_allow_html=True)

    with right_col:
        if len(wildfire_cause) > 0:
            st.markdown('<h2 style="color:#7c355d;"> Top Cause</h2>', unsafe_allow_html=True)
            st.markdown(f'<h4> {wildfire_cause[0]} </h4>', unsafe_allow_html=True)
        else:
            st.markdown('<h2 style="color:#7c355d;"> Top Cause</h2>', unsafe_allow_html=True)
            st.markdown(f'<h4> No cause </h4>', unsafe_allow_html=True)

    st.markdown("""---""")

    st.markdown('##')
    st.markdown('##')
    st.markdown('##')


    # ------------------------------------------------------------------------------------------------------------
    # DISPLAY VISUALIZATIONS
    # ------------------------------------------------------------------------------------------------------------

    col1, col2, col3 = st.columns([2, 0.5, 2])

    # Question 1: Total fire occurrence per state
    map_data = filtered_data[['OBJECTID', 'STATE', 'FIRE_SIZE', 'FIRE_YEAR']]
    state_count = pd.DataFrame(map_data.groupby(['STATE','FIRE_YEAR'])['OBJECTID'].count())
    state_count.columns = ['Count']
    state_count.reset_index(inplace=True)


    # Question 2: Average fire-size per state
    avg_state_size = pd.DataFrame(filtered_data.groupby(['STATE','FIRE_YEAR'])['FIRE_SIZE'].mean())
    avg_state_size.columns = ['Average']
    avg_state_size.reset_index(inplace=True)


    # Question 3: Average fire-size per month 
    spread_data = filtered_data[['FIRE_MONTH', 'FIRE_SIZE']]
    avg_fire_spread = pd.DataFrame(spread_data.groupby('FIRE_MONTH')['FIRE_SIZE'].mean()).reset_index()

    ordered_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # sorting data accoring to ordered_months
    avg_fire_spread['to_sort']=avg_fire_spread['FIRE_MONTH'].apply(lambda x:ordered_months.index(x))
    avg_fire_spread = avg_fire_spread.sort_values('to_sort')
    avg_fire_spread.columns = ['Month', 'Average Fire-size', 'Sorter']


     # Question 4: Total fire occurrence per month
    month_count = pd.DataFrame(spread_data['FIRE_MONTH'].value_counts()).reset_index()
    month_count.columns = ['Month', 'Count']

    # sorting data accoring to ordered_months
    month_count['to_sort']=month_count['Month'].apply(lambda x:ordered_months.index(x))
    month_count = month_count.sort_values('to_sort')


     # Question 5: Total wildfire causes
    cause_data = pd.DataFrame(filtered_data['STAT_CAUSE_DESCR'].value_counts()).reset_index()
    cause_data.columns = ['Cause', 'Count']


    # Question 6: Average damage per fire cause
    cause_size = filtered_data[['FIRE_SIZE', 'STAT_CAUSE_DESCR']]
    avg_cause_size = pd.DataFrame(cause_size.groupby('STAT_CAUSE_DESCR')['FIRE_SIZE'].mean()).reset_index()
    avg_cause_size.sort_values(by='FIRE_SIZE', ascending=False, inplace=True)


    with col1:
        st.plotly_chart(sv.us_map(state_count,'STATE','Count', 'Total Wildfire Occurrence Per State'), use_container_width=True)
        st.markdown('#')
        st.markdown('#')
        st.plotly_chart(sv.line(avg_fire_spread,"Month", "Average Fire-size", title='Average Fire Size Per Month'), use_container_width=True)
        st.markdown('#')
        st.markdown('#')
        st.plotly_chart(sv.Hbar(cause_data, 'Count', 'Cause', 'Count', title='Causes of Wildfires'), use_container_width=True)
    with col3:    
        st.plotly_chart(sv.us_map(avg_state_size,'STATE','Average', 'Average Fire-size Per State'), use_container_width=True)
        st.markdown('#')
        st.markdown('#')
        st.plotly_chart(sv.line(month_count,"Month", "Count", title='Total Occurrence Per Month'), use_container_width=True)
        st.markdown('#')
        st.markdown('#')
        st.plotly_chart(sv.Hbar(avg_cause_size, 'FIRE_SIZE', 'STAT_CAUSE_DESCR', 'FIRE_SIZE', title='Average Fire size Per Cause'), use_container_width=True)












# -----------------------------------------------------------------------------------------------------------------------------------
# ML PlATFORM
# -----------------------------------------------------------------------------------------------------------------------------------


if choose == 'ML Platform':

    st.markdown("<h2 style='text-align:center;text-decoration:underline;text-underline-offset:0.3em;text-decoration-color:#7c355d;'>Wildfire Cause Prediction</h2>", unsafe_allow_html=True )
    
    st.markdown('##')
    st.markdown('##')
    st.markdown('##')

    tab1, tab2, tab3 = st.tabs(["Focus Prediction", "Batch Prediction", "Monitoring"])

    # ------------------------------------------------------------------------------------------
    # Focus Prediction
    # ------------------------------------------------------------------------------------------
    with tab1:
        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            year = sorted(wildfire['FIRE_YEAR'].unique())
            ordered_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

            # take input from user for prediction
            form = st.form(key='my_form', clear_on_submit=True)
            fire_year = form.selectbox('Fire Year', year)
            fire_month = form.selectbox('Fire Month', ordered_months)
            fire_size = form.number_input(label='Size (Acres)', min_value=0)
            latitude = form.number_input(label='Latitude', format="%d", min_value=-180)
            longitude = form.number_input(label='Longitude', format="%d", min_value=-180)
            state = form.selectbox('State', wildfire['STATE'].unique())
            form.markdown('##')
            submit_button = form.form_submit_button(label='Submit')

            # once user clicks on submit
            if submit_button:

                # get the data user inputted
                d = {'FIRE_YEAR':[fire_year], 'FIRE_MONTH':[fire_month],'FIRE_SIZE': [fire_size], 
                    'LATITUDE':[latitude], 'LONGITUDE':[longitude], 'STATE':[state]}

                # create a dataframe and display it
                data = pd.DataFrame(data=d)
                d2 = {'Details': data.columns, 'Input Data':data.iloc[0]}
                new_data = pd.DataFrame(data=d2)
                new_data.set_index('Details', inplace=True)

                st.markdown('##')

                # data visualization in table form
                st.markdown("<p style='color:#7c355d; font-family:Verdana;'>Input Data</p>", unsafe_allow_html=True)
                fig = ff.create_table(new_data, colorscale=[[0, "#7c355d"], [.5, '#DBD5E6'],[1, '#ffffff']], index=True, index_title='Wildfire Details')
                for i in range(len(fig.layout.annotations)):
                    fig.layout.annotations[i].font.size = 18

                st.plotly_chart(fig, use_container_width=True)


                st.markdown('##')

                # load the trained model
                st.markdown("<p style='color:#7c355d; font-family:Verdana;'>Predicted Output</p>", unsafe_allow_html=True)
                def pred_model(file):

                    model_handler = bz2.BZ2File(file, 'rb')
                    model = pickle.load(model_handler)
    

                    # define names for columns
                    pred_columns = ['Wildfire Cuase']
                    
                    # make prediction 
                    y_pred = model.predict(data)
                    y_pred_prob = model.predict_proba(data)
                    classes = model.classes_

            
                    output_df = pd.DataFrame(y_pred, columns=pred_columns)
                    prob_df = pd.DataFrame(y_pred_prob, columns=classes).T
                    prob_df.reset_index(inplace=True)
                    prob_df.columns = ['Causes', 'Probabilities']
                    
                    
                    d3 = {'Wildfire Details': output_df.columns, 'Predicted Cause': output_df.iloc[0]}

                    final = pd.DataFrame(data=d3)
                    final.set_index('Wildfire Details', inplace=True)
                    
                    return final, prob_df


                # display predicted output
                pred_data, prob_data = pred_model('../Model/finalize_model.pbz2')

                # data visualization
                fig = ff.create_table(pred_data, colorscale=[[0, "#7c355d"], [.5, '#e5fddc'],[1, '#ffffff']], index=True, index_title='Wildfire Details')
                for i in range(len(fig.layout.annotations)):
                    fig.layout.annotations[i].font.size = 18

                st.plotly_chart(fig, use_container_width=True)

                # plot probabilitiees
                st.markdown('##')
                st.markdown('##')
                st.markdown("<p style='color:#7c355d; font-family:Verdana;'>Predicted Outcomes</p>", unsafe_allow_html=True)
                st.markdown('#')
                st.plotly_chart(sv.Vbar(prob_data, 'Causes', 'Probabilities', 'Probabilities', title='Probabilities of Wildfire Causes'), use_container_width=True)
                
                




    # ---------------------------------------------------------------------------------------------------------------
    # Batch Prediction
    # ---------------------------------------------------------------------------------------------------------------
    with tab2:
        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            def file_upload(name):
                uploaded_file = st.file_uploader('%s' % (name),key='%s' % (name), accept_multiple_files=False)
                content = False
                if uploaded_file is not None:
                    try:
                        uploaded_df = pd.read_csv(uploaded_file)
                        content = True
                        return content, uploaded_df
                    except:
                        try:
                            uploaded_df = pd.read_excel(uploaded_file)
                            content = True
                            return content, uploaded_df
                        except:
                            st.error('Please ensure file is .csv or .xlsx format and/or reupload file')
                            return content, None
                else:
                    return content, None

            st.markdown('##')

            # define template file to be uploaded
            st.markdown("<p style='color:#7c355d;font-family:Verdana;font-size:1em;'> Please upload batch input data for wildfires.\
                            See template below (.xlsx or .csv)</p>", unsafe_allow_html=True)

            # upload file in csv or excel format
            status, df = file_upload(" ")

            st.markdown('##')

            # once user clicks submit
            if st.button('Submit'):

                # make prediction
                def pred_model(file):
                    
                    model_handler = bz2.BZ2File(file, 'rb')
                    model = pickle.load(model_handler)

                    # define names of columns
                    pred_columns = ['Wildfire Cuase']

                    # make predictions 
                    y_pred = model.predict(df)
                    y_pred_prob = model.predict_proba(df)
                    classes = model.classes_

                    
                    # creating dataframe
                    output_df = pd.DataFrame(y_pred, columns=pred_columns)
                    prob_df = pd.DataFrame(y_pred_prob, columns=classes)

                    # join input data to output data
                    result = pd.concat([df, output_df], axis=1, join='inner')
                    result = pd.concat([result, prob_df], axis=1, join='inner')

                    # set custom index range for dataframe
                    #new_index = [str(i).zfill(6) for i in range(1, result.shape[0]+1)]
                    #result.index = new_index

                    return result
                

                st.markdown('##')

                # make predictions and display output
                st.markdown("<p style='color:#7c355d; font-family: Verdana;'>Predicted Output</p>", unsafe_allow_html=True)
                pred_data = pred_model('../Model/finalize_model.pbz2')
                st.dataframe(pred_data)

                st.markdown('##')

                # user can download data here - remember to 'pip install xlsxwriter'
                name = 'fire_cause' + '.xlsx'

                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    pred_data.to_excel(writer, index=True)
                    writer.save()

                st.download_button(label='Download Data', data=buffer, file_name=name, mime='application/vnd.ms-excel')

