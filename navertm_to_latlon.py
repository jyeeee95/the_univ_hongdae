import pandas as pd
from pyproj import Proj
from pyproj import transform

# https://gist.github.com/allieus/1180051/ab33229e820a5eb60f8c7971b8d1f1fc8f2cfabb

WGS84 = { 'proj':'latlong', 'datum':'WGS84', 'ellps':'WGS84', }

TM128 = { 'proj':'tmerc', 'lat_0':'38N', 'lon_0':'128E', 'ellps':'bessel',
   'x_0':'400000', 'y_0':'600000', 'k':'0.9999',
   'towgs84':'-146.43,507.89,681.46'}


def tm128_to_wgs84(x, y):
    return transform( Proj(**TM128), Proj(**WGS84), x, y )


def mapdata_refining(map_dataframe):
    for index, location in map_dataframe.iterrows():
        if location['longitude'] > 150:
            if location['latitude'] > 40:
                x, y = tm128_to_wgs84(location['longitude'], location['latitude'])
        else:
            x, y = location['longitude'], location['latitude']

        map_dataframe.at[index, 'longitude'] = x
        map_dataframe.at[index, 'latitude'] = y
    return map_dataframe

############################################################################################

itaewon_2012_3rd = pd.read_csv("data/itaewon/itaewon_2012_3rd.csv", encoding = 'utf-8')
itaewon_2012_4th = pd.read_csv("data/itaewon/itaewon_2012_4th.csv", encoding = 'utf-8')

itaewon_2013_1st = pd.read_csv("data/itaewon/itaewon_2013_1st.csv", encoding = 'utf-8')
itaewon_2013_2nd = pd.read_csv("data/itaewon/itaewon_2013_2nd.csv", encoding = 'utf-8')
itaewon_2013_3rd = pd.read_csv("data/itaewon/itaewon_2013_3rd.csv", encoding = 'utf-8')
itaewon_2013_4th = pd.read_csv("data/itaewon/itaewon_2013_4th.csv", encoding = 'utf-8')

itaewon_2014_1st = pd.read_csv("data/itaewon/itaewon_2014_1st.csv", encoding = 'utf-8')
itaewon_2014_2nd = pd.read_csv("data/itaewon/itaewon_2014_2nd.csv", encoding = 'utf-8')
itaewon_2014_3rd = pd.read_csv("data/itaewon/itaewon_2014_3rd.csv", encoding = 'utf-8')
itaewon_2014_4th = pd.read_csv("data/itaewon/itaewon_2014_4th.csv", encoding = 'utf-8')

itaewon_2015_1st = pd.read_csv("data/itaewon/itaewon_2015_1st.csv", encoding = 'utf-8')
itaewon_2015_2nd = pd.read_csv("data/itaewon/itaewon_2015_2nd.csv", encoding = 'utf-8')
itaewon_2015_3rd = pd.read_csv("data/itaewon/itaewon_2015_3rd.csv", encoding = 'utf-8')
itaewon_2015_4th = pd.read_csv("data/itaewon/itaewon_2015_4th.csv", encoding = 'utf-8')

itaewon_2016_1st = pd.read_csv("data/itaewon/itaewon_2016_1st.csv", encoding = 'utf-8')
itaewon_2016_2nd = pd.read_csv("data/itaewon/itaewon_2016_2nd.csv", encoding = 'utf-8')
itaewon_2016_3rd = pd.read_csv("data/itaewon/itaewon_2016_3rd.csv", encoding = 'utf-8')
itaewon_2016_4th = pd.read_csv("data/itaewon/itaewon_2016_4th.csv", encoding = 'utf-8')

itaewon_2017_1st = pd.read_csv("data/itaewon/itaewon_2017_1st.csv", encoding = 'utf-8')
itaewon_2017_2nd = pd.read_csv("data/itaewon/itaewon_2017_2nd.csv", encoding = 'utf-8')
itaewon_2017_3rd = pd.read_csv("data/itaewon/itaewon_2017_3rd.csv", encoding = 'utf-8')
itaewon_2017_4th = pd.read_csv("data/itaewon/itaewon_2017_4th.csv", encoding = 'utf-8')

itaewon_2018_1st = pd.read_csv("data/itaewon/itaewon_2018_1st.csv", encoding = 'utf-8')
itaewon_2018_2nd = pd.read_csv("data/itaewon/itaewon_2018_2nd.csv", encoding = 'utf-8')

############################################################################################

itaewon_2012_3rd = mapdata_refining(itaewon_2012_3rd)
itaewon_2012_4th = mapdata_refining(itaewon_2012_4th)

