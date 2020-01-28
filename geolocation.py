from geopy.geocoders import Nominatim
import pandas as pd

#geolocator = Nominatim()
#location = geolocator.geocode("345 Chambers Street New York") 
#print((location.latitude, location.longitude)) 

geolocator = Nominatim()

df = pd.read_csv("mapping.csv",encoding = "ISO-8859-1")

df = df.dropna(subset=['Address'])
df = df.dropna(subset=['City'])
df = df.dropna(subset=['State'])

coords = {}
for i in range(len(list(df["Address"]))):
    address = str(list(df["Address"])[i])+" "+str(list(df["City"])[i])+" "+str(list(df["State"])[i])
    try:
        location = geolocator.geocode(address) 
        coords[i] = [location.latitude,location.longitude]
        print((address, location.latitude, location.longitude))
    except:
        print(address,"error")
