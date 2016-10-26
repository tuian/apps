import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

GC_Path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver"


class LoingTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(GC_Path)
        self.driver.get("http://www.facebook.com")

    def test_Login(self):
        driver = self.driver
        facebook_username = "ar.ranjithkumar@gmail.com"
        facebook_password = "facebook1998"

        emailFieldID = "email"
        passFieldID = "pass"
        loginButton_xPath = "//*[@value='Log In']"
        fbLogo_xPath = "//*[@id='blueBarDOMInspector']/div[1]/div/div/div/div[1]/div[1]/h1/a/span"

        emailFieldIDElement = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_id(emailFieldID))
        passFieldIDElement  = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_id(passFieldID))
        loginButtonElement  = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(loginButton_xPath))

        emailFieldIDElement.clear()
        emailFieldIDElement.send_keys(facebook_username)
        passFieldIDElement.clear()
        passFieldIDElement.send_keys(facebook_password)
        loginButtonElement.click()
        WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_xpath(fbLogo_xPath))
        print "Found the logo"

    def tearDown(self):
        #self.driver.quit()
        print "tearDown"

if __name__ == "__main__":
    unittest.main()





