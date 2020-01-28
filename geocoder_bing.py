import geocoder
data = {}
for i in addresses:
    try:
        g = geocoder.bing(str(i), key="YOUR_API_KEY")
        data[i] = g
        print("grabbed",str(i))
    except:
        data[i] = "error"
        print("***   ERROR   ***",str(i))

        
#bulk geocoder
g = geocoder.bing(addresses, method='batch',key="YOUR_API_KEY")
for result in g:
    try:
        print(result.latlng)
    except:
        print("error")
