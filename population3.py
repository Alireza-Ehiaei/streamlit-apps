import matplotlib as mpl
#import locale
#import SessionState
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.pyplot import figure
import base64
from PIL import Image

#session_state = SessionState.get(checkboxed=False)

######################
# Page Title
######################
st.write("""
# Building a blooming world for all.
""")
image = Image.open("hugh-whyte-J8bU6-tAGy8-unsplash.jpg")

st.image(image, use_column_width=True, caption='Photo by Hugh Whyte on Unsplash')
#Photo by <a href="https://unsplash.com/@opixels?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Hugh Whyte</a> on <a href="https://unsplash.com/s/photos/sustainable-development?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  

st.write("""
# Numbers & Concepts For Development

### Hello!

Thanks for showing interest to see this website! We are going 
to have a new look at the ***numbers & concepts*** in the 
fields of **development & economics**.  

Searching data can be sometimes a time-consuming and tedious process, and filtering, visualizing, and manipulating data can be a 
complicated task. Here you have easier ways to see and download data, and also, be familiar with some concepts in economics and development. 
Remember, data is only valuable if you know how to visualize it and give context. Let's get started with data of population around the world.
""")

st.markdown(""" 

## Population 
Please select the sectors and dates you want to Visualize and Download the population statitics from the left sidebar.
* **Selection based on:** regin, development group, income croupe, and country.
* **Data source:** [United Nations](https://population.un.org/wpp/Download/Standard/Population/)
""")


glbutton = st.button("Glossary")
if glbutton:
         st.write("Total Population:")
         st.success("""Total Population - Both Sexes. De facto population in a country, 
          area or region as of 1 July of the year indicated. Figures are presented in thousands.""")

         st.write("Population Growth Rate: ")
         st.success("""Average exponential rate of growth of the population over a given period. 
          It is calculated as ln(Pt/P0)/t where t is the length of the period. It is expressed as a percentage.
          The rate of population growth is the rate of natural increase (the difference between the birthrate
           and the death rate) combined with the effects of migration.""")

         st.write("Median Age of Population:")
         st.success("""Age that divides the population in two parts of equal size, that is, there are as many 
          persons with ages above the median as there are with ages below the median. It is expressed as years.""")

         st.write("Population Density:")
         st.success("""Population per square Kilometre.""")

         # st.write("Population percentage by Broad Age Groups - Both Sexes:")
         # st.success("""Percentage of Total Population by Broad Age Groups. De facto population as of 1 July of the year indicated.
         #  Figures are expressed per 100 total population.""")

         # st.write("Total Dependency Ratio:")
         # st.success("""((Age 0-14 + Age 65+) / Age 15-64). De facto population as of 1 July of the year indicated.""")

         # st.write("Child Dependency Ratio:")
         # st.success(""" (Age 0-14 / Age 15-64) De facto population as of 1 July of the year indicated.""")
         
         # st.write("Old-Age Dependency Ratio:")
         # st.success("""(Age 65+ / Age 15-64) De facto population as of 1 July of the year indicated.""")

  



image = Image.open("Photo_by_Ishan_@seefromthesky_on_Unsplash.jpg")  
st.image(image, use_column_width=True, caption='Photo by Ishan @seefromthesky on Unsplash')


st.sidebar.header('User Input Features')
selected_topic = st.sidebar.selectbox("Select Topic", ('Population', 'Population Growth Rate', 'Population Density', 'Median Age of Population'))

#################################################### population  ###################################################

if (selected_topic == 'Population'):

      ############# Reading Population data
      df = pd.read_csv(r"C:\Users\IMBS\Downloads\programming\Data\pop_data\WPP2019_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.csv", header=[0], encoding='latin-1')
      df.columns = df.columns.astype(str)
      df = df.rename(columns = {'Region, subregion, country or area':'country'})
      # df = pd.DataFrame(df)
      # df.drop(df[df.Type == "Label/Separator"].index, inplace=True)
      # df = df.reset_index(drop=True)############# Reading Population growth rate data


      # converting strings to numbers
      for col in df.loc[:, '1950':'2020']:
        df[col]  = df[col].str.replace(' ', '')
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) # coercing any errors to NaN
        #df[col] = df[col].apply(lambda x: f'{x:,}')
      #df = df.dropna()
      

      st.sidebar.header('World Population Prospects 2019:')
      st.sidebar.write(' Total population (both sexes combined) by region, subregion and country, annually estimates for 1950 - 2020 (thousands)')


