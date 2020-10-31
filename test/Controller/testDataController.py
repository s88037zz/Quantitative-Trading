from src.Controller.DataController import DataController
import unittest, os, time
from selenium import webdriver


class TestDataController(unittest.TestCase):
    def setUp(self):
        self.controller = DataController(os.path.join("..", "..", "src", "chromedriver"))
        self.driver = self.controller.driver

    def testLogin(self):
        self.controller.login()
        time.sleep(2)
        user = self.driver.find_elements_by_xpath('//*[@class="myAccount topBarText"]')
        self.assertTrue(user)

    def testDonwloadSP500(self):
        self.controller.login()
        self.controller.downlow_SP500("2019/01/01", "2020/01/01")

        self.driver.get("chrome://downloads/")
        item = self.driver.execute_script("""
            var manger = document.querySelector('downloads-manager').shadowRoot;
            var item = manger.querySelector('downloads-item');
            return item
        """)
        print(item)
        self.assertTrue(item)

    def testGetDownloadProgress(self):
        self.driver.get(self.controller.url)
        progress = self.controller.getDownloadProgress()
        self.assertFalse(progress)

