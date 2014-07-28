import os
import sys
import httplib
import base64
import json
import new
import unittest
import sauceclient
from selenium import webdriver
from sauceclient import SauceClient

# based on http://saucelabs.com/examples/example.py

USERNAME = os.environ.get('SAUCE_USERNAME')
ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')
sauce = SauceClient(USERNAME, ACCESS_KEY)

browsers = [{"platform": "Mac OS X 10.9",
             "browserName": "chrome",
             "version": "31"}]

def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)
    return decorator


@on_platforms(browsers)
class SauceSampleTest(unittest.TestCase):
    def setUp(self):
        self.desired_capabilities['name'] = self.id()

        sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_capabilities,
            command_executor=sauce_url % (USERNAME, ACCESS_KEY)
        )
        self.driver.implicitly_wait(30)

    def test_hello(self):
        self.driver.get('localhost:5000')
        assert 'Hello' in self.driver.page_source

    def tearDown(self):
        print("Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id)
        try:
            if sys.exc_info() == (None, None, None):
                sauce.jobs.update_job(self.driver.session_id, passed=True)
            else:
                sauce.jobs.update_job(self.driver.session_id, passed=False)
        finally:
            self.driver.quit()
