import pandas as pd
import geopandas as gpd           # importing geopandas
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

# https://medium.com/@erikgreenj/mapping-us-states-with-geopandas-made-simple-d7b6e66fa20d
usa = gpd.read_file('mapping/states.shp')
type(usa)
usa.head()
usa = usa.to_crs("EPSG:3395")

#Removes alaska and hawaii if we want -- perhaps we do them seperately?
def state_plotter(states, us_map=True):
    #setting up us_map as an input. if you want to return states that are spread out, leave it set to true.
    #If you're plotting bordering states and prefer to zoom in.
    #instantiate a matplotlib figure
    #to change size, use x_lim and y_lim. changing the figsize will not change the size of the map.
    fig, ax = plt.subplots(figsize=(30,30))
    if us_map:
        #?These codes will execute if us_map is set to True (defauit)
        #The following series of if/elif/else statements provide control over
        #whether Alaska and Hawaii will show up in the map. Because of their
        #distance from the lower 48, and the size of Alaska, we don't want them
        #in the map unless necessary
        if 'HI' in states:
            usa[0:50].plot(ax=ax, alpha = 0.3)
        elif 'AK' in states:
            usa[1:51].plot(ax=ax, alpha = 0.3)
        elif 'AK' and 'HI' in states:
            usa[0:51].plot(ax=ax, alpha = 0.3)
        else:
            usa[1:50].plot(ax=ax, alpha = 0.3)
        #The following loop will go through the list of input state abbreviations and plot them
        #ax=ax makes the states appear on the initial matplotlib figure
        for n in states:
            usa[usa.STATE_ABBR == f'{n}'].plot(ax=ax, edgecolor='y', linewidth =2)
        #If you choose not to have the first layer of the whole US, this will plot states on thier own
    elif us_map == False:
        for n in states:
            usa[usa.STATE_ABBR == f'{n}'].plot(ax=ax, edgecolor='y', linewidth =2)
    plt.show()


# state_plotter(['NY','NJ','FL'])

# https://towardsdatascience.com/lets-make-a-map-using-geopandas-pandas-and-matplotlib-to-make-a-chloropleth-map-dddc31c1983d

raindata = pd.read_csv("Data/2007-2014_GOMS_US_CSV.csv", header=0)
raindata["STATEID"] = raindata["NAME"].str[-5:-3]


###TODO MATCH DATASETS BASED ON USA[STATE_ABBR] and rainddata[STAEID]

merged = usa.set_index('STATE_ABBR').join(raindata.set_index('STATEID'))
a = merged.head()
print("t")

# set a variable that will call whatever column we want to visualise on the map
variable = 'DP01'
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(10, 6))
# create map
# merged.plot(column=variable, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')

state_precipiation_data = merged.groupby(['STATE_NAME'], as_index=False).agg('mean')
print (state_precipiation_data.head())

plt.show()