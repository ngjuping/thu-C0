from selenium import webdriver
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#Login setup
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"
baseurl = "https://next.xuetangx.com/"
login_xpaths = {
    "entrance":"//*[@id=\"app\"]/div/div[1]/div/div[1]/div/div/div/div[1]/div[2]/div/span",
    "switch":"//*[@id=\"app\"]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/img",
    "login_by_mail":"//*[@id=\"app\"]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/ul/li[3]",
    "mail":"//*[@id=\"app\"]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[3]/form/div[1]/div/div/input",
    "pwd":"//*[@id=\"app\"]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[3]/form/div[2]/div/div/input",
    "submit":"//*[@id=\"app\"]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]"
}
login_credentials = {
    "mail":"ngjuping2018@163.com",
    "pwd":"NJP05141999njp"
}


#Actual work
courses_xpaths = {
    "profile_img":"[@class='header-login']",
    "my_courses":"html/body/div[3]/div[1]/ul/li[3]/div",
    "PE_course_entrance":"//*[@id=\"app\"]/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div[2]/div[3]/div",
}
targeturl = "https://next.xuetangx.com/learn/thu04011002684/thu04011002684/1520527/exercise"
template = "//*[@id=\"app\"]/div/div[2]/div[1]/div[1]/div[2]/div/ul[{}]/li[4]"
question_xpaths = [template.format(i) for i in range(1,15)]
#questions_urls = [3081359,1485934,3081362,3160861,3160862]
question_xpaths.insert(0,0)
for i in range(0,15):
    print(question_xpaths[i])
next_btn_xpath = "//*[@id=\"app\"]/div/div[2]/div[1]/div[2]/div/div[1]/div[1]/i[2]"

#Starts chrome browser
mydriver = webdriver.Chrome('./chromedriver.exe',desired_capabilities=caps) 
mydriver.get(baseurl)
mydriver.maximize_window()

try:
    wait = WebDriverWait(mydriver, 120)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, login_xpaths["entrance"])))

#mydriver.implicitly_wait(10) # seconds
finally:
    mydriver.find_element_by_xpath(login_xpaths["entrance"]).click()
    mydriver.find_element_by_xpath(login_xpaths["switch"]).click()
    mydriver.find_element_by_xpath(login_xpaths["login_by_mail"]).click()
    mydriver.find_element_by_xpath(login_xpaths["mail"]).send_keys(login_credentials["mail"])
    mydriver.find_element_by_xpath(login_xpaths["pwd"]).send_keys(login_credentials["pwd"])
    time.sleep( 10 )
    mydriver.find_element_by_xpath(login_xpaths["submit"]).click()
    time.sleep(20)
    mydriver.get("https://next.xuetangx.com/my-courses/current")
    wait = WebDriverWait(mydriver, 30)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, courses_xpaths["PE_course_entrance"])))
    element.click()
    time.sleep(20)
    
    mydriver.find_element_by_xpath(question_xpaths[1]).click()