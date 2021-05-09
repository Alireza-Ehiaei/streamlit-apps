import pandas as pd
#import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
#from pandas.plotting import register_matplotlib_converters
import numpy as np
import streamlit as st
from matplotlib.pyplot import figure
import base64
from PIL import Image

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

Searching data can be sometimes a time-consuming and tedious process, and filtering, visualizing, and manipulating data can be a 
complicated task. Here you have easier ways to see and download data, and also, be familiar with some concepts in economics and development. Let's get started with data of population around the world.
""")

st.markdown(""" 

## Population 
Please select the sectors and dates you want to Visualize and Download the population statitics from the left sidebar.
* **Selection based on:** regin, development group, income croupe, and country.
* **Data source:** [United Nations](https://population.un.org/wpp/Download/Standard/Population/)
""")

############# Reading Population data
df = pd.read_csv(r"C:\Users\IMBS\Downloads\programming\Data\pop_data\WPP2019_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.csv", header=[0], encoding='latin-1')
df.columns = df.columns.astype(str)
df = df.rename(columns = {'Region, subregion, country or area':'country'})

# converting strings to numbers
for col in df.loc[:, '1950':'2020']:
  df[col]  = df[col].str.replace(' ', '')
  df[col] = pd.to_numeric(df[col], errors='coerce') # coercing any errors to NaN
#df = df.dropna()

############# Reading Population growth rate data

gf = pd.read_csv(r"C:\Users\IMBS\Downloads\programming\Data\pop_data\WPP2019_POP_F02_POPULATION_GROWTH_RATE.csv", header=[0], encoding='latin-1')
gf.columns = gf.columns.astype(str)
gf = gf.rename(columns = {'Region, subregion, country or area':'country'})


# converting strings to numbers

for col in gf.loc[:, '1950-1955':'2015-2020']:
  gf[col]  = gf[col].str.replace(' ', '')
  gf[col] = pd.to_numeric(gf[col], errors='coerce') # coercing any errors to NaN
#gf = gf.dropna()

st.sidebar.header('User Input Features')

selected_topic = st.sidebar.selectbox("Select Topic", ('Population', 'Population Growth Rate'))

s=[]
####################" Work on population

if (selected_topic == 'Population'):
  
  st.sidebar.header('World Population Prospects 2019:')
  st.sidebar.write(' Total population (both sexes combined) by region, subregion and country, annually for 1950-2100 (thousands)')

############# Time selection

  selected_year = st.sidebar.multiselect("Select Year", list(reversed(range(1950,2020))))
  selected_year = sorted(selected_year)

  selected_year = pd.DataFrame(selected_year)

  year=[] #for listing name of columns
  for m in range(0,len(selected_year)):
    year.append(str(selected_year.loc[m,0]))

  #for slicing the columns values of the chosen list of column names
  df_selected_year = (df.loc[:, df.columns.isin(year)])

################ Sector selection

  sector = df.groupby('Type')
  sorted_sector_unique = sorted(df['Type'].unique() )

  sorted_sector_unique1 = list(filter(lambda x: x != 'Country/Area', sorted_sector_unique))
  sorted_sector_unique2 = list(filter(lambda x: x == 'Country/Area', sorted_sector_unique))


  # #Creating table for groupe in sidebar
  if (sorted_sector_unique1):
      selected_sector1 = st.sidebar.multiselect('Groupe/Region', sorted_sector_unique1)

      # Filtering data
      df_selected_sector1 = df.loc[ (df['Type'].isin(selected_sector1) ) ]
      #st.dataframe(df_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)

   # Creating table for country in sidebar
  if (sorted_sector_unique2):
      sorted_country_unique = list(df['country'][df['Type'] == 'Country/Area'])

      selected_sector2 = st.sidebar.multiselect('Country/Area', sorted_country_unique)

      # Filtering data
      df_selected_sector2 = df.loc[ (df['country'].isin(selected_sector2) ) ]
      #st.dataframe(df_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)
      
      df_selected_sector= df_selected_sector1.append(df_selected_sector2)


      #for slicing the columns values of the chosen  years 
      df_selected_year = (df.loc[:, df.columns.isin(year)])
      
  # for slicing the row values of the chosen groupes in chosen years
  sf1 = df_selected_sector.loc[:, df_selected_sector.columns.isin(df_selected_year)]

# names of country in the chosen rows
  sf2= df_selected_sector.loc[:,'country']

  if (selected_sector2) or (selected_sector1):

    # Table of data
     #To concatenate final DataFrames along column for plotting,
     sf= pd.concat([sf2, sf1], axis=1)
     
     #Transpode the table to have better sense
     sft = (sf.T)
     sft.columns = sft.iloc[0]
     sft.drop(sft.index[0], inplace = True)
     
     st.write('Summary table for the population of ',", ".join(selected_sector2) ,  ", ".join(selected_sector1),'in years: ', " - ".join(year) )
     st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.10}"), height=300)
     
     #For downloading csv file
     def filedownload(df):
           csv = df.to_csv(index=True)
           b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
           href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
           return href

     st.markdown(filedownload(sft), unsafe_allow_html=True)
     

####################### Plotting 

     
############## creating button to see and plot data
     if st.button('Plot population over year'):

       def bar_plot(ax, data, colors=None, total_width=0.8, single_width=.5, legend=True):
       #Draws a bar plot with multiple bars per data point.
           
           # Check if colors where provided, otherwhise use the default color cycle
           if colors is None:
               colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

           # Number of bars per group (number of times on x axis)
           n_bars = len(data.T) # len(data) makes error!!
           
          # The width of a single bar groupe (associate to each time on x axis)
           bar_width = total_width / (n_bars)
           
          # List containing handles for the drawn bars, used for the legend
           bars = []

           # Iterate over all data, i is number of bar groupes (associate to each time on x axis)
           for i, (name, values) in enumerate(data.items()):

              # The offset in x direction of that bar          
               x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
              

              # Draw a bar for every value of that type
               for x, y in enumerate(values):

                   bar = ax.bar(x + x_offset, y, width= bar_width * single_width , color=colors[i % len(colors)])
                   ax.bar_label(bar, padding=3, fontsize=5)

            
              # Add a handle to the last drawn bar, which we'll need for the legend
               bars.append(bar[0])
           
           # Draw legend if we need
           if legend:
               ax.legend(bars, data.keys(), fontsize=5)

           ax.set_ylabel('Population')
           ax.set_title('Population over years')

           #number of x-tickets
           ax.set_xticks(np.arange(n_bars))


          #value of x-tickets
           X_Tick_List = []
           X_Tick_Label_List=[]

           for item in range (0,len(sft)):
               X_Tick_List.append(item)
               X_Tick_Label_List.append(str(data.index[item]))
           
           label= X_Tick_Label_List  
           plt.xticks(ticks=X_Tick_List,labels=label, rotation=0,fontsize=8)

           
           #ax.set_xticklabels(list(data.index))
           
       #  Pad margins so that markers don't get clipped by the axes
           plt.margins(0.09)
          # Tweak spacing to prevent clipping of tick-labels
           plt.subplots_adjust(bottom=0.1)

       fig, ax = plt.subplots()
       ax.ticklabel_format(axis="y",useOffset=False,style='plain')

       bar_plot(ax, sft, total_width=.8, single_width= 1)

        #For plotting chart
       st.pyplot(fig)

# Plotting line chart _ against years
       x = np.arange(len(year))  # the label locations
       fig1, yx = plt.subplots()
       
      
      # check if ther is one columd plots scatter instead of lines
       if (len(year)==1):
    
          for n in range(0,len(sf)):
              yx.scatter(x, sft.iloc[0,n], label=str(sf.iloc[n,0])) #, s=area, c=colors, alpha=0.5)
              
          
       else:

          curv=[]
          for n in range(0,len(sf)):
              #yx.scatter(x, sf.iloc[n,1:], label= str(sf.iloc[n,0]))
              curv.append(yx.plot(x , sf.iloc[n,1:], label= str(sf.iloc[n,0])))
         
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


  #Plotting line chart _ against subjects (groups, country..)

     if st.button('Plot population over groupe, region, country or area'):

      def bar_plot(ax, data, colors=None, total_width=0.8, single_width=.5, legend=True):
       #Draws a bar plot with multiple bars per data point.
           
           # Check if colors where provided, otherwhise use the default color cycle
           if colors is None:
               colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

           # Number of bars per group (number of times on x axis)
           n_bars = len(data.T) # len(data) makes error!!
           
          # The width of a single bar groupe (associate to each time on x axis)
           bar_width = total_width / (n_bars)
           
          # List containing handles for the drawn bars, used for the legend
           bars = []

           # Iterate over all data, i is number of bar groupes (associate to each time on x axis)
           for i, (name, values) in enumerate(data.items()):

              # The offset in x direction of that bar          
               x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
              

              # Draw a bar for every value of that type
               for x, y in enumerate(values):

                   bar = ax.bar(x + x_offset, y, width= bar_width * single_width , color=colors[i % len(colors)])
                   ax.bar_label(bar, padding=3, fontsize=5)

            
              # Add a handle to the last drawn bar, which we'll need for the legend
               bars.append(bar[0])
           
           # Draw legend if we need
           if legend:
               ax.legend(bars, data.keys(), fontsize=5)

           ax.set_ylabel('Population')
           ax.set_title('Population over years')

           #number of x-tickets
           ax.set_xticks(np.arange(n_bars))


          #value of x-tickets
           X_Tick_List = []
           X_Tick_Label_List=[]

           for item in range (0,len(sft)):
               X_Tick_List.append(item)
               X_Tick_Label_List.append(str(data.index[item]))
           
           label= X_Tick_Label_List  
           plt.xticks(ticks=X_Tick_List,labels=label, rotation=0,fontsize=8)


           
           #ax.set_xticklabels(list(data.index))
           
       #  Pad margins so that markers don't get clipped by the axes
           plt.margins(0.09)
          # Tweak spacing to prevent clipping of tick-labels
           plt.subplots_adjust(bottom=0.1)

           fig, ax = plt.subplots()
           ax.ticklabel_format(axis="y",useOffset=False,style='plain')

           bar_plot(ax, sft, total_width=.8, single_width= 1)

            #For plotting chart
           st.pyplot(fig)
           
           sf=sf.set_index(sf.columns[0])        

           x = np.arange(len(sf))  # the label locations

           curv=[]
           fig2, ax1 = plt.subplots()

           # check if ther is one columd plots scatter instead of lines
           if (len(sf)==1):

              for n in range(0,len(sft)):
                  ax1.scatter(x, sft.iloc[n,0], label=str(year[n])) #, s=area, c=colors, alpha=0.5)
              
           else:
           
             for n in range(0,len(sft)):
                 curv.append(ax1.plot(x , sft.iloc[n,0:], label= str(year[n])))
           
           ax1.set_ylabel('Population')
           ax1.set_title('Population over subjects')
           ax1.set_xticks(x)
           ax1.set_xticklabels(list(sf.index),rotation=90)
           ax1.legend(fontsize=7)
           #ax1.bar_label(x, padding=3)
           fig2.tight_layout()
           plt.margins(0.09)
           plt.subplots_adjust(bottom=0.1)
           st.pyplot(fig2)


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
    selected_year_range = pd.DataFrame(selected_year_range)

    year_range=[] #for listing name of columns
    for m in range(0,len(selected_year_range)):
      year_range.append(str(selected_year_range.loc[m,0]))

    #for slicing the columns values of the chosen list of column names
    gf_selected_year = (gf.loc[:, gf.columns.isin(selected_year_range)])

################ Sector selection

    sector = gf.groupby('Type')
    sorted_sector_unique = sorted(gf['Type'].unique() )

    sorted_sector_unique1 = list(filter(lambda x: x != 'Country/Area', sorted_sector_unique))
    sorted_sector_unique2 = list(filter(lambda x: x == 'Country/Area', sorted_sector_unique))


    # #Creating table for groupe in sidebar
    if (sorted_sector_unique1):
        selected_sector1 = st.sidebar.multiselect('Groupe/Region', sorted_sector_unique1)
        
        # Filtering data
        gf_selected_sector1 = gf.loc[ (gf['Type'].isin(selected_sector1) ) ]
        #st.dataframe(gf_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)
        
     # Creating table for country in sidebar
    if (sorted_sector_unique2):
        sorted_country_unique = list(gf['country'][gf['Type'] == 'Country/Area'])

        selected_sector2 = st.sidebar.multiselect('Country/Area', sorted_country_unique)
        
        # Filtering data
        gf_selected_sector2 = gf.loc[ (gf['country'].isin(selected_sector2) ) ]
        #st.dataframe(gf_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)
        
        gf_selected_sector= gf_selected_sector1.append(gf_selected_sector2)
        

        #for slicing the columns values of the chosen  years 
        gf_selected_year = (gf.loc[:, gf.columns.isin(year_range)])
        
        

  # for slicing the row values of the chosen groupes in chosen years
    sf1 = gf_selected_sector.loc[:, gf_selected_sector.columns.isin(gf_selected_year)]
    
  # names of country in the chosen rows
    sf2= gf_selected_sector.loc[:,'country']
    
    if (selected_sector2) or (selected_sector1):

      # Table of data
       #To concatenate final DataFrames along column for plotting,
       sf= pd.concat([sf2, sf1], axis=1)
       
       #Transpode the table to have better sense
       sft = (sf.T)
       sft.columns = sft.iloc[0]
       sft.drop(sft.index[0], inplace = True)
       
       st.write('Summary table for the population growth rate of (or based on); ',  ", ".join(selected_sector1),  ", ".join(selected_sector2) ,'in time period: ', " - ".join(year_range) )
       st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.10}"), height=300)
    
    

    def filedownload(gf):
         csv = gf.to_csv(index=True)
         b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
         href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
         return href

    st.markdown(filedownload(sf), unsafe_allow_html=True)

####################### Plotting 

     
############## creating button to see and plot data
    if st.button('Plot population over year'):

       def bar_plot(ax, data, colors=None, total_width=0.8, single_width=.5, legend=True):
       #Draws a bar plot with multiple bars per data point.
           
           # Check if colors where provided, otherwhise use the default color cycle
           if colors is None:
               colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

           # Number of bars per group (number of times on x axis)
           n_bars = len(data.T) # len(data) makes error!!
           
          # The width of a single bar groupe (associate to each time on x axis)
           bar_width = total_width / (n_bars)
           
          # List containing handles for the drawn bars, used for the legend
           bars = []

           # Iterate over all data, i is number of bar groupes (associate to each time on x axis)
           for i, (name, values) in enumerate(data.items()):

              # The offset in x direction of that bar          
               x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
              

              # Draw a bar for every value of that type
               for x, y in enumerate(values):

                   bar = ax.bar(x + x_offset, y, width= bar_width * single_width , color=colors[i % len(colors)])
                   ax.bar_label(bar, padding=3, fontsize=5)

            
              # Add a handle to the last drawn bar, which we'll need for the legend
               bars.append(bar[0])
           
           # Draw legend if we need
           if legend:
               ax.legend(bars, data.keys(), fontsize=5)

           ax.set_ylabel('Population')
           ax.set_title('Population over years')

           #number of x-tickets
           ax.set_xticks(np.arange(n_bars))


          #value of x-tickets
           X_Tick_List = []
           X_Tick_Label_List=[]

           for item in range (0,len(sft)):
               X_Tick_List.append(item)
               X_Tick_Label_List.append(str(data.index[item]))
           
           label= X_Tick_Label_List  
           plt.xticks(ticks=X_Tick_List,labels=label, rotation=0,fontsize=8)

           
           #ax.set_xticklabels(list(data.index))
           
       #  Pad margins so that markers don't get clipped by the axes
           plt.margins(0.09)
          # Tweak spacing to prevent clipping of tick-labels
           plt.subplots_adjust(bottom=0.1)

       fig, ax = plt.subplots()
       ax.ticklabel_format(axis="y",useOffset=False,style='plain')

       bar_plot(ax, sft, total_width=.8, single_width= 1)

        #For plotting chart
       st.pyplot(fig)

# Plotting line chart _ against years
       x = np.arange(len(year_range))  # the label locations
       fig1, yx = plt.subplots()

       
      
      # check if ther is one columd plots scatter instead of lines
       if (len(year_range)==1):
    
          for n in range(0,len(sf)):
              yx.scatter(x, sft.iloc[0,n], label=str(sf.iloc[n,0])) #, s=area, c=colors, alpha=0.5)
              
          
       else:

          curv=[]
          for n in range(0,len(sf)):
              #yx.scatter(x, sf.iloc[n,1:], label= str(sf.iloc[n,0]))
              curv.append(yx.plot(x , sf.iloc[n,1:], label= str(sf.iloc[n,0])))
         
       yx.set_ylabel('Population')
       yx.set_title('Population over years')
       yx.set_xticks(x)
       yx.set_xticklabels(year_range,rotation=0)
       yx.legend(fontsize=7)
       #yx.bar_label(x, padding=3)
       fig1.tight_layout()
       plt.margins(0.09)
       plt.subplots_adjust(bottom=0.1)
       st.pyplot(fig1)



#Plotting line chart _ against subjects (groups, country..)

    if st.button('Plot population over groupe, region, country or area'):
         def bar_plot(ax, data, colors=None, total_width=0.8, single_width=.5, legend=True):
       #Draws a bar plot with multiple bars per data point.
           
           # Check if colors where provided, otherwhise use the default color cycle
           if colors is None:
               colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

           # Number of bars per group (number of times on x axis)
           n_bars = len(data.T) # len(data) makes error!!
           
          # The width of a single bar groupe (associate to each time on x axis)
           bar_width = total_width / (n_bars)
           
          # List containing handles for the drawn bars, used for the legend
           bars = []

           # Iterate over all data, i is number of bar groupes (associate to each time on x axis)
           for i, (name, values) in enumerate(data.items()):

              # The offset in x direction of that bar          
               x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
              

              # Draw a bar for every value of that type
               for x, y in enumerate(values):

                   bar = ax.bar(x + x_offset, y, width= bar_width * single_width , color=colors[i % len(colors)])
                   ax.bar_label(bar, padding=3, fontsize=5)

            
              # Add a handle to the last drawn bar, which we'll need for the legend
               bars.append(bar[0])
           
           # Draw legend if we need
           if legend:
               ax.legend(bars, data.keys(), fontsize=5)

           ax.set_ylabel('Population')
           ax.set_title('Population over years')

           #number of x-tickets
           ax.set_xticks(np.arange(n_bars))


          #value of x-tickets
           X_Tick_List = []
           X_Tick_Label_List=[]

           for item in range (0,len(sft)):
               X_Tick_List.append(item)
               X_Tick_Label_List.append(str(data.index[item]))
           
           label= X_Tick_Label_List  
           plt.xticks(ticks=X_Tick_List,labels=label, rotation=0,fontsize=8)

           
           #ax.set_xticklabels(list(data.index))
           
       #  Pad margins so that markers don't get clipped by the axes
           plt.margins(0.09)
          # Tweak spacing to prevent clipping of tick-labels
           plt.subplots_adjust(bottom=0.1)

         fig, ax = plt.subplots()
         ax.ticklabel_format(axis="y",useOffset=False,style='plain')

         bar_plot(ax, sft, total_width=.8, single_width= 1)

          #For plotting chart
         st.pyplot(fig)
           
         sf=sf.set_index(sf.columns[0])        

         x = np.arange(len(sf))  # the label locations

         curv=[]
         fig2, ax1 = plt.subplots()

         # check if ther is one columd plots scatter instead of lines
         if (len(sf)==1):

            for n in range(0,len(sft)):
                ax1.scatter(x, sft.iloc[n,0], label=str(year_range[n])) #, s=area, c=colors, alpha=0.5)
            
         else:
         
           for n in range(0,len(sft)):
               curv.append(ax1.plot(x , sft.iloc[n,0:], label= str(year_range[n])))
         
         ax1.set_ylabel('Population')
         ax1.set_title('Population over subjects')
         ax1.set_xticks(x)
         ax1.set_xticklabels(list(sf.index),rotation=90)
         ax1.legend(fontsize=7)
         #ax1.bar_label(x, padding=3)
         fig2.tight_layout()
         plt.margins(0.09)
         plt.subplots_adjust(bottom=0.1)
         st.pyplot(fig2)


