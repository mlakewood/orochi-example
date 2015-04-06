import requests
import subprocess
import json
from time import sleep

class Orochi(object):

    def __init__(self, path, port):
        self.path = path
        self.port = port
        self.orochi = None

    def start(self, timeout=5):
        self.orochi = subprocess.Popen(['java', '-jar', self.path, self.port])
        
        started = False
        sleep_count = 0
        while not started:
            try:
                response = requests.get('http://127.0.0.1:{}'.format(self.port))
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException:
                sleep_count += 1
                if sleep_count < timeout:
                    sleep(1)
                else:
                    break
        return self.orochi        
        
    def add_proxy(self, name, backend, front_port, command):
        request = {"name": name,
                   "backend": backend, 
                   "front-port": front_port,
                   "command": command}
        
        response = requests.post("http://127.0.0.1:{}/proxy".format(self.port), data=json.dumps(request))
        return response

    def get_proxy(self, name):
        response = requests.get("http://127.0.0.1:{}/proxy/{}".format(self.port, name))
        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        return false
                                
    
    def shutdown_proxies(self):
        requests.delete("http://127.0.0.1:{}/proxy".format(self.port))

    def terminate(self):
        self.orochi.terminate()
