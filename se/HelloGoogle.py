import time
from selenium import webdriver

GC_Path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver"
driver = webdriver.Chrome(GC_Path)

driver.get('http://www.google.com/xhtml');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('Chrome Driver')
#search_box.
search_box.submit()
# time.sleep(5) # Let the user actually see something!
# driver.quit()