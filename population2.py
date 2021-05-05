import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.pyplot import figure

st.write(

  """
# Numbers & Concepts 
Hello!

Thanks for showing interest to see this website! We are going 
to have a new look at the **numbers**, and
 ***development & economic***  **  concepts.**  

Searching data is consuming and can be sometime tedious if you don’t know how to filter, plot or download data, here you have 
the easier ways to see and download data 
""")
#You've taken the first step towards being able to gain financial freedom and become your own boss. 

st.markdown(""" 

## Population 
Choose the sectors and dates you want to see the population statitics from the left sidebar, and download the table or chart. 

* **Selection based on:** Regin/country, Development, Income
* **Data source:** [United Nations](https://population.un.org/wpp/Download/Standard/Population/)
""")


#Change layout by search markdown cheatsheet
# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

df = pd.read_csv(r'https://github.com/Hamed-ehia/streamlit-apps/blob/main/WPP2019_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.csv', header=[0], thousands = ' ')
df.columns = df.columns.astype(str)
df = df.rename(columns = {'Region, subregion, country or area':'country'})

# converting strings to numbers
for col in df.loc[:, '1950':'2020']:
  df[col]  = df[col].str.replace(' ', '')
  df[col] = pd.to_numeric(df[col], errors='coerce') # coercing any errors to NaN
df = df.dropna()

st.sidebar.header('User Input Features')
selected_year = st.sidebar.multiselect("Select Year", list(reversed(range(1950,2020))))
selected_year = sorted(selected_year)


selected_year =pd.DataFrame(selected_year)


#Accumulate data in a list, not a DataFrame.  It is always cheaper 
#to append to a python list and then convert it to a DataFrame at the end,
# both in terms of memory and performance.

d=[] #for listing name of columns
for m in range(0,len(selected_year)):
  d.append(str(selected_year.loc[m,0]))

#for slicing the columns values of the chosen list of column names
df_selected_year = (df.loc[:, df.columns.isin(d)])

st.sidebar.header('Population sectors')

sector = df.groupby('Type')
sorted_sector_unique = sorted(df['Type'].unique() )

#Creating table for sector in sidebar
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique)
# The selections is not yet accepted in main window

# Filtering data

df_selected_sector = df.loc[ (df['Type'].isin(selected_sector) ) ]

df_selected_sector

sf1 = df_selected_sector.loc[:, df_selected_sector.columns.isin(df_selected_year)]

sf2= df_selected_sector.loc[:,'country']

#To concatenate DataFrames along column, you can specify the axis parameter as 1 :
sf= pd.concat([sf2, sf1], axis=1)
st.write(sf)
# sf = df_selected_sector.loc[:,df_selected_sector.columns.isin('country' df_selected_year)]
# sf

#st.write(df_selected_sector[df_selected_sector.country=='EUROPE'])

#selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))

# op = st.beta_expander('Optional parameters')
# op.checkbox("Enable Debugging")
# op.radio("Pick your favorite", list(reversed(range(1950,2020))))



# Plotting
def plot_sf(x):
  df = pd.DataFrame(df_selected_sector)
  labels = df.country
#  plt.style.use('ggplot')
  plt.fill_between(df.country, df['2010'], color='skyblue', alpha=0.3)

  x = np.arange(len(labels))  # the label locations
  width = 0.35  # the width of the bars


  fig, ax = plt.subplots()
  rects1 = ax.bar(x - width/2, df['2010'], width, color='skyblue', alpha=0.9)
 # rects2 = ax.bar(x + width/2, dselected_year, width, label='Women')

# Add some text for labels, title and custom x-axis tick labels, etc.
  ax.set_ylabel('Ppulation')
#  ax.set_title('Scores by group and gender')
  ax.set_xticks(x)
  ax.set_xticklabels(labels,rotation=45)
  ax.legend()

  ax.bar_label(rects1, padding=3)
#  ax.bar_label(rects2, padding=3)

  fig.tight_layout()

  # Pad margins so that markers don't get clipped by the axes
  plt.margins(0.09)
# Tweak spacing to prevent clipping of tick-labels
  plt.subplots_adjust(bottom=0.1)
  return st.pyplot(fig)

#num_company = st.sidebar.slider('country', 1, 10)

if st.button('Show Plots'): # if you want to show immidiately without button
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.country):
      plot_sf(i)
    #for i in list(df_selected_sector.country)[:num_company]: #Number of plots not number of selections
        



#st.line_chart(df[['1950']])