################ Sector selection for population

      sector = df.groupby('Type')
      sorted_sector_unique = sorted(df['Type'].unique())

      sorted_sector_unique1 = list(filter(lambda x: x != 'Country/Area' and x != 'Label/Separator' and x != 'SDG subregion', sorted_sector_unique))
      sorted_sector_unique2 = list(filter(lambda x: x == 'Country/Area', sorted_sector_unique))


      # #Creating table for groupe in sidebar
      if (sorted_sector_unique1):
          selected_sector_group = st.sidebar.multiselect('Groupe/Region', sorted_sector_unique1)

          # Filtering data
          df_selected_sector_group = df.loc[ (df['Type'].isin(selected_sector_group) ) ]
          #st.dataframe(df_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)

       # Creating table for country in sidebar
      if (sorted_sector_unique2):
          sorted_country_unique = list(df['country'][df['Type'] == 'Country/Area'])

          selected_sector_country = st.sidebar.multiselect('Country/Area', sorted_country_unique)
          
        # # For selecting all countries instead of the line above write lines below (not recommended)
        #   container = st.sidebar.beta_container()
        #   all_options = st.sidebar.checkbox("Select all Countries/Areas")

        #   if (all_options):
        #     selected_sector_country = container.multiselect("Select all Countries/Areas", sorted_country_unique,sorted_country_unique)
        #   else:
        #     selected_sector_country = container.multiselect("Select all Countries/Areas", sorted_country_unique)
     
          selected_sector_country = sorted(selected_sector_country)


     # Filtering data
      df_selected_sector_country = df.loc[ (df['country'].isin(selected_sector_country) ) ]
      
      df_selected_sector= df_selected_sector_group.append(df_selected_sector_country)
    


############# Time selection for population     

      container = st.sidebar.beta_container()
      all_options = st.sidebar.checkbox("Select all Years")

      if (all_options):
        selected_time_period = container.multiselect("Select Year(s):", list(reversed(range(1950,2020))),list(reversed(range(1950,2020))))
      else:
        selected_time_period = container.multiselect("Select Year(s):", list(reversed(range(1950,2020))))
 
      selected_time_period = sorted(selected_time_period)
      selected_time_period = pd.DataFrame(selected_time_period)

      time_period=[] #for listing name of columns
      for m in range(0,len(selected_time_period)):
        time_period.append(str(selected_time_period.loc[m,0]))


######### Table of data for population
   
      if (len(time_period) > 0 ) and ((len(selected_sector_group) > 0) or (len(selected_sector_country) > 0)):

     #for slicing the columns values of the chosen  time_periods 
            sf1= (df_selected_sector.loc[:, df.columns.isin(time_period)])
            
          # names of country in the chosen rows
            sf2= df_selected_sector.loc[:,'country']      
           #To concatenate final DataFrames along column for plotting,
            sf= pd.concat([sf2, sf1], axis=1)
           
           #Transpode the table to have better sense
            sft = (sf.T)
            sft = pd.DataFrame(sft)
            
            sft.columns = sft.iloc[0]
            sft.drop(sft.index[0], inplace = True)




#################################################### Population Growth Rate ###################################################


elif (selected_topic == 'Population Growth Rate'):

          df = pd.read_csv(r"C:\Users\IMBS\Downloads\programming\Data\pop_data\WPP2019_POP_F02_POPULATION_GROWTH_RATE.csv", header=[0], encoding='latin-1')
          df.columns = df.columns.astype(str)
          df = df.rename(columns = {'Region, subregion, country or area':'country'})


          # converting strings to numbers

          for col in df.loc[:, '1950-1955':'2015-2020']:
            df[col]  = df[col].str.replace(' ', '')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) # coercing any errors to NaN
            
          
          st.sidebar.header('World Population Prospects 2019:')
          st.sidebar.write('Average annual rate of population change by region, subregion and country, annually estimates for 1950 - 2020 (percentage)')


