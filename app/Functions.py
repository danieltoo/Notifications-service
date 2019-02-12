import math

def pointOnZone(x, y, polygon):
    """ This function caculate if the point is inside the polygon"""
    i = 0
    j = len(polygon) - 1
    salida = False
    for i in range(len(polygon)):
        if (polygon[i][1] < y and polygon[j][1] >= y) or (polygon[j][1] < y and polygon[i][1] >= y):
            if polygon[i][0] + (y - polygon[i][1]) / (polygon[j][1] - polygon[i][1]) * (polygon[j][0] - polygon[i][0]) < x:
                salida = not salida
        j = i
    return salida  

def distance(start, end):
    """ This function calculate the distance between two points"""
    rlat0 = math.radians(start[0])
    rlng0 = math.radians(start[1])
    rlat1 = math.radians(end[0])
    rlng1 = math.radians(end[1])
    latDelta = rlat1 - rlat0
    lonDelta = rlng1 - rlng0
    distance = 6371000 * 2 * math.asin(
        math.sqrt(
            math.cos(rlat0) * math.cos(rlat1) * math.pow(math.sin(lonDelta / 2), 2) +
            math.pow(math.sin(latDelta / 2), 2)
        )
    )
    return distance 

def inSegment (start, end, point, width):
    """ This function calculate if the point is in one segment of  the roadSegment"""
    area  = (distance(start, end) * width) / 2
    a = distance (start, point)
    b = distance (point, end)
    c = distance (start, end)
    s = (( a + b + c ) / 2)
    ap = math.sqrt(
        (s * (s - a ) ) * ( ( s - b ) * ( s - c ) )
    )
    if (ap < area) : 
        return True 
    else: 
        return False

def inRoadSegment (polyline, point, width) :
    """ This function determine if the point is inthe segment """
    width = width / 2
    isOnRoad = False
    for i in range(len(polyline)):
        if inSegment(polyline[i][0], polyline[i][1], point, width):
            isOnRoad = True
    return isOnRoad


def determinateZone (location, zones):
    """ This function determinate the zone where the point is"""
    inzone = {}
    for zone in zones:  
        loc = location.split(',')
        point = pointOnZone (float(loc[0]), float(loc[1]), zone["location"] )
        if (point) : 
            inzone = zone
            print ("Alerta sucitada en ", zone["name"])
    return inzone

