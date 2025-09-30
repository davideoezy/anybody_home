from ubiquiti.unifi import API as Unifi_API
import json
import paho.mqtt.client as mqtt
import time


class anybody_home():
    def __init__(self):
        self.n_devices = 4
        self.dev_1 = '192.168.0.51'
        self.dev_2 = '192.168.0.52'
        self.dev_3 = '192.168.0.53'
        self.dev_4 = '192.168.0.54'
        self.devices = ['192.168.0.51','192.168.0.52','192.168.0.53','192.168.0.54']
        self.last_seen_prev = [(time.time() - 7200)] * self.n_devices

    def time_seen(self, dev_list):     
        #last_seen = [0] * self.n_devices

        max_devices = len(dev_list)

        for i in range(0,max_devices):
            for j in range(0,self.n_devices):
                try:
                    if dev_list[i]['ip'] == self.devices[j]:
                        self.last_seen_prev[j] = device_list[i]['last_seen']
                
                except:
                    continue

    def time_since_seen(self):

        duration = [0] * self.n_devices

        for i in range(0, self.n_devices):
            duration[i] = round((time.time() - self.last_seen_prev[i])/60)
            if duration[i] > 999:
                duration[i] = 999

        return duration
    

    def anybody_home(self, last_seen_curr):
        somebody_home = 0

        if any(t < 20 for t in last_seen_curr):
            somebody_home = 1

        return somebody_home

if __name__ == "__main__":

    anybody_home = anybody_home()

    topic = "home/inside/sensor/presence"

    # Broker details:
    server_address="192.168.0.10" 
    client = mqtt.Client("docker_anybody_home")
    client.connect(server_address, keepalive=60)

    while True:

        api = Unifi_API(username="ubnt", password="ubnt", baseurl="unifi.bomfunk.blue", verify_ssl=False)
        api.login()
        device_list = (api.list_clients(order_by="ip"))
        api.logout()

        anybody_home.time_seen(device_list)

        last_seen_curr = anybody_home.time_since_seen()

        somebody_home = anybody_home.anybody_home(last_seen_curr)

        dict_msg = {"somebody_home": somebody_home, "dev_1":last_seen_curr[0], "dev_2":last_seen_curr[1], "dev_3":last_seen_curr[2], "dev_4":last_seen_curr[3]}

        msg = json.dumps(dict_msg)

        client.publish(topic,msg)

        time.sleep(30)