################ Sector selection for population growth rate

          sector = df.groupby('Type')
          sorted_sector_unique = sorted(df['Type'].unique() )

          sorted_sector_unique1 = list(filter(lambda x: x != 'Country/Area' and x != 'Label/Separator' and x != 'SDG subregion', sorted_sector_unique))
          sorted_sector_unique2 = list(filter(lambda x: x == 'Country/Area', sorted_sector_unique))


          # table for groupe in sidebar
          if (sorted_sector_unique1):
              selected_sector_group = st.sidebar.multiselect('Groupe/Region', sorted_sector_unique1)
              
              # Filtering data
              df_selected_sector_group = df.loc[ (df['Type'].isin(selected_sector_group) ) ]
              #st.dataframe(gf_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)
              
           # table for country in sidebar
          if (sorted_sector_unique2):
              sorted_country_unique = list(df['country'][df['Type'] == 'Country/Area'])
              selected_sector_country = st.sidebar.multiselect('Country/Area', sorted_country_unique)

          df_selected_sector_country = df.loc[ (df['country'].isin(selected_sector_country) ) ]
              
          df_selected_sector= df_selected_sector_group.append(df_selected_sector_country)
              
 

################ Time period selection for population growth rate

          container = st.sidebar.beta_container()
          all_options = st.sidebar.checkbox("Select all Periods")

          if (all_options):
            selected_time_period = container.multiselect("Select Time Period:", list(list(df.loc[:, '1950-1955':'2015-2020'])), list(list(df.loc[:, '1950-1955':'2015-2020'])))
          else:
            selected_time_period = container.multiselect("Select Time Period:", list(list(df.loc[:, '1950-1955':'2015-2020'])))
     
          selected_time_period = sorted(selected_time_period)
          selected_time_period = pd.DataFrame(selected_time_period)


          time_period=[] #for listing name of columns
          for m in range(0,len(selected_time_period)):
              time_period.append(str(selected_time_period.loc[m,0]))



######### Table of data for population growth rate

          if (len(time_period) > 0 ) and ((len(selected_sector_group) > 0) or (len(selected_sector_country) > 0)) :

           # Slicing the row values of the chosen groupes in chosen time_periods
              sf1 = df_selected_sector.loc[:, df_selected_sector.columns.isin(time_period)]
              
            # names of country in the chosen rows
              sf2= df_selected_sector.loc[:,'country']

             #To concatenate final DataFrames along column for plotting,
              sf= pd.concat([sf2, sf1], axis=1)
             
             #Transpode the table to have better sense
              sft = (sf.T)
              sft.columns = sft.iloc[0]
              sft.drop(sft.index[0], inplace = True)
         
        #    st.write('Summary table for the population growth rate of (or based on); ',  ", ".join(selected_sector_group),  ", ".join(selected_sector_country) ,'in time period: ', " - ".join(time_period) )
        #    st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.10}"), height=300)
        
        # def filedownload(gf):
        #      csv = gf.to_csv(index=True)
        #      b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        #      href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
        #      return href

        # st.markdown(filedownload(sf), unsafe_allow_html=True)




#################################################### Median Age of Population ###################################################

elif (selected_topic == 'Median Age of Population'):

          df = pd.read_csv(r"C:\Users\IMBS\Downloads\programming\Data\pop_data\WPP2019_POP_F05_MEDIAN_AGE.csv", header=[0], encoding='latin-1')
        
          df.columns = df.columns.astype(str)
          df = df.rename(columns = {'Region, subregion, country or area':'country'})
      

          # converting strings to numbers

          for col in df.loc[:, '1950':'2020']:
            df[col]  = df[col].str.replace(' ', '')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) # coercing any errors to 
           # gf[col] = gf[col].apply(lambda x: f'{x:,}')
           #gf = gf.dropna()

          
          st.sidebar.header('World Population Prospects 2019:')
          st.sidebar.write('Median Age of Population by region, subregion and country, annually estimates for 1950 - 2020')


################ Sector selection for Median Age of Population

          sector = df.groupby('Type')
          sorted_sector_unique = sorted(df['Type'].unique() )

          sorted_sector_unique1 = list(filter(lambda x: x != 'Label/Separator' and x != 'Label/Separator' and x != 'SDG subregion' and x != 'Country/Area', sorted_sector_unique))
          sorted_sector_unique2 = list(filter(lambda x: x == 'Country/Area', sorted_sector_unique))


          # table for groupe in sidebar
          if (sorted_sector_unique1):
              selected_sector_group = st.sidebar.multiselect('Groupe/Region', sorted_sector_unique1)
              
              # Filtering data
              df_selected_sector_group = df.loc[ (df['Type'].isin(selected_sector_group) ) ]
              #st.dataframe(gf_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)
              
           # table for country in sidebar
          if (sorted_sector_unique2):
              sorted_country_unique = list(df['country'][df['Type'] == 'Country/Area'])
              selected_sector_country = st.sidebar.multiselect('Country/Area', sorted_country_unique)
          
          df_selected_sector_country = df.loc[ (df['country'].isin(selected_sector_country) ) ]
              
          df_selected_sector= df_selected_sector_group.append(df_selected_sector_country)


