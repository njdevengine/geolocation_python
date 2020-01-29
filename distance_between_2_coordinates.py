import pandas as pd
import geocoder
import geopy.distance

#import csv remove NAN
df = pd.read_csv("mapping.csv",encoding = "ISO-8859-1")
df = df.dropna(subset=['Address'])
df = df.dropna(subset=['City'])
df = df.dropna(subset=['State'])

#combine addresses
addresses = []
for i in range(len(list(df["Address"]))):
    address = str(list(df["Address"])[i])+" "+str(list(df["City"])[i])+" "+str(list(df["State"])[i])
    addresses.append(address)

#geocode the addresses
data = {}
for i in addresses:
    try:
        g = geocoder.bing(str(i), key="YOUR_KEY")
        data[i] = g
        print("grabbed",str(i))
    except:
        data[i] = "error"
        print("***   ERROR   ***",str(i))

#clean up json to generate coordinate list
c_list = []
for i in range(len(data)):
    c = data[list(data.keys())[i]].latlng
    c_list.append(c)

#get latitudes and longitudes
lats = []
lons = []
for i in c_list:
    la = i[0]
    lo = i[1]
    lats.append(la)
    lons.append(lo)

#generate dataframe of coordinates, lat,lon, address
d = {"coordinates":c_list,"address":list(data.keys()),"latitude":lats,"longitude":lons}
df2 = pd.DataFrame(data = d)

df2.to_csv("coordinates.csv")

all_cities = ["Wall Street New York, New York","Brooklyn, New York","Herald Square, New York", "Jersey City, New York",
             "Boca Raton, Florida","Miami, Florida", "Fort Lauderdale, Florida","Tampa, Florida","Orlando, Florida",
              "Atlanta, Georgia", "Washington D.C.", "Chicago, Illinoise","Denver, Colorado","Seattle Washington",
             "San Francisco, California","San Diego, California","Santa Monica, California","Los Angeles California",
             "Irvine California", "Las Vegas, Nevada","Phoenix Arizona", "Dallas Texas","Austin Texas","Houston Texas",
              "San Antonio Texas", "Philadelphia, Pennsylvania"]
a_data = {}
for i in all_cities:
    location = geocoder.bing(str(i), key="YOUR_KEY")
    a_data[i] = location
    
a_c_list = []
for i in range(len(a_data)):
    c = a_data[list(a_data.keys())[i]].latlng
    a_c_list.append(c)
lats = []
lons = []

for i in a_c_list:
    la = i[0]
    lo = i[1]
    lats.append(la)
    lons.append(lo)
    
d = {"coordinates":a_c_list,"address":list(a_data.keys()),"latitude":lats,"longitude":lons}
adf = pd.DataFrame(data = d)

#compare each city in upload to distances to selected cities
data_list = []

cities_array = []
lookup_array = []
distance_array = []

for x in range(len(df2)):
    for i in range(len(adf)):
        coords_1 = ((list(adf["latitude"])[i]),(list(adf["longitude"])[i]))
        coords_2 = ((list(df2["latitude"])[x]),(list(df2["longitude"])[x]))
        city = adf["address"][i]
        lookup_address = df2["address"][x]
        distance = (geopy.distance.distance(coords_1, coords_2).miles)
        cities_array.append(city)
        lookup_array.append(lookup_address)
        distance_array.append(distance)
        
d = {"city":cities_array,"address":lookup_array,"distance":distance_array}
output = pd.DataFrame(data = d)
output.to_csv('output.csv')

ndf = output
ndf = ndf[ndf.distance <=30]

ndf.groupby(by="city").count().sort_values(by="distance",ascending=False).to_csv("special_cities.csv")
# view your dataframe
ndf.groupby(by="city").count().sort_values(by="distance",ascending=False)
