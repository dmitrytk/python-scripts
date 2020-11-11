import os
import googlemaps

gmaps = googlemaps.Client(key=os.environ['MAP_API_KEY'])


for i in range(2):
    res = gmaps.elevation(locations=(60+i, 60+i))[0]
    print(res['elevation'])