################ Time period selection for Median Age of Population

          container = st.sidebar.beta_container()
          all_options = st.sidebar.checkbox("Select all Years")

          if (all_options):
            selected_time_period = container.multiselect("Select Year(s):", list(list(df.loc[:, '1950':'2020'])), list(list(df.loc[:, '1950':'2020'])))
          else:
            selected_time_period = container.multiselect("Select Year(s):", list(list(df.loc[:, '1950':'2020'])))
     
          selected_time_period = sorted(selected_time_period)
          selected_time_period = pd.DataFrame(selected_time_period)

          time_period=[] #for listing name of columns
          for m in range(0,len(selected_time_period)):
            time_period.append(str(selected_time_period.loc[m,0]))

   

######### Table of data for Median Age of Population

          if (len(time_period) > 0 ) and ((len(selected_sector_group) > 0) or (len(selected_sector_country) > 0)):

                            
           # Slicing the row values of the chosen groupes in chosen time_periods
              sf1 = df_selected_sector.loc[:, df_selected_sector.columns.isin(time_period)]
              
            # names of country in the chosen rows
              sf2= df_selected_sector.loc[:,'country']

             #To concatenate final DataFrames along column for plotting,
              sf= pd.concat([sf2, sf1], axis=1)
           
           #Transpode the table to have better sense
              sft = (sf.T)
              sft = pd.DataFrame(sft)
              
              sft.columns = sft.iloc[0]
              sft.drop(sft.index[0], inplace = True)
              




#################################################### Population  Density ###################################################

elif (selected_topic == 'Population Density'):

          df = pd.read_csv(r"C:\Users\IMBS\Downloads\programming\Data\pop_data\WPP2019_POP_F06_POPULATION_DENSITY.csv", header=[0], encoding='latin-1')
        
          df.columns = df.columns.astype(str)
          df = df.rename(columns = {'Region, subregion, country or area':'country'})
      

          # converting strings to numbers

          for col in df.loc[:, '1950':'2020']:
            df[col]  = df[col].str.replace(' ', '')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) # coercing any errors to 
           # gf[col] = gf[col].apply(lambda x: f'{x:,}')
           #gf = gf.dropna()

          
          st.sidebar.header('World Population Prospects 2019:')
          st.sidebar.write('Population density by region, subregion and country, annually estimates for 1950 - 2020 (persons per square km)')


################ Sector selection for Population  Density

          sector = df.groupby('Type')
          sorted_sector_unique = sorted(df['Type'].unique() )

          sorted_sector_unique1 = list(filter(lambda x: x != 'Label/Separator' and x != 'Label/Separator' and x != 'SDG subregion' and x != 'Country/Area', sorted_sector_unique))
          sorted_sector_unique2 = list(filter(lambda x: x == 'Country/Area', sorted_sector_unique))


          # table for groupe in sidebar
          if (sorted_sector_unique1):
              selected_sector_group = st.sidebar.multiselect('Groupe/Region', sorted_sector_unique1)
              
              # Filtering data
              df_selected_sector_group = df.loc[ (df['Type'].isin(selected_sector_group) ) ]
              #st.dataframe(gf_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)
              
           # table for country in sidebar
          if (sorted_sector_unique2):
              sorted_country_unique = list(df['country'][df['Type'] == 'Country/Area'])
              selected_sector_country = st.sidebar.multiselect('Country/Area', sorted_country_unique)
          

          df_selected_sector_country = df.loc[ (df['country'].isin(selected_sector_country) ) ]
          
          df_selected_sector= df_selected_sector_group.append(df_selected_sector_country)
              


################ Time period selection for Population  Density

          container = st.sidebar.beta_container()
          all_options = st.sidebar.checkbox("Select all Years")

          if (all_options):
            selected_time_period = container.multiselect("Select Year(s):", list(reversed(range(1950,2020))),list(reversed(range(1950,2020))))
          else:
            selected_time_period = container.multiselect("Select Year(s):", list(reversed(range(1950,2020))))
     
          selected_time_period = sorted(selected_time_period)
          selected_time_period = pd.DataFrame(selected_time_period)

          time_period=[] #for listing name of columns
          for m in range(0,len(selected_time_period)):
            time_period.append(str(selected_time_period.loc[m,0]))


          


