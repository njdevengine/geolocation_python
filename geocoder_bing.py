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
