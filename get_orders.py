import json
import requests
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
map_route = "www.google.com/maps/dir"
f = open("orders_list.txt", "x", encoding="utf-8")
#secrets = get_dumpling_secret()
secrets = {"0e38bd38-e49b-487d-bbf1-f2a6a1e10549":"IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjNjZmI0MGFkLTIyNGItNGM2Yy04OGVjLTg3Y2QxNTFmNWRmMVwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcIjZmOTlkMjdjLWU2NWQtNDMyMi1iNjY0LWIzMzE4ZWViYmJlOFwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCIwZTM4YmQzOC1lNDliLTQ4N2QtYmJmMS1mMmE2YTFlMTA1NDlcIn19IiwiaWF0IjoxNjkwOTc1NTAzfQ.k56pNNwuVHQXKfgMXoh2PJGraKjJwglvIi8XOMQu4gt3Ri3XYQ2w04V5YyUh-Cxwax5WpIvn7goLqyMWIvNcUejevn-TgB0H0mu7y6bCnTYaJWdtKdZ7oc71zR5gEhdz-KC3Ok-p0VT7g2Jc2TbCrVMEFUR55qZGCK1LCkFg9g2gXYfl-c-z4yl818BbhpZts8h0CtjPYht5fZi3wIUsdDxbgRPjNfKvRHMIu5MyhX6_JtcSVzp-25nJSM6sPrOKA8P1xku_KeVUyjkc-VPuyH61eGDiXGNjW9AXLpU232ncS9MbNk2CzVO1vgxhzCZX8kbwXhRCVku_xLp-wjQKbA"}
orders = json.loads(retreive_orders(secrets).content)
tot_orders = {}
for order in orders['orders']:
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
    add_dict = order['shippingInfo']['shipmentDetails']['address']
    add = add_dict['addressLine1']
    if 'addressLine2' in add_dict:
        add = add + " " + add_dict['addressLine2']
    add = add + ", " + add_dict['city'] + ", " + add_dict['zipCode']
    map_route = map_route + "/" + add
    f.write("Address: " + add)
    f.write("\n")
    f.write("Phone: " + add_dict['phone'] + "\n")    
    f.write("-------------------------\n")
f.write("Total Orders: \n")
for tot in tot_orders:
    f.write(tot + "   Total Order: " + str(tot_orders[tot]) + "\n")    
map_route = map_route.replace(" ","+")
map_route = map_route.replace(",","")
f.write("\n\n\n")
f.write("Google Map Link:\n")
f.write(map_route)
f.close()
