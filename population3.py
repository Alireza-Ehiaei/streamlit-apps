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

image = Image.open("Photo_by_Ishan_@seefromthesky_on_Unsplash.jpg")  
st.image(image, use_column_width=True, caption='Photo by Ishan @seefromthesky on Unsplash')


############# Reading Population data
df = pd.read_csv("WPP2019_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.csv", header=[0], encoding='latin-1')
df.columns = df.columns.astype(str)
df = df.rename(columns = {'Region, subregion, country or area':'country'})

# converting strings to numbers
for col in df.loc[:, '1950':'2020']:
  df[col]  = df[col].str.replace(' ', '')
  df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) # coercing any errors to NaN
  #df[col] = df[col].apply(lambda x: f'{x:,}')
#df = df.dropna()

############# Reading Population growth rate data

gf = pd.read_csv("WPP2019_POP_F02_POPULATION_GROWTH_RATE.csv", header=[0], encoding='latin-1')
gf.columns = gf.columns.astype(str)
gf = gf.rename(columns = {'Region, subregion, country or area':'country'})


# converting strings to numbers

for col in gf.loc[:, '1950-1955':'2015-2020']:
  gf[col]  = gf[col].str.replace(' ', '')
  gf[col] = pd.to_numeric(gf[col], errors='coerce').fillna(0) # coercing any errors to 
  gf[col] = gf[col].apply(lambda x: f'{x:,}')
#gf = gf.dropna()

st.sidebar.header('User Input Features')

selected_topic = st.sidebar.selectbox("Select Topic", ('Population', 'Population Growth Rate'))

# s = st.State() 
# if not s:
#     s.pressed_first_button = False

####################" Work on population

if (selected_topic == 'Population'):
      

      st.sidebar.header('World Population Prospects 2019:')
      st.sidebar.write(' Total population (both sexes combined) by region, subregion and country, annually for 1950-2100 (thousands)')

    ############# Time selection

      #selected_time_period = st.sidebar.multiselect("Select Year(s)", list(reversed(range(1950,2020))))
      

      container = st.sidebar.beta_container()
      all_options = st.sidebar.checkbox("Select all Years")

      if (all_options):
        selected_time_period = container.multiselect("Select all Years:", list(reversed(range(1950,2020))),list(reversed(range(1950,2020))))
      else:
        selected_time_period = container.multiselect("Select all Years:", list(reversed(range(1950,2020))))
 
      selected_time_period = sorted(selected_time_period)


      selected_time_period = pd.DataFrame(selected_time_period)

      time_period=[] #for listing name of columns
      for m in range(0,len(selected_time_period)):
        time_period.append(str(selected_time_period.loc[m,0]))

      #for slicing the columns values of the chosen list of column names
      df_selected_time_period = (df.loc[:, df.columns.isin(time_period)])

    ################ Sector selection for population

      sector = df.groupby('Type')
      sorted_sector_unique = sorted(df['Type'].unique() )

      sorted_sector_unique1 = list(filter(lambda x: x != 'Country/Area', sorted_sector_unique))
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

          # selected_sector_country = st.sidebar.multiselect('Country/Area', sorted_country_unique)
          # st.write(len(selected_sector_group))

          # all_option = st.sidebar.checkbox("Select all Countries/Areas")

          # if (all_option):
          #   selected_sector_country = list(df['country'][df['Type'] == 'Country/Area'])

          container = st.sidebar.beta_container()
          all_options = st.sidebar.checkbox("Select all Countries/Areas")

          if (all_options):
            selected_sector_country = container.multiselect("Select all Countries/Areas", sorted_country_unique,sorted_country_unique)
          else:
            selected_sector_country = container.multiselect("Select all Countries/Areas", sorted_country_unique)
     
          selected_sector_country = sorted(selected_sector_country)




      if (len(time_period) > 0 ) and ((len(selected_sector_group) > 0) or (len(selected_sector_country) > 0)):

          # Table of data

        # Filtering data
            df_selected_sector_country = df.loc[ (df['country'].isin(selected_sector_country) ) ]
            #st.dataframe(df_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)
            
            df_selected_sector= df_selected_sector_group.append(df_selected_sector_country)


            #for slicing the columns values of the chosen  time_periods 
            df_selected_time_period = (df.loc[:, df.columns.isin(time_period)])
            
            # for slicing the row values of the chosen groupes in chosen time_periods
            sf1 = df_selected_sector.loc[:, df_selected_sector.columns.isin(df_selected_time_period)]

          # names of country in the chosen rows
            sf2= df_selected_sector.loc[:,'country']      
           #To concatenate final DataFrames along column for plotting,
            sf= pd.concat([sf2, sf1], axis=1)
           
           #Transpode the table to have better sense
            sft = (sf.T)
            sft = pd.DataFrame(sft)
            
            sft.columns = sft.iloc[0]
            sft.drop(sft.index[0], inplace = True)



