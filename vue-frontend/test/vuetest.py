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
baseurl = "http://localhost:8081/"
login_xpaths = {
    "username":"""//*[@id="login_panel"]/form/div[1]/input""",
    "pwd":"""//*[@id="login_panel"]/form/div[2]/input""",
    "submit":"""//*[@id="login_panel"]/form/button[1]"""
}

booking_xpaths = {
    'showvenues':"""//*[@id="menu"]/div/li/a""",
    'getlastvenue':"""(//*[@id="menu"]/div/li/div/a)[1]""",
    # div[35] = 26th day of month,
    'selectDay':"""//*[@id="app"]/div[1]/div[3]/div[1]/div[1]/div/div/div[2]/div[37]/div/span""",
    # 3rd period of day
    'selectTime':"""/html/body/div/div[1]/div[5]/div[1]/div[2]/div/div[1]/div/div[7]""", 
    
    'book':"""//*[@id="app"]/div[1]/div[5]/div[1]/div[3]/button""",
    'checkResv':"""/html/body/div[2]/div/div[3]/button[1]""",
    'clickSelect':"""//*[@id="swal2-content"]/select""",
    'offline':"""//*[@id="swal2-content"]/select/option[2]""",
    "offlineOK":"""/html/body/div[2]/div/div[3]/button[1]""",
    'pay':"""/html/body/div[2]/div/div[3]/button[1]"""
}

payment_xpaths = {
    'username':"""//*[@id="J_tLoginId"]""",
    'password':"""//*[@id="payPasswd_rsainput"]""",
    'submit':"""//*[@id="J_newBtn"]"""
}

payment_credentials = {
    "mail":"wmnlvo1425@sandbox.com",
    "pwd":"111111"
}

share_xpath = {
    'manage': """//*[@id="menu"]/div/a[1]""",
    'shares': """//*[@id="menu"]/div/a[2]""",
    'create':"""//*[@id="app"]/div[1]/div[3]/div[3]/div/div[1]/div[2]/form/div[2]/div/div[1]""",
    'focus':"""/html/body/div[1]/div[1]/div[3]/div[3]/div/div[2]/div/div/div[2]/div/div[1]/div/div[2]/div/p""",
    'submit':"""/html/body/div[1]/div[1]/div[3]/div[3]/div/div[2]/div/div/div[2]/div/div[2]/button""",
    'update':"""//*[@id="app"]/div[1]/div[3]/div[3]/div/div[1]/div[2]/form/div[3]/div[2]/div[1]""",
    'delete':"""//*[@id="app"]/div[1]/div[3]/div[3]/div/div[1]/div[2]/form/div[3]/div[2]/div[2]""",
    "confirmDelete":"""/html/body/div[2]/div/div[3]/button[1]""",
    'closeModal':"""//*[@id="share_modal-125"]/div/div/div[1]/button"""
}

feedback_xpath = {
    'manage': """//*[@id="menu"]/div/a[1]""",
    'feedback': """//*[@id="menu"]/div/a[3]""",
    'create':'//*[@id="app"]/div[1]/div[3]/div[3]/div/div[1]/div[2]/form/div[2]/div',
    'focus':"""/html/body/div[1]/div[1]/div[3]/div[3]/div/div[3]/div/div/div[2]/div/div[1]/div/div[2]/div/p""",
    'submit':"""/html/body/div[1]/div[1]/div[3]/div[3]/div/div[3]/div/div/div[2]/div/div[3]/button""",
    'update':"""//*[@id="app"]/div[1]/div[3]/div[3]/div/div[1]/div[2]/form/div[2]/div[2]/div[1]""",
    'delete':"""//*[@id="app"]/div[1]/div[3]/div[3]/div/div[1]/div[2]/form/div[2]/div[2]/div[2]""",
    "confirmDelete":"""/html/body/div[2]/div/div[3]/button[1]""",
    'uploadFile':"""/html/body/div[1]/div[1]/div[3]/div[3]/div/div[3]/div/div/div[2]/div/input""",
    'uploadFilePath':'D:\\thu-c0\\vue-frontend\\test\\feedbacktestjpg.jpg',
    'closeModal':"""/html/body/div[1]/div[1]/div[3]/div[3]/div/div[3]/div/div/div[1]/button""",
    '4star':"""/html/body/div[1]/div[1]/div[3]/div[3]/div/div[3]/div/div/div[2]/div/div[2]/div/div[2]/span[4]"""

}

#Starts chrome browser
mydriver = webdriver.Chrome('./chromedriver.exe',desired_capabilities=caps) 

mydriver.get(baseurl)
mydriver.maximize_window()


wait = WebDriverWait(mydriver, 120)

# Login and insert username and pwd
wait.until(EC.element_to_be_clickable((By.XPATH, login_xpaths["username"]))).send_keys('2018080120')
wait.until(EC.element_to_be_clickable((By.XPATH, login_xpaths["pwd"]))).send_keys('123456')
wait.until(EC.element_to_be_clickable((By.XPATH, login_xpaths["submit"]))).click()
time.sleep(3)

