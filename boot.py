import network
sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

sta.active(True)
ap.active(False)

import ujson

contents = open('credentials.json').read()

credo = ujson.loads(contents)
name = credo['wifi_name']
pswd = credo['wifi_password']
sta.connect(name, pswd)

print(sta.ifconfig())