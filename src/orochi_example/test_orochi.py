import unittest

import requests

from orochi_python.orochi import Orochi

class OrochiExampleTest(unittest.TestCase):

    def setUp(self):
        self.orochi = Orochi()
        self.orochi.start()

    def tearDown(self):
        self.orochi.shutdown_proxies()
        self.orochi.terminate()
        

    def test_test(self):
        base_path = "/Users/underplank/projects/orochi-example/scripts/"

        name = "proxy-1"
        backends = {"remote-addr": "127.0.0.1", "server-port": "8000"}
        front_port = 8081
        command = {"setup": base_path + "setup.sh",
                   "command": base_path + "command.sh 8000",
                   "started-check": base_path + "../venv/bin/python " + base_path + "started-check.py http://127.0.0.1:8000/README.md",
                   "teardown": base_path + "teardown.sh"}

        self.orochi.add_proxy(name, backends, front_port, command)
        
        res = requests.get('http://127.0.0.1:{}/README.md'.format(front_port))
        self.assertEqual(res.status_code, 200)

        proxy = self.orochi.get_proxy(name)
        req = proxy['requests']
        self.assertEqual(len(req), 1)
        self.assertEqual(req[0]['response']['body'], u'# orochi-example\nThis is an example python repo that uses orochi\n')
        

        
