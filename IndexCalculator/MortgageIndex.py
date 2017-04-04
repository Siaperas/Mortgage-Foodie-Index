from sqlalchemy import *
import pandas as pd
from matplotlib import pyplot
from statsmodels.tsa.stattools import adfuller

# Function to plot and calculate the stationarity of each area's lending
def test_stationarity(timeseries):
    # Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    # Plot rolling statistics:
    orig = pyplot.plot(timeseries, color='blue', label='Original')
    mean = pyplot.plot(rolmean, color='red', label='Rolling Mean')
    std = pyplot.plot(rolstd, color='black', label='Rolling Std')
    pyplot.legend(loc='best')
    pyplot.title('Rolling Mean & Standard Deviation')
    # Change to True in order to plot
    pyplot.show(block=False)
    # Perform Dickey-Fuller test:
    print 'Results of Dickey-Fuller Test:'
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print dfoutput


db = create_engine('sqlite:///lending.db')
metadata = MetaData(db)

lending = Table('lending', metadata, autoload=True)
connection = db.connect()
#recover the sum of each quarter of each area
resoverall = connection.execute("SELECT Area"
                                ",SUM(Q2_2013) AS SUM_Q2_2013"
                                ",SUM(Q3_2013) AS SUM_Q3_2013"
                                ",SUM(Q4_2013) AS SUM_Q4_2013"
                                ",SUM(Q1_2014) AS SUM_Q1_2014"
                                ",SUM(Q2_2014) AS SUM_Q2_2014"
                                ",SUM(Q3_2014) AS SUM_Q3_2014"
                                ",SUM(Q4_2014) AS SUM_Q4_2014"
                                ",SUM(Q1_2015) AS SUM_Q1_2015"
                                ",SUM(Q2_2015) AS SUM_Q2_2015"
                                ",SUM(Q3_2015) AS SUM_Q3_2015"
                                ",SUM(Q4_2015) AS SUM_Q4_2015"
                                ",SUM(Q1_2016) AS SUM_Q1_2016"
                                ",SUM(Q2_2016) AS SUM_Q2_2016  FROM lending GROUP BY Area")
df = pd.DataFrame(resoverall.fetchall())
df.columns = resoverall.keys()
print df
# Convert DataFrame to timeseries
df=df.T.reset_index().reindex(columns=[0,1,2,3,4,5,6,7])
df=df.ix[1:]
df=df.rename(columns = {0:'E',1:'EC',2:'N',3:'NW',4:'SE',5:'SW',6:'W',7:'WC'})
df.insert(0, 'Date', ['2013-06-01','2013-09-01','2013-12-01','2014-03-01','2014-06-01','2014-09-01','2014-12-01',
                      '2015-03-01', '2015-06-01', '2015-09-01', '2015-12-01','2016-03-01','2016-06-01'])
df['Date']=pd.to_datetime(df['Date'], format="%Y-%m-%d")
df[['E','EC','N','NW','SE','SW','W','WC']]=df[['E','EC','N','NW','SE','SW','W','WC']].astype(float)
print df
df = df.set_index('Date')

# Plot the lending numbers for each area through the quarters
f = pyplot.figure(figsize=(10, 10)) # Change the size as necessary
df.plot(ax=f.gca()) # figure.gca means "get current axis"
pyplot.title('Mortgage Index', color='black')
pyplot.show()

# print stationarity test
for i in df:
    test_stationarity(df[i])

