import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import numpy as np
import streamlit as st
from matplotlib.pyplot import figure
from PIL import Image
import base64

######################
# Page Title
######################
st.write("""
# Building a blooming world for all.
""")
image = Image.open("C:/Users/IMBS/Downloads/hugh-whyte-J8bU6-tAGy8-unsplash.jpg")

st.image(image, use_column_width=True, caption='Photo by Hugh Whyte on Unsplash')
#Photo by <a href="https://unsplash.com/@opixels?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Hugh Whyte</a> on <a href="https://unsplash.com/s/photos/sustainable-development?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  

st.write("""
# Numbers & Concepts For Development

### Hello!

Thanks for showing interest to see this website! We are going 
to have a new look at the ***numbers & concepts*** in the 
fields of **development & economics**.  


Searching data can be sometimes a time-consuming and tedious 
process, and if you don’t know how to filter, plot, etc., can 
be a complicated task. Here you have easier ways to see and 
download data, and also, be familiar with some concepts in 
economics and development. Let's get started with population data around the world.

""")

st.markdown(""" 

## Population 
Please select the sectors and dates you want to Visualize and Download the population statitics from the left sidebar.
* **Selection based on:** Regin/country, Development, Income
* **Data source:** [United Nations](https://population.un.org/wpp/Download/Standard/Population/)
""")

############# Reading Population data
df = pd.read_csv(r"C:\Users\IMBS\Downloads\programming\Data\pop_data\WPP2019_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.csv", header=[0], thousands = ' ', encoding='latin-1')
df.columns = df.columns.astype(str)
df = df.rename(columns = {'Region, subregion, country or area':'country'})

# converting strings to numbers
for col in df.loc[:, '1950':'2020']:
  df[col]  = df[col].str.replace(' ', '')
  df[col] = pd.to_numeric(df[col], errors='coerce') # coercing any errors to NaN
df = df.dropna()

############# Reading Population growth rate data
gf = pd.read_csv(r"C:\Users\IMBS\Downloads\programming\Data\pop_data\WPP2019_POP_F02_POPULATION_GROWTH_RATE.csv", header=[0], thousands = ' ', encoding='latin-1')
gf.columns = gf.columns.astype(str)
#gf = gf.rename(columns = {'Region, subregion, country or area':'country'})


# converting strings to numbers
for col in gf.loc[:, '1950-1955':'2015-2020']:
  gf[col]  = gf[col].str.replace(' ', '')
  gf[col] = pd.to_numeric(gf[col], errors='coerce') # coercing any errors to NaN
gf = gf.dropna()

st.sidebar.header('User Input Features')

selected_topic = st.sidebar.selectbox("Select Topic", ('Population', 'Population Growth Rate'))

if (selected_topic == 'Population'):
  
  st.sidebar.header('World Population Prospects 2019:')
  st.sidebar.write(' Total population (both sexes combined) by region, subregion and country, annually for 1950-2100 (thousands)')
  selected_year = st.sidebar.multiselect("Select Year", list(reversed(range(1950,2020))))
  selected_year = sorted(selected_year)


  selected_year =pd.DataFrame(selected_year)


  #Accumulate data in a list, not a DataFrame.  It is always cheaper 
  #to append to a python list and then convert it to a DataFrame at the end,
  # both in terms of memory and performance, so:


  year=[] #for listing name of columns
  for m in range(0,len(selected_year)):
    year.append(str(selected_year.loc[m,0]))

  #for slicing the columns values of the chosen list of column names
  df_selected_year = (df.loc[:, df.columns.isin(year)])

  sector = df.groupby('Type')
  sorted_sector_unique = sorted(df['Type'].unique() )

  #Creating table for sector in sidebar
  selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique)
  # The selections is not yet accepted in main window

  # Filtering data
  df_selected_sector = df.loc[ (df['Type'].isin(selected_sector) ) ]
  #st.dataframe(df_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)


  sf1 = df_selected_sector.loc[:, df_selected_sector.columns.isin(df_selected_year)]

  sf2= df_selected_sector.loc[:,'country']


  if (selected_sector):

    # Table of data
     #To concatenate DataFrames along column, you can specify the axis parameter as 1 :
     sf= pd.concat([sf2, sf1], axis=1)
     st.write('Summary table for the population of ( or based on); ',  ", ".join(selected_sector) ,'in years: ', " - ".join(year) )
    # st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.10}"), height=300)
     st.write(sf)

     def filedownload(df):
         csv = df.to_csv(index=False)
         b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
         href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
         return href

     st.markdown(filedownload(sf), unsafe_allow_html=True)

     # sft = (sf.T)
     # sft.columns = sft.iloc[0]
     # sft.drop(sft.index[0], inplace = True)
     # st.write('sft',sft)
     # st.write('sft11',sft)

     #st.line_chart(sf.T)

     # Plotting Line chart

     x = np.arange(len(year))  # the label locations
     width = 0.35  # the width of the bars
     curve=[]
     fig, ax = plt.subplots()
     for m in  range(0,len(sf)-1):
      curve.append(ax.plot(x, sf.iloc[m,1:], label= str(sf.iloc[m,0]).format(i=m)))

     ax.set_ylabel('Population')
     ax.set_title('Population over years')
     ax.set_xticks(x)
     ax.set_xticklabels(year,rotation=0)
     ax.legend(fontsize=7)

     fig.tight_layout()

      # Pad margins so that markers don't get clipped by the axes
     plt.margins(0.09)
    # Tweak spacing to prevent clipping of tick-labels
     plt.subplots_adjust(bottom=0.1)
     st.pyplot(fig)
     
   