######### Table of data for population density

          if (len(time_period) > 0 ) and ((len(selected_sector_group) > 0) or (len(selected_sector_country) > 0)):

           # Slicing the row values of the chosen groupes in chosen time_periods
              sf1 = df_selected_sector.loc[:, df_selected_sector.columns.isin(time_period)]
              
            # names of country in the chosen rows
              sf2= df_selected_sector.loc[:,'country']

             #To concatenate final DataFrames along column for plotting,
              sf= pd.concat([sf2, sf1], axis=1)
           
           #Transpode the table to have better sense
              sft = (sf.T)
              sft = pd.DataFrame(sft)
              
              sft.columns = sft.iloc[0]
              sft.drop(sft.index[0], inplace = True)






#################################################### population by age groupe ###################################################

elif (selected_topic == 'Population by Age Group'):

          df = pd.read_csv(r"C:\Users\IMBS\Downloads\programming\Data\pop_data\WPP2019_POP_F09_1_PERCENTAGE_OF_TOTAL_POPULATION_BY_BROAD_AGE_GROUP_BOTH_SEXES.csv", header=[0], encoding='latin-1')
        
          df.columns = df.columns.astype(str)
          df = df.rename(columns = {'Region, subregion, country or area':'country', 'Reference date (as of 1 July)':'date'})
      

          # converting strings to numbers

          for col in df.loc[:, '0-1':'90+']:
            df[col]  = df[col].str.replace(' ', '')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) # coercing any errors to 
           # gf[col] = gf[col].apply(lambda x: f'{x:,}')
           #gf = gf.dropna()

          
          st.sidebar.header('World Population Prospects 2019:')
          st.sidebar.write(' Percentage total population (both sexes combined) by broad age group, region, subregion and country, annually estimates for 1950 - 2020 (percentage)')
   

################ Sector selection for population by age groupe

          sector = df.groupby('Type')
          sorted_sector_unique = sorted(df['Type'].unique() )

          sorted_sector_unique1 = list(filter(lambda x: x != 'Label/Separator' and x != 'Label/Separator' and x != 'SDG subregion' and x != 'Country/Area', sorted_sector_unique))
          sorted_sector_unique2 = list(filter(lambda x: x == 'Country/Area', sorted_sector_unique))


          # table for groupe in sidebar
          if (sorted_sector_unique1):
              selected_sector_group = st.sidebar.multiselect('Groupe/Region', sorted_sector_unique1)
              
              
           # table for country in sidebar
          if (sorted_sector_unique2):
              sorted_country_unique = list(df['country'][df['Type'] == 'Country/Area'].unique())
              selected_sector_country = st.sidebar.multiselect('Country/Area', sorted_country_unique)


          df_selected_sector= selected_sector_group + (selected_sector_country)
          df_selected_sector
          



          
################ Age groupe selection for population by age groupe
          
          container = st.sidebar.beta_container()
          all_options = st.sidebar.checkbox("Select all Age Groupes")

          if (all_options):
            selected_age_group = container.multiselect("Select Age Groupe:", list(list(df.loc[:, '0-1':'90+'])), list(list(df.loc[:, '0-1':'90+'])))
          else:
            selected_age_group = container.multiselect("Select Age Groupe:", list(list(df.loc[:, '0-1':'90+'])))
     
          selected_age_group = sorted(selected_age_group)
          selected_age_group = pd.DataFrame(selected_age_group)

          age_group=[] #for listing name of columns
          for m in range(0,len(selected_age_group)):
            age_group.append(str(selected_age_group.loc[m,0]))


################ Time period selection for population by age groupe
         
          container = st.sidebar.beta_container()
          all_options = st.sidebar.checkbox("Select all Years")

          if (all_options):
            selected_time_period = container.multiselect("Select Year(s):",  list(reversed(range(1950,2020, 5))),list(reversed(range(1950,2020,5))))
          else:
            selected_time_period = container.multiselect("Select Year(s):", list(reversed(range(1950,2020, 5))))
     
          selected_time_period = sorted(selected_time_period)
          selected_time_period = pd.DataFrame(selected_time_period)

          time_period=[] #for listing name of columns
          for m in range(0,len(selected_time_period)):
            time_period.append(str(selected_time_period.loc[m,0]))

          time= pd.to_numeric(time_period)
           

