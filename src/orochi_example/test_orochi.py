import os
import unittest
from time import sleep

import requests

from orochi_python.orochi import Orochi

class OrochiExampleTest(unittest.TestCase):

    def setUp(self):
        self.base_path =  os.path.join(os.path.dirname(__file__), "../../scripts/")
        self.orochi = Orochi()
        self.orochi.start(timeout=10)
    

    def tearDown(self):
         self.orochi.shutdown_proxies()
         self.orochi.terminate()
        

    def test_pass_through_proxy(self):
        name = "proxy-1"
        backends = {"remote-addr": "127.0.0.1", "server-port": "8000"}
        front_port = 8081
        command = {"setup": self.base_path + "setup.sh",
                   "command": self.base_path + "command.sh 8000 " + self.base_path,
                   "started-check": self.base_path + "../venv/bin/python " + self.base_path + "started-check.py http://127.0.0.1:8000/README.md",
                   "teardown": self.base_path + "teardown.sh 8000"}

        self.orochi.add_pass_through_proxy(name, backends, front_port, command)
        
        res = requests.get('http://127.0.0.1:{}/README.md'.format(front_port))
        self.assertEqual(res.status_code, 200)

        proxy = self.orochi.get_proxy(name)
        req = proxy['actions']
        self.assertEqual(len(req), 3)
        self.assertEqual(req[2]['body'][:8], '# orochi')

    def test_mock_proxy(self):
        name = "proxy-1"
        backends = {"remote-addr": "127.0.0.1", "server-port": "8000"}
        # front_port = 8081


        # self.orochi.add_pass_through_proxy(name, backends, front_port, command)

    
    def test_web_hook_proxy(self):

        wh_name = "proxy-web-hook"
        wh_backends =  {"request-time": {"timing": "during", "delay": 2000},
                     "request": {"method": "get",
                               "url": "http://127.0.0.1:8081/LICENSE.md"},
                     "response": {"status": 200,
                                "body": "canned"}}
        wh_front_port = 8082
        wh_command = {}
        self.orochi.add_web_hook_proxy(wh_name, wh_backends, wh_front_port, wh_command)
        proxy = self.orochi.get_proxy(wh_name)
        req = proxy['actions']

        pt_name = "proxy-1"
        pt_backends = {"remote-addr": "127.0.0.1", "server-port": "8001"}
        pt_front_port = 8081
        pt_command = {"setup": self.base_path + "setup.sh",
                   "command": self.base_path + "command.sh 8001 " + self.base_path,
                   "started-check": self.base_path + "../venv/bin/python " + self.base_path + "started-check.py http://127.0.0.1:8001/LICENSE.md",
                   "teardown": self.base_path + "teardown.sh 8001"}

        self.orochi.add_pass_through_proxy(pt_name, pt_backends, pt_front_port, pt_command)        

        res = requests.get('http://127.0.0.1:{}/foo_bar'.format(wh_front_port))
        self.assertEqual(res.status_code, 200)

        sleep(1)

        pt_proxy = self.orochi.get_proxy(pt_name)
        pt_req = pt_proxy['actions']
        
        self.assertEqual(len(pt_req), 3)
        self.assertEqual(pt_req[2]['body'][:8], 'The MIT ')


        wh_proxy = self.orochi.get_proxy(wh_name)
        wh_req = wh_proxy['actions']

        self.assertEqual(len(wh_req), 4)
        self.assertEqual(wh_req[3]['body'], 'canned')

        
