import openrouteservice
from geopy.geocoders import Nominatim
from emission import get_emission
import folium
import uuid 
import os 

def get_route_data(origin,destination, mode):
    geolocator = Nominatim(user_agent="eco_app")
    loc1 = geolocator.geocode(origin)
    loc2 = geolocator.geocode(destination)

    if not loc1 or not loc2:
      return {
        'start':origin,
        'end': destination,
        'mode': mode,
        'distance': 0,
        'duration': 0,
        'emission': 0,
        'map_file': None
    }


    client = openrouteservice.Client(key='Secret_Key')
    coords = ((loc1.longitude, loc1.latitude), (loc2.longitude, loc2.latitude))
    route = client.directions(coords, profile=mode, format='geojson')

    distance_km = route['features'][0]['properties']['segments'][0]['distance'] / 1000
    duration_min = route['features'][0]['properties']['segments'][0]['duration'] / 60
    emission = get_emission(distance_km, mode)

   
    m = folium.Map(location=[(loc1.latitude + loc2.latitude)/2, (loc1.longitude + loc2.longitude)/2], zoom_start=13)
    folium.GeoJson(route, name='route').add_to(m)
    filename = f"map_{uuid.uuid4().hex}.html"
    filepath = os.path.join("static",'maps',filename)
    m.save(filepath)


    return {
    'start': origin,
    'end': destination,
    'mode': mode,
    'distance': round(distance_km, 2),
    'duration': round(duration_min, 2),
    'emission': emission,
    'map_file': filename 
    }

