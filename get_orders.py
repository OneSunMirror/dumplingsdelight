import json
import requests
from optimize_route import find_route
from requests.auth import HTTPBasicAuth
#from get_secret import get_dumpling_secret
def retreive_orders(secrets):
    id = list(secrets.keys())[0]
    key = list(secrets.values())[0]
    site = '3ef608c7-e534-454c-bf72-feca1095dbcc'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': key,
        'wix-account-id': id,
        'wix-site-id': site,
    }
    #auth = HTTPBasicAuth(list(secrets.keys())[0], list(secrets.values())[0])
    #f.write(auth)
    json_data = {
        'query': {
            'filter': '{"paymentStatus": "PAID"}',
            'paging': {
                'limit': 100,
            },
            'sort': '[{"number": "desc"}]',
        },
    }
    response = requests.post('https://www.wixapis.com/stores/v2/orders/query', headers=headers, json=json_data)
    #for c in response.iter_lines():
    #    f.write(c)
    return response

def gen_routes(locations, optimum_route):
    source_link = "www.google.com/maps/dir/?api=1&waypoints="
    last_start = ""
    routes = []
    l = len(locations)
    for x in range(1, l, 10):
        link = source_link + last_start
        last_y = x
        for y in range(x, min(x+10, l)-1):
            last_start = locations[optimum_route[y]] + "%7C"
            if locations[optimum_route[y]] !=  locations[optimum_route[y-1]]:
                link = link  + locations[optimum_route[y]] + "%7C"
            last_y = y+1
        link = link + "&destination=" + locations[optimum_route[last_y]]
        link = link.replace(" ","%2C")
        link = link.replace(",","")
        routes.append(link)
    return routes


origin = "Sanctuary Lakes Shopping Centre, 300 Point Cook Rd, Point Cook VIC 3030"
locations = [origin]
f = open("orders_list.txt", "x", encoding="utf-8")
#secrets = get_dumpling_secret()
secrets = {"0e38bd38-e49b-487d-bbf1-f2a6a1e10549":"IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjNjZmI0MGFkLTIyNGItNGM2Yy04OGVjLTg3Y2QxNTFmNWRmMVwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcIjZmOTlkMjdjLWU2NWQtNDMyMi1iNjY0LWIzMzE4ZWViYmJlOFwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCIwZTM4YmQzOC1lNDliLTQ4N2QtYmJmMS1mMmE2YTFlMTA1NDlcIn19IiwiaWF0IjoxNjkwOTc1NTAzfQ.k56pNNwuVHQXKfgMXoh2PJGraKjJwglvIi8XOMQu4gt3Ri3XYQ2w04V5YyUh-Cxwax5WpIvn7goLqyMWIvNcUejevn-TgB0H0mu7y6bCnTYaJWdtKdZ7oc71zR5gEhdz-KC3Ok-p0VT7g2Jc2TbCrVMEFUR55qZGCK1LCkFg9g2gXYfl-c-z4yl818BbhpZts8h0CtjPYht5fZi3wIUsdDxbgRPjNfKvRHMIu5MyhX6_JtcSVzp-25nJSM6sPrOKA8P1xku_KeVUyjkc-VPuyH61eGDiXGNjW9AXLpU232ncS9MbNk2CzVO1vgxhzCZX8kbwXhRCVku_xLp-wjQKbA"}
orders = json.loads(retreive_orders(secrets).content)
tot_orders = {}
for order in orders['orders']:
    add_dict = order['shippingInfo']['shipmentDetails']['address']
    add = add_dict['addressLine1']
    if 'addressLine2' in add_dict:
        add = add + " " + add_dict['addressLine2']
    add = add + ", " + add_dict['city'] + ", " + add_dict['zipCode']
    locations.append(add)
    #map_route = map_route + "/" + add


optimum_route = find_route(locations, 'duration')
optimum_route.append(0)
map_route = gen_routes(locations, optimum_route) 
#print(map_route)

f.write("\n\n\n")
f.write("Google Map Link Best Route by Time taken:\n")
for m in map_route:
    f.write(m)
    f.write("\n")

#optimum_route = find_route(locations, 'distance')
#locations.append(origin)
#optimum_route.append(0)
#map_route = gen_routes(locations, optimum_route)

#f.write("\n\n\n")
#f.write("Google Map Link Best Route by Distance travelled:\n")
#for m in map_route:
#    f.write(m)
#    f.write("\n")

c = 1
f.write("\n\n\n")
for i in orders['orders']:
    order = orders['orders'][optimum_route[c]-1]
    c = c +1
    f.write("Order no: " +  str(order['number']))
    f.write("\n\n")
    for item in order['lineItems']:
        f.write(item['name'] + " Order: " + str(item['quantity']))
        if item['name'] in tot_orders:  
            tot_orders[item['name']] = tot_orders[item['name']] + item['quantity']
        else:
            tot_orders[item['name']] =  item['quantity']
        f.write("\n")
    f.write("\n")
    f.write("Address: " + locations[optimum_route[c-1]])
    f.write("\n")
    f.write("Phone: " + order['shippingInfo']['shipmentDetails']['address']['phone'] + "\n")    
    f.write("-------------------------\n")

f.write("Total Orders: \n")
for tot in tot_orders:
    f.write(tot + "   Total Order: " + str(tot_orders[tot]) + "\n")    









f.close()

