from selenium import webdriver
from selenium.webdriver import ActionChains
import time, os


class DataController(object):
    def __init__(self):
        self.url = "https://hk.investing.com/etfs/spdr-s-p-500-historical-data"
        self.save_path = os.path.abspath(os.path.join("..", "..", "data"))
        self.driver_path = os.path.abspath(os.path.join(os.path.pardir, 'chromedriver'))
        self.driver = self.get_driver()
        self.email = "s88037zz@gmail.com"
        self.passwd = 's88037zz'

    def login(self):
        self.driver.get(self.url)

        elem_login = self.driver.find_element_by_xpath("//*[@class='login bold']")
        elem_login.click()
        time.sleep(1)

        # find the elements
        elem_email = self.driver.find_element_by_xpath("//*[@id='loginFormUser_email']")
        elem_passwd = self.driver.find_element_by_xpath("//*[@id='loginForm_password']")
        for elem in self.driver.find_elements_by_xpath("//a[@class='newButton orange']"):
            if elem.text == '登入' or elem.text == 'login':
                elem_login_btn = elem

        # set user info and click login button
        elem_email.send_keys(self.email)
        elem_passwd.send_keys(self.passwd)
        self.driver.execute_script("arguments[0].click()", elem_login_btn)
        time.sleep(2)

    def hover(self, element):
        ActionChains(self.driver).move_to_element(element).perform()

    def get_driver(self):
        options = self.get_chrome_options()
        driver = webdriver.Chrome(executable_path=self.driver_path, options=options)
        return driver

    def get_chrome_options(self):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0,
                 'download.default_directory': self.save_path,
                 'directory_upgrade': True}
        options.add_experimental_option('prefs', prefs)
        return options

    def downlow_SP500(self, start_date, end_date):
        self.driver.get(self.url)
        time.sleep(2)

        # open the date window
        elem_date_picker = self.driver.find_elements_by_xpath("//*[@id='datePickerIconWrap']")[1]
        self.driver.execute_script("arguments[0].click();", elem_date_picker)

        # change the start and end date
        elem_start_date = self.driver.find_element_by_xpath("//*[@id='startDate']")
        elem_start_date.clear()
        elem_start_date.send_keys(start_date)
        elem_end_date = self.driver.find_element_by_xpath("//*[@id='endDate']")
        elem_end_date.clear()
        elem_end_date.send_keys(end_date)
        time.sleep(2)
        elem_apply = self.driver.find_element_by_xpath("//*[@id='a"
                                                       "pplyBtn']")
        elem_apply.click()
        time.sleep(2)

        # download data
        elem_download = self.driver.find_element_by_xpath("//*[@title='下載數據']")
        elem_download.click()
        while self.getDownloadProgress():
            time.sleep(3)
        self.driver.get("chrome://downloads/")
        print("Download successfully")

    def getDownloadProgress(self):
        self.driver.get("chrome://downloads/")
        progress = self.driver.execute_script("""
            try{
                var tag = document.querySelector('downloads-manager').shadowRoot;
                var intag = tag.querySelector('downloads-item').shadowRoot;
                var progress_tag = intag.getElementById('progress');
                var progress = null;
                if(progress_tag) {
                    progress = progress_tag.value;
                }
                 return progress;            
            }
            catch(e){
                return null;
            }
        """)

        return progress


if __name__ == '__main__':
    dc = DataController()
    dc.login()
    dc.downlow_SP500('1970/01/01', '2020/10/21')
