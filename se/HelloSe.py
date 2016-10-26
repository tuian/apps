from selenium import webdriver

GC_Path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver"
driver = webdriver.Chrome(GC_Path)

driver.get("http://www.tcs.com/")

driver.quit()