######### Table of data for population by age groupe

          if (len(time_period) > 0 ) and ((len(df_selected_sector) > 0) ):
              
              sf1  = df.loc[ (df['country'].isin(selected_sector_country) | df['Type'].isin(selected_sector_group)) & (df['date'].isin(time)), ['country', 'date'] ]
              sf2  = df.loc[ (df['country'].isin(selected_sector_country) | df['Type'].isin(selected_sector_group) )& (df['date'].isin(time)), df.columns.isin(age_group) ]

  
             #To concatenate final DataFrames along column for plotting,
              sf= pd.concat([sf1, sf2], axis=1)            

                  
           #Transpode the table to have better sense
              sft = (sf.T)
              sft = pd.DataFrame(sft)
              
              sft.columns = sft.iloc[0]
              sft.drop(sft.index[0], inplace = True)
              sf
              





#################################################### population  ###################################################






#################################################### population  ###################################################








#################################################### population  ###################################################




#################################################### population  ###################################################

#################### Show table #####################

def show_table(data):
     

        if (selected_topic == 'Population'):

           st.write('Summary table for the Population of ',", ".join(selected_sector_country) ,  ", ".join(selected_sector_group),'in time period: ', " - ".join(time_period) )
           st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.10}"), height=300)
         

        elif (selected_topic == 'Population Growth Rate'):

           st.write('Summary table for the Population Growth Rate of (or based on); ',  ", ".join(selected_sector_group),  ", ".join(selected_sector_country) ,'in time period: ', " - ".join(time_period) )
           st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.10}"), height=300)
        
        elif (selected_topic == 'Population Density'):

           st.write('Summary table for the Population Density of (or based on); ',  ", ".join(selected_sector_group),  ", ".join(selected_sector_country) ,'in time period: ', " - ".join(time_period) )
           st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.10}"), height=300)

           
        elif (selected_topic == 'Median Age of Population'):

           st.write('Summary table for the Median Age of Population of (or based on); ',  ", ".join(selected_sector_group),  ", ".join(selected_sector_country) ,'in time period: ', " - ".join(time_period) )
           st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.10}"), height=300)



        elif (selected_topic == 'Population by Age Group'):

           st.write('Summary table for the population by age group of (or based on); ',  ", ".join(df_selected_sector) ,'in time period: ', " - ".join(time_period) )
           st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.0f}").set_precision(2), height=300)

       #For downloading csv file
        def filedownload(df):
             csv = df.to_csv(index=True)
             b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
             href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
             return href

        st.markdown(filedownload(data.T), unsafe_allow_html=True)


####################### Plotting #########################



######################### Definning function for plotting bar chart of population over groupe, country...

def bar_chart_time(ax, data, colors=None, total_width=0.8, single_width=.5, legend=True):
             
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
               ax.bar_label(bar, padding= 5, fontsize=6 , rotation=90) #  fmt='%d', label_type='center',

        
          # Add a handle to the last drawn bar, which we'll need for the legend
           bars.append(bar[0])
       
       # Draw legend if we need
       if legend:
           ax.legend(bars, data.keys(), fontsize=5)


       if (selected_topic == 'Population'): 
            ax.set_title('Population over Time')
            ax.set_ylabel('Population')

       elif (selected_topic == 'Population Growth Rate'):
          ax.set_title('Population Growth Rate over Time')
          ax.set_ylabel('Population Growth Rate')

       elif (selected_topic == 'Population Density'):
          ax.set_title('Population Density over Time')
          ax.set_ylabel('Population Density')

       elif (selected_topic == 'Median Age of Population'):
          ax.set_title('Median Age of Population over Time')
          ax.set_ylabel('Median Age of Population')

          


       #number of x-tickets
       ax.set_xticks(np.arange(n_bars))


      # lable of x-tickets
       x_tick_list = []
       x_tick_lable_list=[]

       for item in range (0,len(sft)):
           x_tick_list.append(item)
           x_tick_lable_list.append(str(data.index[item]))
       
       label= x_tick_lable_list  
       plt.xticks(ticks=x_tick_list,labels=label, rotation=45,fontsize=8, ha="right", rotation_mode="default")
       


       
       # ax.set_xticklabels(list(data.index))
       
       # Pad margins so that markers don't get clipped by the axes
       plt.margins(0.09)

      # Tweak spacing to prevent clipping of tick-labels
       plt.subplots_adjust(bottom=0.1)

     
       #ax.ticklabel_format(axis="y",useOffset=False,style='plain', useLocale=True)
       ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

      #For plotting chart
       st.pyplot(fig)

       return