elif (selected_topic == 'Population Growth Rate'):



################ Time period selection for population growth rate

    
          st.sidebar.header('World Population Prospects 2019:')
          st.sidebar.write('Average annual rate of population change by region, subregion and country, 1950-2100 (percentage)')

          # Selectin time period for showing population growth rate
          # container = st.sidebar.beta_container()
          # all_options = st.sidebar.checkbox("Select all Periods")

          # if (all_options):
          #   selected_time_period = container.multiselect("Select all Periods:", list(list(gf.loc[:, '1950-1955':'2015-2020'])), list(list(gf.loc[:, '1950-1955':'2015-2020'])))
          # else:
          #   selected_time_period = container.multiselect("Select all Periods:", list(list(gf.loc[:, '1950-1955':'2015-2020'])))
     
          # selected_time_period = sorted(selected_time_period)


          # selected_time_period = pd.DataFrame(selected_time_period)

          # time_period=[] #for listing name of columns
          # for m in range(0,len(selected_time_period)):
          #   time_period.append(str(selected_time_period.loc[m,0]))

          # #for slicing the columns values of the chosen list of time periods
          # gf_selected_time_period = (gf.loc[:, df.columns.isin(time_period)])
          # gf_selected_time_period


          selected_time_period = st.sidebar.multiselect("Select Time Period", list(list(gf.loc[:, '1950-1955':'2015-2020'])))
          selected_time_period = sorted(selected_time_period)
          selected_time_period = pd.DataFrame(selected_time_period)

          time_period=[] #for listing name of columns
          for m in range(0,len(selected_time_period)):
            time_period.append(str(selected_time_period.loc[m,0]))

          #for slicing the columns values of the chosen list of column names
          gf_selected_time_period = (gf.loc[:, gf.columns.isin(selected_time_period)])


################ Sector selection for population growth rate

          sector = gf.groupby('Type')
          sorted_sector_unique = sorted(gf['Type'].unique() )

          sorted_sector_unique1 = list(filter(lambda x: x != 'Country/Area', sorted_sector_unique))
          sorted_sector_unique2 = list(filter(lambda x: x == 'Country/Area', sorted_sector_unique))


          # #Creating table for groupe in sidebar
          if (sorted_sector_unique1):
              selected_sector_group = st.sidebar.multiselect('Groupe/Region', sorted_sector_unique1)
              
              # Filtering data
              gf_selected_sector_group = gf.loc[ (gf['Type'].isin(selected_sector_group) ) ]
              #st.dataframe(gf_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)
              
           # Creating table for country in sidebar
          if (sorted_sector_unique2):
              sorted_country_unique = list(gf['country'][gf['Type'] == 'Country/Area'])
              selected_sector_country = st.sidebar.multiselect('Country/Area', sorted_country_unique)


              
              
              
          
          if (len(time_period) > 0 ) and ((len(selected_sector_group) > 0) or (len(selected_sector_country) > 0)) :


             # Filtering data
              gf_selected_sector_country = gf.loc[ (gf['country'].isin(selected_sector_country) ) ]
              #st.dataframe(gf_selected_sector.style.background_gradient(cmap='Reds').format("{:.2%}"), height=700)
              
              gf_selected_sector= gf_selected_sector_group.append(gf_selected_sector_country)
              

              #for slicing the columns values of the chosen  time_periods 
              gf_selected_time_period = (gf.loc[:, gf.columns.isin(time_period)])
             

            # for slicing the row values of the chosen groupes in chosen time_periods
              sf1 = gf_selected_sector.loc[:, gf_selected_sector.columns.isin(gf_selected_time_period)]
              
            # names of country in the chosen rows
              sf2= gf_selected_sector.loc[:,'country']

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


