

def get_emission(distance_km, mode):
    factors = {
        'driving-car': 192,    
        'cycling-regular': 21,
        'foot-walking': 0
    }
    return round(distance_km * factors.get(mode, 0) / 1000, 3)  
