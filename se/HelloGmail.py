# -*- coding: utf-8 -*-
'''
Demandbase , Add this, Google tag manager, Bluekai

http://selenium-python.readthedocs.io/locating-elements.html
http://www.w3schools.com/xml/xpath_intro.asp

webDriver.Close() - Close the browser window that the driver has focus of
webDriver.Quit() - Calls dispose
webDriver.Dispose() Closes all browser windows and safely ends the session

'''
import sys,time
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

reload(sys)
sys.setdefaultencoding('utf8')

GV_Google_ChromeDriver_Path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver"


def printPageInfo_ByPage_URL(page):
    driver = webdriver.Chrome(GV_Google_ChromeDriver_Path)
    driver.get(page)
    # print "",driver.

    # Driver properties
    print "Page Details:"
    print "Current URL: ",driver.current_url
    print "Page Title",driver.title
    #print "Window Size", driver.get_window_size('current')
    driver.maximize_window()
    #print "Window Size",driver.get_window_size('current')
    #print "Cookies",driver.get_cookies()
    #print "Application Cache", driver.application_cache
    #print "Deleting cookies", driver.delete_all_cookies()
    #print "Cookies", driver.get_cookies()

    # Find all input control elements on the page

    #list_input_fields = driver.find_elements(by=By.XPATH,value="//*[@type='text']")
    #list_input_fields = driver.find_elements(by=By.XPATH,value="//*") #all tags in a html file
    #list_input_fields = driver.find_elements(by=By.XPATH, value="//*[@id='formBlock']/fieldset/*[@type='text' or @type='textarea' or @type='select-one' or @type='radio' or @type='password']")
    #list_input_fields = driver.find_elements(by=By.XPATH, value="//*[@id='formBlock']/fieldset/*[self::input or self::textarea or self::select]")
    list_input_fields = driver.find_elements(by=By.XPATH, value="//*[self::input[@type='text' or @type='radio' or @type='password' or @type='checkbox' or @type='hidden' or @type='button' or @type='submit'] or self::textarea or self::select]")

    #list_input_fields = driver.find_elements(by=By.TAG_NAME,value='input')
    #form[@name='ct100']/*
    #print type(list_input_fields)
    print "Web Elements - Input :"
    element_count = 0
    # Loop through the elements and print information
    for item in list_input_fields:
        element_count = element_count + 1
        # print "Tag_Name              :", item.tag_name
        # print "Text                  :", item.text
        # print "ID                    :", item.id
        # print "parent                :", item.parent
        # print "is_enabled            :", item.is_enabled()
        # print "is_selected           :", item.is_selected()
        # print "is_displayed          :", item.is_displayed()
        # print "location_s_view       :", item.location_once_scrolled_into_view
        # print "size                  :", item.size
        # print "location              :", item.location
        # print "rect                  :", item.rect # works only for image, to ge the size and location
        #
        # print "Get Attribute (type)  :", item.get_attribute('type')
        # print "Get Attribute (name)  :", item.get_attribute('name')
        # print "Get Attribute (id)    :", item.get_attribute('id')
        # print "Get Attribute (Value) :", item.get_attribute('value')



        print "{} | Tag_Name: {} | Type: {} | Attribute_Name: {} | Attribute_ID: {} | Attribute_Value: {} "\
            .format(element_count,item.tag_name,
            item.get_attribute('type'),
            item.get_attribute('name'),
            item.get_attribute('id'),
                    item.get_attribute('value'))