itaewon_2013_1st = mapdata_refining(itaewon_2013_1st)
itaewon_2013_2nd = mapdata_refining(itaewon_2013_2nd)
itaewon_2013_3rd = mapdata_refining(itaewon_2013_3rd)
itaewon_2013_4th = mapdata_refining(itaewon_2013_4th)

itaewon_2014_1st = mapdata_refining(itaewon_2014_1st)
itaewon_2014_2nd = mapdata_refining(itaewon_2014_2nd)
itaewon_2014_3rd = mapdata_refining(itaewon_2014_3rd)
itaewon_2014_4th = mapdata_refining(itaewon_2014_4th)

itaewon_2015_1st = mapdata_refining(itaewon_2015_1st)
itaewon_2015_2nd = mapdata_refining(itaewon_2015_2nd)
itaewon_2015_3rd = mapdata_refining(itaewon_2015_3rd)
itaewon_2015_4th = mapdata_refining(itaewon_2015_4th)

itaewon_2016_1st = mapdata_refining(itaewon_2016_1st)
itaewon_2016_2nd = mapdata_refining(itaewon_2016_2nd)
itaewon_2016_3rd = mapdata_refining(itaewon_2016_3rd)
itaewon_2016_4th = mapdata_refining(itaewon_2016_4th)

itaewon_2017_1st = mapdata_refining(itaewon_2017_1st)
itaewon_2017_2nd = mapdata_refining(itaewon_2017_2nd)
itaewon_2017_3rd = mapdata_refining(itaewon_2017_3rd)
itaewon_2017_4th = mapdata_refining(itaewon_2017_4th)

itaewon_2018_1st = mapdata_refining(itaewon_2018_1st)
itaewon_2018_2nd = mapdata_refining(itaewon_2018_2nd)

############################################################################################

itaewon_2012_3rd.to_csv("data/itaewon/itaewon_2012_3rd.csv", index = False, mode='w')
itaewon_2012_4th.to_csv("data/itaewon/itaewon_2012_4th.csv", index = False, mode='w')

itaewon_2013_1st.to_csv("data/itaewon/itaewon_2013_1st.csv", index = False, mode='w')
itaewon_2013_2nd.to_csv("data/itaewon/itaewon_2013_2nd.csv", index = False, mode='w')
itaewon_2013_3rd.to_csv("data/itaewon/itaewon_2013_3rd.csv", index = False, mode='w')
itaewon_2013_4th.to_csv("data/itaewon/itaewon_2013_4th.csv", index = False, mode='w')

itaewon_2014_1st.to_csv("data/itaewon/itaewon_2014_1st.csv", index = False, mode='w')
itaewon_2014_2nd.to_csv("data/itaewon/itaewon_2014_2nd.csv", index = False, mode='w')
itaewon_2014_3rd.to_csv("data/itaewon/itaewon_2014_3rd.csv", index = False, mode='w')
itaewon_2014_4th.to_csv("data/itaewon/itaewon_2014_4th.csv", index = False, mode='w')

itaewon_2015_1st.to_csv("data/itaewon/itaewon_2015_1st.csv", index = False, mode='w')
itaewon_2015_2nd.to_csv("data/itaewon/itaewon_2015_2nd.csv", index = False, mode='w')
itaewon_2015_3rd.to_csv("data/itaewon/itaewon_2015_3rd.csv", index = False, mode='w')
itaewon_2015_4th.to_csv("data/itaewon/itaewon_2015_4th.csv", index = False, mode='w')

itaewon_2016_1st.to_csv("data/itaewon/itaewon_2016_1st.csv", index = False, mode='w')
itaewon_2016_2nd.to_csv("data/itaewon/itaewon_2016_2nd.csv", index = False, mode='w')
itaewon_2016_3rd.to_csv("data/itaewon/itaewon_2016_3rd.csv", index = False, mode='w')
itaewon_2016_4th.to_csv("data/itaewon/itaewon_2016_4th.csv", index = False, mode='w')

itaewon_2017_1st.to_csv("data/itaewon/itaewon_2017_1st.csv", index = False, mode='w')
itaewon_2017_2nd.to_csv("data/itaewon/itaewon_2017_2nd.csv", index = False, mode='w')
itaewon_2017_3rd.to_csv("data/itaewon/itaewon_2017_3rd.csv", index = False, mode='w')
itaewon_2017_4th.to_csv("data/itaewon/itaewon_2017_4th.csv", index = False, mode='w')

itaewon_2018_1st.to_csv("data/itaewon/itaewon_2018_1st.csv", index = False, mode='w')
itaewon_2018_2nd.to_csv("data/itaewon/itaewon_2018_2nd.csv", index = False, mode='w')
