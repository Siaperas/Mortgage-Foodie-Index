import pandas as pd
from sqlalchemy import *

# Create a database using the file Leding. The databse will be holding info for each postcode's lending in the London area.
df = pd.read_excel(open('Lending.xlsx','rb'), skiprows=1, sheetname='CML time series')

df=df.loc[df['Area'].isin(['E','EC','N','NW','SE','SW','W','WC'])]
df=df.dropna()
df = df.drop('Area name', 1)
df = df.drop('Region', 1)
df=df.rename(columns = {'2013 Q2':'Q2_2013','2013 Q3':'Q3_2013','2013 Q4':'Q4_2013',
                        '2014 Q1': 'Q1_2014', '2014 Q2': 'Q2_2014', '2014 Q3': 'Q3_2014',
                        '2014 Q4': 'Q4_2014', '2015 Q1': 'Q1_2015', '2015 Q2': 'Q2_2015',
                        '2015 Q3': 'Q3_2015', '2015 Q4': 'Q4_2015', '2016 Q1': 'Q1_2016',
                        '2016 Q2': 'Q2_2016'})
print df
engine = create_engine('sqlite:///lending.db')
df.to_sql('lending', engine, if_exists='replace')
