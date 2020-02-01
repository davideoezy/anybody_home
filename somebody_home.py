
import time
import arpreq
import paho.mqtt.client as mqtt


class anybody_home():
    def __init__(self):
        self.devices = 4
        self.last_seen_prev = [(time.time() - 7200)] * self.devices

    def whos_home(self):

        home_list = [(time.time(), 0)] * self.devices

        for ip in range(0, self.devices):
            test = arpreq.arpreq('192.168.0.' + str(ip+51))
            if test is not None:
                home_list[ip] = time.time(), 1

        return home_list

    def last_time_seen(self, current_reading):

        last_seen = [0] * self.devices

        for ip in range(0, self.devices):
            if current_reading[ip][1] == 1:
                last_seen[ip] = time.time()
            elif current_reading[ip][1] == 0:
                last_seen[ip] = self.last_seen_prev[ip]

        return last_seen

    def time_since_seen(self, last_seen):

        duration = [0] * self.devices

        for ip in range(0, self.devices):
            duration[ip] = round((time.time() - last_seen[ip])/60)
            if duration[ip] > 999:
                duration[ip] = 999

        return duration



if __name__ == "__main__":

    anybody_home = anybody_home()

    # ---------------- Initialise variables ------------------

    topic = "home/inside/sensor/"
    measurement = "presence"

    # Broker details:
    server_address="192.168.0.10" 
    client = mqtt.Client("docker_anybody_home")
    client.connect(server_address, keepalive=60)

    while True:
        home_list_curr = anybody_home.whos_home()

        last_seen_curr = anybody_home.last_time_seen(
            home_list_curr)

        time_since_connected = anybody_home.time_since_seen(last_seen_curr)

        anybody_home.last_seen_prev = last_seen_curr[:]

        #reading = "%s dev_1=%s,dev_2=%s,dev_3=%s,dev_4=%s" % (measurement, time_since_connected[0], time_since_connected[1], time_since_connected[2], time_since_connected[3])
        
        #dict_msg = {"dev_1":time_since_connected[0], "dev_2":time_since_connected[1], "dev_3":time_since_connected[2], "dev_4":time_since_connected[3]}
        for i in range(1:5):
            device = "device_" + str(i)
            topic_device = topic + device
            dict_msg = {device:time_since_connected[i]}
            msg = json.dumps(dict_msg)
            print(msg)

            client.publish(topic_device,msg)

        time.sleep(30)

# create table anybody_home (anybody_home int, dev_1 float, dev_2 float, dev_3 float, dev_4 float, ts timestamp);