def printPageInfo_ByPage_iFrame(page,by_what,iframe_class_name):
    driver = webdriver.Chrome(GV_Google_ChromeDriver_Path)
    driver.get(page)
    # print "",driver.

    #driver.switch_to().frame(driver.find_element(By.CLASS_NAME,value="iframeheight"))
    driver.switch_to.frame(driver.find_element(by_what,iframe_class_name))
    # Driver properties
    print "Page Details:"
    print "Current URL: ",driver.current_url
    print "Page Title",driver.title
    #print "Window Size", driver.get_window_size('current')
    driver.maximize_window()
    #print "Window Size",driver.get_window_size('current')
    #print "Cookies",driver.get_cookies()
    #print "Application Cache", driver.application_cache
    #print "Deleting cookies", driver.delete_all_cookies()
    #print "Cookies", driver.get_cookies()

    # Find all input control elements on the page

    #list_input_fields = driver.find_elements(by=By.XPATH,value="//*[@type='text']")
    #list_input_fields = driver.find_elements(by=By.XPATH,value="//*") #all tags in a html file
    #list_input_fields = driver.find_elements(by=By.XPATH, value="//*[@id='formBlock']/fieldset/*[@type='text' or @type='textarea' or @type='select-one' or @type='radio' or @type='password']")
    #list_input_fields = driver.find_elements(by=By.XPATH, value="//*[@id='formBlock']/fieldset/*[self::input or self::textarea or self::select]")
    list_input_fields = driver.find_elements(by=By.XPATH,value="//*[self::input[@type='text' or @type='radio' or @type='password' or @type='checkbox' or @type='hidden' or @type='button' or @type='submit'] or self::textarea or self::select]")

    #list_input_fields = driver.find_elements(by=By.TAG_NAME,value='input')
    #form[@name='ct100']/*
    #print type(list_input_fields)
    print "Web Elements - Input :"
    element_count = 0
    # Loop through the elements and print information
    for item in list_input_fields:
        element_count = element_count + 1
        # print "Tag_Name              :", item.tag_name
        # print "Text                  :", item.text
        # print "ID                    :", item.id
        # print "parent                :", item.parent
        # print "is_enabled            :", item.is_enabled()
        # print "is_selected           :", item.is_selected()
        # print "is_displayed          :", item.is_displayed()
        # print "location_s_view       :", item.location_once_scrolled_into_view
        # print "size                  :", item.size
        # print "location              :", item.location
        # print "rect                  :", item.rect # works only for image, to ge the size and location
        #
        # print "Get Attribute (type)  :", item.get_attribute('type')
        # print "Get Attribute (name)  :", item.get_attribute('name')
        # print "Get Attribute (id)    :", item.get_attribute('id')
        # print "Get Attribute (Value) :", item.get_attribute('value')

        print "{} | Tag_Name: {} | Type: {} | Attribute_Name: {} | Attribute_ID: {} | Attribute_Value: {} "\
            .format(element_count,item.tag_name,
            item.get_attribute('type'),
            item.get_attribute('name'),
            item.get_attribute('id'),
            item.get_attribute('value'))

    driver.switch_to.default_content()
    driver.quit()