#################### Show table #####################

def show_table(data):

     

        if (selected_topic == 'Population'):

           st.write('Summary table for the population of ',", ".join(selected_sector_country) ,  ", ".join(selected_sector_group),'in years: ', " - ".join(time_period) )
           st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.10}"), height=300)
         

        elif (selected_topic == 'Population Growth Rate'):

           st.write('Summary table for the population growth rate of (or based on); ',  ", ".join(selected_sector_group),  ", ".join(selected_sector_country) ,'in time period: ', " - ".join(time_period) )
           st.dataframe(sf.style.background_gradient(cmap='viridis').format("{:.10}"), height=300)
        

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


       #number of x-tickets
       ax.set_xticks(np.arange(n_bars))


      # lable of x-tickets
       x_tick_list = []
       x_tick_lable_list=[]

       for item in range (0,len(sft)):
           x_tick_list.append(item)
           x_tick_lable_list.append(str(data.index[item]))
       
       label= x_tick_lable_list  
       plt.xticks(ticks=x_tick_list,labels=label, rotation=0,fontsize=8)

       
       # ax.set_xticklabels(list(data.index))
       
       # Pad margins so that markers don't get clipped by the axes
       plt.margins(0.09)

      # Tweak spacing to prevent clipping of tick-labels
       plt.subplots_adjust(bottom=0.1)

     
       # ax.ticklabel_format(axis="y",useOffset=False,style='plain', useLocale=True)
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


       #number of x-tickets
       ax.set_xticks(x)
      
      # label of x-tickets
       ax.set_xticklabels((data.T.index),rotation=0)


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


       #number of x-tickets
       ax.set_xticks(np.arange(n_bars))


      # lable of x-tickets
       x_tick_list = []
       x_tick_lable_list=[]

       for item in range (0,len(data.T)):
           x_tick_list.append(item)
           x_tick_lable_list.append(str(data.T.index[item]))
       
       label= x_tick_lable_list  
       plt.xticks(ticks=x_tick_list,labels=label, rotation=80,fontsize=8)

       
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
          ax1.set_ylabel('Groupe/Region-Country/Aria')



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
 

################# Plotting - showing orders
#session_state_show = SessionState.get(show='', button_sent=False)
#button_sent= st.sidebar.button('Show Dataset')  
# if (button_sent)

if (len(time_period) > 0 ) and ((len(selected_sector_group) > 0) or (len(selected_sector_country) > 0)):
 
 #session_state_show.button_sent =True

 #if session_state_show.button_sent:

   # session_state.checkboxed = True
    



    # session_state.checkboxed = False
    # selected_chart = st.radio("Select Charts ", ["Population over Time",  "Population over  Groupe/Region or Country/Aria", "Both"], index=2)
    # st.write("selected_chart",selected_chart)

    # session_state_input = SessionState.get(text='', checkboxed1=False)
    # st.write('Select Charts:')
    # session_state_input.text = 'Population over Time'
    # checkboxed1= st.checkbox('Population over Time')
    # session_state.option_2 = st.checkbox('Population over  Groupe/Region or Country/Aria')
    # session_state.option_3 = st.checkbox('Both')
    

    # if checkboxed1:
    #   session_state_input.checkboxed1 = True


    show_table(sf)

    fig, ax = plt.subplots()
    bar_chart_time(ax, sft, total_width=.8, single_width= 1)

    fig, ax1 = plt.subplots()
    line_chart_time(ax1, sf)
    

    fig, ax = plt.subplots()
    bar_chart_gr(ax, sft, total_width=.8, single_width= 1)


    
# elif (session_state_show.button_sent ==False):
#    st.write("Please select at least one Year, and one Groupe/Region or Country/Aria")


st.sidebar.text("")
st.sidebar.text("")


# Cleaning the plot (useful if you want to draw new shapes without closing the figure
# but quite useless for this particular example. I put it here as an example).

#plt.gcf().clear()
# checkbox

st.sidebar.write(''' This app is created by [a.ehiaei] (https://www.linkedin.com/in/alireza-ehiaei-9280971a1/), any tips appreciated.''')
    #df.numeric.describe()


st.sidebar.text("")
st.sidebar.text("")

 