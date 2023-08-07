import requests
import googlemaps
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
from googlemaps import distance_matrix
url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
map_api_key = "AIzaSyDILOATa9jdhX1tQqsYiS-ALgKSzZ6pesM"


def get_matrix(src, dest, x, y, master_mat, type):
    gmaps = googlemaps.Client(key=map_api_key)
    l_src = len(src)
    l_dest = len(dest)
    print(x, "-" , y)
    if l_src > 10:
        master_mat[x:x+10, y::] = get_matrix(src[0:10], dest, x, y, master_mat, type)[x:x+10, y::]
        master_mat[x+10::, y::] = get_matrix(src[10::], dest, x + 10, y, master_mat, type)[x+10::, y::]
    elif l_dest > 10:
        master_mat[x::, y:y+10] = get_matrix(src,dest[0:10], x, y, master_mat, type)[x::, y:y+10]
        master_mat[x::, y+10::] = get_matrix(src,dest[10::], x, y + 10, master_mat, type)[x::, y+10::]
    else:
        d_mat_json = gmaps.distance_matrix(src, dest)
        #print("...")
        #print(d_mat_json)
        i = 0
        for r in d_mat_json['rows']:
            row = [0] * l_src
            j = 0
            for c in r['elements']:
                master_mat[x+i,y+j] = c[type]['value']
                j = j + 1
            i = i + 1
    return master_mat
    


def find_route(locations, type):
    gmaps = googlemaps.Client(key=map_api_key)
    print(locations)
    main_len= len(locations)
    main_mat = np.matrix(np.zeros([main_len,main_len])) 
    main_mat = get_matrix(locations, locations, 0, 0, main_mat, type)
    #d_mat_json = gmaps.distance_matrix(locations, locations)
   
    permutation, distance = solve_tsp_dynamic_programming(np.asmatrix(main_mat))
    
    return permutation