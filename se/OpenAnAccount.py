import sys,time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

reload(sys)
sys.setdefaultencoding('utf8')

GV_Google_ChromeDriver_Path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver"


def login():
    driver = webdriver.Chrome(GV_Google_ChromeDriver_Path)
    driver.get("https://uat1.panoramaadviser.com.au")
    print driver.current_url
    print driver.title
    driver.maximize_window()

    # username_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_elements(By.ID,"login_username"))
    # username_element[0].send_keys("201664770")

    username_element = WebDriverWait(driver,10).until(lambda driver: driver.find_element_by_id("login_username"))
    username_element.send_keys("201664770")

    #driver.execute_script("document.getElementById('login_username').value='201664770'")

    password_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("login_entered_password"))
    password_element.send_keys("nextgen02")
    #driver.execute_script("document.getElementById('login_entered_password').value='nextgen02'")

    next_button_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_elements(By.NAME,"logon"))
    # next_button_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath("//*[@id='jq-logon']/form/fieldset/ul/li[3]/div/button"))
    #print next_button_element.tag_name

    # next_button_element.click()
    next_button_element[0].click()
    #driver.execute_script("document.getElementsByName('logon')[0].click()")

    # gotit_button_element = WebDriverWait(driver, 10).until(lambda driver: driver.find_elements(By.CLASS_NAME,"btn  btn-action btn-action-primary ready"))
    # gotit_button_element[0].click()
    if(driver.execute_script("document.getElementsByClassName('btn btn-action btn-action-primary ready')[0]") <> None):
        driver.execute_script("document.getElementsByClassName('btn btn-action btn-action-primary ready')[0].click()")

    time.sleep(15)
    print "Nagivating to Open an account page"
    driver.get("https://uat1.panoramaadviser.com.au/ng/secure/app/#ng/newaccount/accounttype")
    time.sleep(1)

    # print type(driver.find_elements(By.XPATH, "//*[@name='producttype']/option[3]"))
    list_iframe = driver.find_elements(By.TAG_NAME, "iframe")
    for iframe in list_iframe:
        print "Tag Name", iframe.tag_name
        print "Attribute_ID",iframe.get_attribute("id")
        print "Attribute_Name",iframe.get_attribute("name")

    driver.switch_to.frame(driver.find_element(By.NAME,value="BT_PANORAMA_ip"))
    print driver.current_url
    print driver.current_window_handle
    print driver.name

    #driver.switch_to.default_content()
    #print driver.find_elements(By.XPATH, "//*[contains(@id,'input-select-view')]")
    print driver.find_elements(By.TAG_NAME, "iframe")


    list_select = driver.find_elements(By.TAG_NAME, "select")
    for item in list_select:
        print "Tag Name", item.tag_name, item.is_selected()
        print "Attribute_ID", item.get_attribute("id")
        print "Attribute_Name", item.get_attribute("name")

    print "The one needed:",list_select[0].get_attribute("name")

    select = Select(list_select[0])

    print select.options[2].tag_name,select.options[2].get_attribute("value")
    print select.options[2].tag_name, select.options[2].is_selected()
    select.options[2].tag_name, select.options[2].click()
    #print [o.text for o in select.options]  # these are string-s
    #select.select_by_visible_text("BT Panorama Investments")

    #driver.execute_script("document.getElementsByClassName('btn btn-action btn-action-primary ready')[0].click()")
    #(document.getElementsByClassName("form-element")[0]).getElementsByTagName("select")[0].options.selectedIndex
    #driver.execute_script("(document.getElementsByClassName('form-element')[0]).getElementsByTagName('select')[0].options.selectedIndex = 1")

    time.sleep(300)

if __name__ == "__main__":
    login()
