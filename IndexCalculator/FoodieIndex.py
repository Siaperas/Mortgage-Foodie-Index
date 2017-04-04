from sqlalchemy import *
from pandas import DataFrame
import numpy as np
import pandas as pd
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.cm


db = create_engine('sqlite:///london_restaurants.db')
metadata = MetaData(db)
# Retrieve the restaurants from the database
restaurants = Table('London_Restaurants', metadata, autoload=True)
connection = db.connect()
# Retrieve the necessary info and add them to dataframe
resoverall = connection.execute("SELECT area AS AREA, COUNT(area) AS COUNT,SUM(rating)/COUNT(area) AS AVERAGE FROM London_Restaurants GROUP BY area")
df = DataFrame(resoverall.fetchall())
df.columns = resoverall.keys()

# DataFrame manipulation
df2 = DataFrame(columns=('AREA', 'DENSITY'))
df2.loc[0] = ["E", 20]
df2.loc[1] = ["EC", 1]
df2.loc[2] = ["N", 22]
df2.loc[3] = ["NW", 11]
df2.loc[4] = ["SE", 28]
df2.loc[5] = ["SW", 20]
df2.loc[6] = ["W", 14]
df2.loc[7] = ["WC", 1]
df = df.merge(df2, on='AREA')
df.head()

# Calculate the Foodie Index of each area
df2 = DataFrame(columns=('AREA', 'INDEX'))
df2.loc[0] = ["E", (df.iat[0,1]/df.iat[0,3])/500+df.iat[0,2]]
df2.loc[1] = ["EC", (df.iat[1,1]/df.iat[1,3])/500+df.iat[1,2]]
df2.loc[2] = ["N", (df.iat[2,1]/df.iat[2,3])/500+df.iat[2,2]]
df2.loc[3] = ["NW", (df.iat[3,1]/df.iat[3,3])/500+df.iat[3,2]]
df2.loc[4] = ["SE", (df.iat[4,1]/df.iat[4,3])/500+df.iat[4,2]]
df2.loc[5] = ["SW", (df.iat[5,1]/df.iat[5,3])/500+df.iat[5,2]]
df2.loc[6] = ["W", (df.iat[6,1]/df.iat[6,3])/500+df.iat[6,2]]
df2.loc[7] = ["WC", (df.iat[7,1]/df.iat[7,3])/500+df.iat[7,2]]
df = df.merge(df2, on='AREA')
df.head()

# Output the indexes of each area in a map using Basemap
fig, ax = plt.subplots(figsize=(10, 20))
m = Basemap(resolution='f',  # c, l, i, h, f or None
            projection='merc',
            lat_0=51.525, lon_0=-0.11,
            llcrnrlon=-0.35, llcrnrlat=51.4, urcrnrlon=0.13, urcrnrlat=51.65)
m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2', lake_color='#46bcec')
m.drawcoastlines()
m.readshapefile('uk_postcode_bounds/Areas', 'areas')
df_poly = pd.DataFrame({
    'shapes': [Polygon(np.array(shape), True) for shape in m.areas],
    'AREA': [area['name'] for area in m.areas_info]
})
df_poly = df_poly.merge(df, on='AREA', how='left')
cmap = plt.get_cmap('Oranges')
pc = PatchCollection(df_poly.shapes, zorder=2)
norm = Normalize()
pc.set_facecolor(cmap(norm(df_poly['INDEX'].fillna(0).values)))
ax.add_collection(pc)
mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
mapper.set_array(df_poly['INDEX'])
plt.colorbar(mapper, shrink=0.4)
plt.show()