######################### Definning function for plotting line chart of population over groupe, country...

def line_chart_time(ax, data):
       
       data=data.set_index(data.columns[0])  
            
       x = np.arange(len(time_period))  # the label locations

       curv=[]

       # check if there is one column plots scatter instead of lines
       if (len(time_period)==1):

          for n in range(0,len(data)):
              ax.scatter(x, data.iloc[n,0], label=str(data.index[n])) #, s=area, c=colors, alpha=0.5)

       else:
       
         for n in range(0,len(data)):
             curv.append(ax.plot(x, data.iloc[n,0:], label= str(data.index[n])))
       

       if (selected_topic == 'Population'): 
            ax.set_title('Population over Time')
            ax.set_ylabel('Population')

       elif (selected_topic == 'Population Growth Rate'):
          ax.set_title('Population Growth Rate over Time')
          ax.set_ylabel('Population Growth Rate')

       elif (selected_topic == 'Population Density'):
          ax.set_title('Population Density over Time')
          ax.set_ylabel('Population Density')

       elif (selected_topic == 'Median Age of Population'):
          ax.set_title('Median Age of Population over Time')
          ax.set_ylabel('Median Age of Population')


       #number of x-tickets
       ax.set_xticks(x)
      
      # label of x-tickets
       ax.set_xticklabels((data.T.index),rotation=45)


       # Changing scientific notation of numbers
       # ax.ticklabel_format(axis="y",useOffset=True,style='plain', useLocale=True)
       ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

       # #ax1.set_yticklabels(list(data.index),rotation=0)
       #ax1.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter("%.f")) # setting number of decilals

       ax.legend(fontsize=7)
       #ax1.bar_label(x, padding=3)
       fig.tight_layout()
       plt.margins(0.09)
       plt.subplots_adjust(bottom=0.1)
       st.pyplot(fig)

       return


######################### Definning function for plotting bar chart of population over groupe, country...

def bar_chart_gr(ax, data, colors=None, total_width=0.8, single_width=.5, legend=True):
     
       # Check if colors where provided, otherwhise use the default color cycle
       if colors is None:
           colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

       # Number of bars per group (number of times on x axis)
       n_bars = len(data) # len(data) makes error!!
       
      # The width of a single bar groupe (associate to each time on x axis)
       bar_width = total_width / (n_bars)
       
      # List containing handles for the drawn bars, used for the legend
       bars = []

       # Iterate over all data, i is number of bar groupes (associate to each time on x axis)
       for i, (name, values) in enumerate(data.T.items()):

          # The offset in x direction of that bar          
           x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
          

          # Draw a bar for every value of that type
           for x, y in enumerate(values):

               bar = ax.bar(x + x_offset, y, width= bar_width * single_width , color=colors[i % len(colors)])
               ax.bar_label(bar, padding=5, fontsize=6 ,  rotation=90) # fmt='%d',

        
          # Add a handle to the last drawn bar, which we'll need for the legend
           bars.append(bar[0])
       
       # Draw legend if we need
       if legend:
           ax.legend(bars, data.T.keys(), fontsize=5)

       if (selected_topic == 'Population'): 
            ax.set_title('Population by Groupe/Region-Country/Aria')
            ax.set_ylabel('Population')

       elif (selected_topic == 'Population Growth Rate'):
          ax.set_title('Population Growth Rate by Groupe/Region-Country/Aria')
          ax.set_ylabel('Population Growth Rate')

       elif (selected_topic == 'Population Density'):
          ax.set_title('Population Density by Groupe/Region-Country/Aria')
          ax.set_ylabel('Population Density')

       elif (selected_topic == 'Median Age of Population'):
          ax.set_title('Median Age of Population over Time')
          ax.set_ylabel('Median Age of Population')


       #number of x-tickets
       ax.set_xticks(np.arange(n_bars))


      # lable of x-tickets
       x_tick_list = []
       x_tick_lable_list=[]

       for item in range (0,len(data.T)):
           x_tick_list.append(item)
           x_tick_lable_list.append(str(data.T.index[item]))
       
       label= x_tick_lable_list  
       plt.xticks(ticks=x_tick_list,labels=label, rotation=45,fontsize=8)

       
       #ax.set_xticklabels(list(data.index))
       
      # Pad margins so that markers don't get clipped by the axes
       plt.margins(0.09)

      # Tweak spacing to prevent clipping of tick-labels
       plt.subplots_adjust(bottom=0.1)

     
       # ax.ticklabel_format(axis="y",useOffset=False, style='plain', useLocale=True)
       ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

     # for rotation the chart: https://stackoverflow.com/questions/22540449/how-can-i-rotate-a-matplotlib-plot-through-90-degrees
       
        #For plotting chart
       st.pyplot(fig)
       return