def createEmailAccount():

    driver = webdriver.Chrome(GV_Google_ChromeDriver_Path)
    #driver.execute_script("document.getElementsByClassName('comment-user')[0].click()")
    driver.get("https://accounts.google.com/SignUp")

    # Page properties
    print "Page Details:"
    print "Current URL: ", driver.current_url
    print "Page Title:", driver.title

    firstname_value = "Rambopythonboyfirst1"
    lastname_value  = "Rambopythonboysecond"
    username_value = "Rambopythonboyfs1"
    password_value = "PyRambo153"
    day_value = "11"
    month_value = "01"
    year_value = "1981"
    gender_value = "MALE"
    phone_value = "466450415"
    signupidvinput_value="466450415"

    firstname_id       = "FirstName"
    lastname_id        = "LastName"
    username_id        = "GmailAddress"
    password_id        = "Passwd"
    passwordAgain_id   = "PasswdAgain"
    day_id             = "BirthDay"
    month_id           = "HiddenBirthMonth"
    year_id            = "BirthYear"
    gender_id          = "HiddenGender"
    phone_id           = "RecoveryPhoneCountry"
    signupidvinput_id  = "signupidvinput"

    loginButton_id = "submitbutton"
    iagreeButton_id = "iagreebutton"
    signupidvcontinueButton_id = "next-button"

    loginButton_xPath = "//*[@value='Next step']"
    iagreeButton_xPath = "//*[@value='I agree']"
    signupidvcontinueButton_xpath = "//*[@value='Continue']"
    #fbLogo_xPath = "//*[@id='blueBarDOMInspector']/div[1]/div/div/div/div[1]/div[1]/h1/a/span"

    firstname_Element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(firstname_id))
    lastname_Element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(lastname_id))
    username_Element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(username_id))
    password_Element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(password_id))
    passwordAgain_Element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passwordAgain_id))
    day_Element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(day_id))
    month_Element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(month_id))
    year_Element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(year_id))
    gender_Element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(gender_id))
    phone_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(phone_id))

    loginButtonElement  = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(loginButton_id))
    iagreeButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(iagreeButton_id))

    # loginButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(loginButton_xPath))
    # iagreeButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(iagreeButton_xPath))

    # firstname_Element.clear()
    # lastname_Element.clear()
    # username_Element.clear()
    # password_Element.clear()
    # passwordAgain_Element.clear()
    # day_Element.clear()
    # month_Element.clear()
    # year_Element.clear()
    # gender_Element.clear()

    firstname_Element.send_keys(firstname_value)
    lastname_Element.send_keys(lastname_value)
    username_Element.send_keys(username_value)
    password_Element.send_keys(password_value)
    passwordAgain_Element.send_keys(password_value)

    driver.execute_script("document.getElementById('HiddenBirthMonth').value='01'")
    #driver.execute_script("alert(document.getElementById('HiddenBirthMonth').value)")
    #month_Element.send_keys(month_value)
    day_Element.send_keys(day_value)
    year_Element.send_keys(year_value)
    #gender_Element.send_keys(gender_value)
    driver.execute_script("document.getElementById('HiddenGender').value='MALE'")
    #driver.execute_script("alert(document.getElementById('HiddenGender').value)")
    #phone_element.send_keys(phone_value)

    #wait = ui.WebDriverWait(driver, 60)  # timeout after 10 seconds
    #wait.until(loginButtonElement.click())
    loginButtonElement.click()
    driver.execute_script("document.getElementById('iagreebutton').disabled = false")
    iagreeButtonElement.click()
    print driver.current_url
    #driver.get("https://accounts.google.com/UserSignUpIdvChallenge")
    print driver.current_url

    signupidvInputElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(signupidvinput_id))
    signupidvcontinueButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(signupidvcontinueButton_id))

    #signupidvcontinueButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(signupidvcontinueButton_xpath))

    signupidvInputElement.send_keys(signupidvinput_value)
    signupidvcontinueButtonElement.click()
    time.sleep(300)
    driver.close()

def loginToGmail():
    driver = webdriver.Chrome(GV_Google_ChromeDriver_Path)
    driver.get("http://mail.google.com")
    print driver.current_url
    print driver.title
    if(driver.title =="Gmail"):
        username_element = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_id("Email"))
        username_element.send_keys("arrkoz1@gmail.com")
        next_button_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("next"))
        next_button_element.click()
        password_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("Passwd"))
        password_element.send_keys("")
        signin_button_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("signIn"))
        signin_button_element.click()

        time.sleep(30)

#driver.quit()
if __name__ == "__main__":
    #createEmailAccount()
    printPageInfo_ByPage_URL("https://uat1.panoramaadviser.com.au")
    # printPageInfo_ByPage_URL("http://107.20.135.69/contact.aspx")
    #printPageInfo_ByPage_iFrame("http://www.tcs.com/contact/Pages/default.aspx",By.CLASS_NAME,"iframeheight")
    #printPageInfo_ByPage_URL("https://accounts.google.com/SignUp")
#    loginToGmail()