# Click sequence to pick venue -> court -> time -> pay offline
wait.until(EC.element_to_be_clickable((By.XPATH, booking_xpaths["showvenues"]))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, booking_xpaths["getlastvenue"]))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, booking_xpaths["selectDay"]))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, booking_xpaths["selectTime"]))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, booking_xpaths["book"]))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, booking_xpaths["checkResv"]))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, booking_xpaths["clickSelect"]))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, booking_xpaths["offline"]))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, booking_xpaths["offlineOK"]))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, booking_xpaths["pay"]))).click()

# --------------------------- CREATE SHARE ---------------------------
# Go to my courts and create a share post
manageCourts = wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['manage'])))
manageCourts.click()
wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['create']))).click()
time.sleep(1)

# Click on textbox and ready to enter stuff
textbox = wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['focus'])))
# Very short input
textbox.send_keys("Hi")
# Try to submit
submit = wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['submit'])))
submit.click()
time.sleep(1)
# Very long input
textbox.send_keys(" this is selenium but it's too longggggggggggggggggggg ggggggggggggggggggggggggggg  gggggggggggggggggggggggggggggg")
# Try to submit
submit.click()
time.sleep(1)
# Need to clear previous data
textbox.clear()
textbox.send_keys(" this is selenium share")
# Final share post creation submit
submit.click()
time.sleep(10)

# --------------------------- UPDATE SHARE ---------------------------
# Go to shares page and check if new share post is there
allShares = wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['shares'])))
allShares.click()
time.sleep(5)
# Go back to manage court page
manageCourts.click()
# Click the update post button
wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['update']))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['focus']))).send_keys("update with selenium")
wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['submit']))).click()
time.sleep(10)
# Go to shares page and check if updated share post is there
allShares.click()
time.sleep(10)
# Go back to manage court page
manageCourts.click()

# --------------------------- DELETE SHARE ---------------------------

# Delete the share post
wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['delete']))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['confirmDelete']))).click()
time.sleep(5)


with open('../node_modules/timeshift-js/timeshift.js', 'r') as timeshift_js: 

    timeshiftjs = timeshift_js.read() 
    mydriver.execute_script(timeshiftjs)
    mydriver.execute_script("""
        Date = TimeShift.Date;
        TimeShift.setTime(1640455914000);
        """)

allShares = wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['shares'])))
allShares.click()
manageCourts = wait.until(EC.element_to_be_clickable((By.XPATH, share_xpath['manage'])))
manageCourts.click()

# --------------------------- CREATE FEEDBACK ---------------------------
wait.until(EC.element_to_be_clickable((By.XPATH, feedback_xpath['create']))).click()
print("Shit")
time.sleep(1)
# Click on textbox and ready to enter stuff
textbox = wait.until(EC.element_to_be_clickable((By.XPATH, feedback_xpath['focus'])))
# Very short input
textbox.send_keys("Hi")
# Try to submit
submit = wait.until(EC.element_to_be_clickable((By.XPATH, feedback_xpath['submit'])))
submit.click()
time.sleep(1)
# Very long input
textbox.send_keys(" this is selenium but it's too longggggggggggggggggggg ggggggggggggggggggggggggggg  gggggggggggggggggggggggggggggg")
# Try to submit
submit.click()
time.sleep(1)
# Clear input
textbox.clear()
# OK input
textbox.send_keys(" this is selenium")
# Last submit
submit.click()
time.sleep(10)
# Check if the feedback is created
allFeedbacks = wait.until(EC.element_to_be_clickable((By.XPATH, feedback_xpath['feedback'])))
allFeedbacks.click()
time.sleep(10)
# Come back to court manage page
manageCourts.click()

# --------------------------- UPDATE FEEDBACK ---------------------------
wait.until(EC.element_to_be_clickable((By.XPATH, feedback_xpath['update']))).click()
textbox = wait.until(EC.element_to_be_clickable((By.XPATH, feedback_xpath['focus'])))
textbox.send_keys("update with selenium")
time.sleep(1)
wait.until(EC.element_to_be_clickable((By.XPATH, feedback_xpath['uploadFile']))).send_keys(feedback_xpath['uploadFilePath'])
wait.until(EC.element_to_be_clickable((By.XPATH, feedback_xpath['4star']))).click()
time.sleep(1)
wait.until(EC.element_to_be_clickable((By.XPATH, feedback_xpath['submit']))).click()
time.sleep(10)

allFeedbacks.click()
time.sleep(10)

# --------------------------- DELETE FEEDBACK ---------------------------
manageCourts.click()
wait.until(EC.element_to_be_clickable((By.XPATH, feedback_xpath['delete']))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, feedback_xpath['confirmDelete']))).click()


# -- payment
# wait.until(EC.element_to_be_clickable((By.XPATH, payment_xpaths["username"])))
# element.send_keys(payment_credentials["mail"])
# time.sleep(1)
# wait.until(EC.element_to_be_clickable((By.XPATH, payment_xpaths["password"])))
# element.send_keys(payment_credentials["pwd"])
# time.sleep(1)
# wait.until(EC.element_to_be_clickable((By.XPATH, payment_xpaths["submit"]))).click()



# To get elements by xpath and click? $x("some xpath") in console.