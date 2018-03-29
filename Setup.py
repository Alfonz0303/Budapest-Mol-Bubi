import urllib.request, urllib.parse, urllib.error
import json 
import requests
import math


class location():
    # getting the latitude and the longitude of your 'starting/ending' point
    # using google geocode api
    def lat1_long1(location):
        serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
        while True:
            address = location
            if len(address) < 1: 
                break
            key = ' ' # <= apiKey for Geocode
            url = serviceurl + urllib.parse.urlencode(
                {'address': address, 'key': key})

            uh = urllib.request.urlopen(url)
            data = uh.read().decode()            

            try:
                js = json.loads(data)
            except:
                js = None

            if not js or 'status' not in js or js['status'] != 'OK':
                print('==== Failure To Retrieve ====')
                print(data)
                continue
            lat1 = js["results"][0]["geometry"]["location"]["lat"]
            lng1 = js["results"][0]["geometry"]["location"]["lng"]
            return lat1, lng1 #locations coordinate
                                
    def distance(lat1, long1, lat2, long2):
    # counting the distance between your location and the closest mol bubi station
    # mol bubi stations info in the mol_bubi.txt file => from https://api.citybik.es/v2/networks/bubi
    # Using here the 'haversine’ formula:
    #                                   https://www.movable-type.co.uk/scripts/latlong.html
    #                                   https://en.wikipedia.org/wiki/Haversine_formula  
        R = 6317
        rad_lat1 = math.radians(lat1)
        rad_long1 = math.radians(long1)
        rad_lat2 = math.radians(lat2)
        rad_long2 = math.radians(long2)
        
        distance = math.acos(math.sin(rad_lat1) * math.sin(rad_lat2) + math.cos(rad_lat1) * math.cos(rad_lat2) * math.cos(rad_long1-rad_long2)) * R
        return distance


class closest(location):
    # calculating the closest mol bubi station
    def bubi(coordinate):
        fh = open("mol_bubi.txt") #stations info in mol_bubi.txt
        bubi = []
        for sor in fh:
            sor = sor.rstrip().split(',')
            bubi.append(sor)
        fh.close()

        coordinate = location.lat1_long1(coordinate)
        x = coordinate[0]
        y = coordinate[1]

        di = {}
        station_name = []
        distance_bubi = []

        for elem in bubi:
            z = location.distance(x, y, float(elem[1]), float(elem[2])) 
            station_name.append(elem[0])
            distance_bubi.append(z)

        di = dict(zip(station_name, distance_bubi)) # two list in one dict

        name = None 
        smallest = float(20)

        for k, v in di.items():
            if smallest > v:
                smallest = v
                name = k
        return name, di[name]

class bike(closest):
    def info(address):
        # getting the stations info
        url = 'https://api.citybik.es/v2/networks/bubi' #open source api from https://api.citybik.es/v2/networks
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()

        try:
            js = json.loads(data)
        except:
            js = None
        
        network = js['network']['stations']
        for net in network:  
            if net['name'] == address:
                lat1 = net['latitude']
                long1 = net['longitude']
                empty_slots1 = net['empty_slots']
                free_bikes1 = net['free_bikes']
        return empty_slots1, free_bikes1,  lat1, long1

class destination_bubi(bike):
    # coutning the destination between the two closest mol bubi station with google distance matrix
    # in the distance matrix I used 'walking mode', and the shortest route
    # from that distance I have count the duration in minutes on a hypotesis that you are able to ride the bike with an average 15km/h
    #

    def far_away(lat1, long1, lat2, long2): 
        start = (str(lat1) + "," + str(long1))
        end = ("|" + str(lat2) + "," + str(long2))

        serviceurl = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        o = 1
        while o <= 1:
            if len(start) < 1: 
                break
            if len(end) < 1: 
                break
            key = " " # <=apiKey for Distance matrix

            url = serviceurl + urllib.parse.urlencode({'units': 'metric', 'origins': start, 'destinations': end, 'key':key, 'mode': 'walking'})
            uh = urllib.request.urlopen(url)
            data = uh.read().decode()
            
            try:
                js = json.loads(data)
            except:
                js = None

            if not js or 'status' not in js or js['status'] != 'OK':
                print('==== Failure To Retrieve ====')
                print(data)
                continue


            # this is a hypotesis
            for i in js['rows']:
                for j in i['elements']:   
                    sec = j['distance']['value']
                    time = sec / 250 # hypotesis example: 15 km/h; 19 min 12 sec (19,1 min); 4,8 km => means that you can ride 250 meter in 1 minute
                    duration = time # minutes
                    Distance1 = j['distance']['text'] # the distance between the two mol bubui station
                    o +=1
        return Distance1, duration