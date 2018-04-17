import math

def distance(start, end):
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

def inRoad (start, end, point, width):
    width = width / 2
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