######################### Definning function for plotting line chart of population over groupe, country...

def line_chart_gr(ax, data):
       
       
       data=data.set_index(data.columns[0])        

       y = np.arange(len(data))  # the label locations

       curv=[]

      # # check if ther is one columd plots scatter instead of lines
      #  if (len(time_period)==1):

      #     for n in range(0,len(data)-1):
      #         ax1.scatter(data.iloc[n,0], y, label=str(time_period[n]))  #, s=area, c=colors, alpha=0.5) 
          
       # else:
       
       for n in range(0,len(data.T)):
             curv.append(ax1.plot(data.T.iloc[n,0:], y  , label= str(time_period[n]))) #, autopct='%.2f'
       
       
       if (selected_topic == 'Population'): 
            ax1.set_title('Population by Groupe/Region-Country/Aria')
            ax1.set_ylabel('Population')

       elif (selected_topic == 'Population Growth Rate'):
          ax1.set_title('Population Growth Rate by Groupe/Region-Country/Aria')
          ax1.set_ylabel('')

       elif (selected_topic == 'Population Density'):
          ax.set_title('Population Density by Groupe/Region-Country/Aria')
          ax.set_ylabel('Population Density')

       elif (selected_topic == 'Median Age of Population'):
          ax.set_title('Median Age of Population over Time')
          ax.set_ylabel('Median Age of Population')

       ax1.set_yticklabels(list(data.index),rotation=0)
       ax1.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter("%.2d")) # setting number of decilals
       ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
       ax1.legend(fontsize=7)

       #ax1.bar_label(x, padding=3)
       
       fig.tight_layout()
       plt.savefig("pgf_fonts.pdf")
       plt.margins(0.09)
       plt.subplots_adjust(bottom=0.1)
       
         

       st.pyplot(fig)

       return
 

################# Plotting Execution


if (len(time_period) > 0 ) and (len(df_selected_sector) > 0):

    show_table(sf)
    

    check = st.checkbox("Plot Population over Time")
    #st.write('State of the checkbox:', check)

    if check:

           fig, ax = plt.subplots()
           bar_chart_time(ax, sft, total_width=.8, single_width= 1)

           fig, ax1 = plt.subplots()
           line_chart_time(ax1, sf)

    check1 = st.checkbox("Population over  Groupe/Region or Country/Aria")
    if check1:

            fig, ax = plt.subplots()
            bar_chart_gr(ax, sft, total_width=.8, single_width= 1)

    
    # check2 = st.checkbox("Both")
    # if check2:

    #        fig, ax = plt.subplots()
    #        bar_chart_time(ax, sft, total_width=.8, single_width= 1)

    #        fig, ax1 = plt.subplots()
    #        line_chart_time(ax1, sf)

    #        fig, ax = plt.subplots()
    #        bar_chart_gr(ax, sft, total_width=.8, single_width= 1)
          

    
# elif (session_state_show.button_sent ==False):
#    st.write("Please select at least one Year, and one Groupe/Region or Country/Aria")


st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")


# Cleaning the plot (useful if you want to draw new shapes without closing the figure
# but quite useless for this particular example. I put it here as an example).

#plt.gcf().clear()
# checkbox

st.text("")
st.text("")
st.text("")
st.text("")

st.text("")
st.text("")
st.text("")
st.text("")


st.markdown('***')
st.markdown(" This app is created by [a.ehiaei] (https://www.linkedin.com/in/alireza-ehiaei-9280971a1/), any tips appreciated.")
    #df.numeric.describe()


st.sidebar.text("")
st.sidebar.text("")

 