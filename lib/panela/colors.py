import os
import json

COLORS_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'colors.json')
COLOR_TABLE = json.loads(open(COLORS_JSON, 'r').read())
VALID_COLORS = [x['hexString'] for x in COLOR_TABLE]
HEX_TO_ANSI = {x['hexString']:x['colorId'] for x in COLOR_TABLE}

def rgb_from_str(s):
    # s starts with a #.  
    r, g, b = int(s[1:3],16), int(s[3:5], 16),int(s[5:7], 16)  
    return r, g, b 

def find_nearest_color(hex_color):  
    R, G, B = rgb_from_str(hex_color)
    mindiff = None
    for d in VALID_COLORS:  
        r, g, b = rgb_from_str(d)  
        diff = abs(R -r)*256 + abs(G-g)* 256 + abs(B- b)* 256   
        if mindiff is None or diff < mindiff:  
            mindiff = diff  
            mincolorname = d  
    return mincolorname 