# Plotting bar chart
     x = np.arange(len(year))  # the label locations
     width = 0.35  # the width of the bars
     curv=[]
     fig1, yx = plt.subplots()
     
     for n in range(0,len(sf)-1):
      curv.append(yx.bar(x - width/2, sf.iloc[n,1:], width, label= str(sf.iloc[n,0])))
     
     yx.set_ylabel('Population')
     yx.set_title('Population over years')
     yx.set_xticks(x)
     yx.set_xticklabels(year,rotation=0)
     yx.legend(fontsize=7)
     #yx.bar_label(x, padding=3)
     fig1.tight_layout()
     plt.margins(0.09)
     plt.subplots_adjust(bottom=0.1)
     st.pyplot(fig1)
    
  
 

  # # num_company = st.sidebar.slider('country', 1, 10)

  # #     if st.button('Show Plots'): # if you want to show with button
  # #         st.header('Stock Closing Price')
  # #         for i in list(df_selected_sector.country)[:num_company]: #Number of plots not number of selections:
  # #           plot_sf(i)

        
elif (selected_topic == 'Population Growth Rate'):
    

    st.sidebar.header('World Population Prospects 2019:')
    st.sidebar.write('Average annual rate of population change by region, subregion and country, 1950-2100 (percentage)')

    # Selectin time period for showing population growth rate
    selected_year_range = st.sidebar.multiselect("Select Time Period", list(list(gf.loc[:, '1950-1955':'2015-2020'])))
    selected_year_range = sorted(selected_year_range)

    # year_range=[] #for listing name of columns
    # for m in range(0,len(selected_year_range)):
    #   year_range.append(str(selected_year_range.loc[m,0]))
    # st.write('selected_year_range', year)

    #for slicing the columns values of the chosen list of column names
    gf_selected_year = (gf.loc[:, gf.columns.isin(selected_year_range)])


    # Selecting sectors
    sector = gf.groupby('Type')
    sorted_sector_unique = sorted(gf['Type'].unique() )

    #Creating table for sector in sidebar
    selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique)

    # Filtering data
    gf_selected_sector = gf.loc[ (gf['Type'].isin(selected_sector) ) ]
    #st.dataframe(df_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)

    #" Creating dataframe of selected features"
    sf1 = gf_selected_sector.loc[:, gf_selected_sector.columns.isin(selected_year_range)]

    sf2= gf_selected_sector.loc[:,'Region, subregion, country or area']


    if (selected_sector):
    #To concatenate DataFrames along column, you can specify the axis parameter as 1 :
       sf= pd.concat([sf2, sf1], axis=1)
       st.write('Summary table for the population growth rate of(or based on); ',  ", ".join(selected_year_range) ,'in time period: ', " - ".join(selected_year_range) )
       st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.10}"), height=300)
    
    

    def filedownload(df):
         csv = df.to_csv(index=False)
         b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
         href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
         return href

    st.markdown(filedownload(sf), unsafe_allow_html=True)



    # Plotting
    x = np.arange(len(selected_year_range))  # the label locations
    width = 0.35  # the width of the bars
    curve=[]
    fig, ax = plt.subplots()
    for m in  range(0,len(sf)-1):
     curve.append(ax.plot(x, sf.iloc[m,1:], label= str(sf.iloc[m,0]).format(i=m)))

    ax.set_ylabel('Population')
    ax.set_title('Population over years')
    ax.set_xticks(x)
    ax.set_xticklabels(selected_year_range,rotation=0)
    ax.legend(fontsize=7)

    fig.tight_layout()

      # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.09)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.1)
    st.pyplot(fig)
     

# Plotting bar chart
    x = np.arange(len(selected_year_range))  # the label locations
    width = 0.35  # the width of the bars
    curv=[]
    fig1, yx = plt.subplots()
     
    for n in range(0,len(sf)-1):
     curv.append(yx.bar(x - width/2, sf.iloc[n,1:], width, label= str(sf.iloc[n,0])))
     
    yx.set_ylabel('Population')
    yx.set_title('Population over years')
    yx.set_xticks(x)
    yx.set_xticklabels(selected_year_range,rotation=0)
    yx.legend(fontsize=7)
     #yx.bar_label(x, padding=3)
    fig1.tight_layout()
    plt.margins(0.09)
    plt.subplots_adjust(bottom=0.1)
    st.pyplot(fig1)