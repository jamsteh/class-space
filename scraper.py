from selenium import webdriver
import json
import time

def compassLogin(safariDriver):
    with open(file = "login.json", mode = 'r') as rawLogin:
        login = json.loads(str(rawLogin.read()))

    username = login['username']
    password = login['password']
    print("successfully retrieved username and password from store")

    safariDriver.get("https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=authsearch")
    print("successfully arrived at howdy login")

    usernameField = safariDriver.find_element_by_id("username")
    passwordField = safariDriver.find_element_by_id("password")
    print("found username and password fields")

    usernameField.send_keys(username)
    passwordField.send_keys(password)
    time.sleep(4)
    passwordField.submit()
    print("successfully submitted username and password fields")

    # submitButton = safariDriver.find_element_by_name()

def compassMFA(safariDriver):
    phoneRowLabel = safariDriver.find_element_by_css_selector("div.row-label.phone-label")
    callButton = phoneRowLabel.find_element_by_css_selector("button.auth-button.positive")

    callButton.click()
    print("clicked duo call button")

def main():
    safariDriver = webdriver.Safari()
    safariDriver.implicitly_wait(10)
    compassLogin(safariDriver)
    time.sleep(5)
    mainWindow = safariDriver.current_window_handle
    safariDriver.switch_to.frame("duo_iframe")
    compassMFA(safariDriver)
    safariDriver.switch_to.window(mainWindow)
    time.sleep(10)
    print(safariDriver.page_source)

if __name__ == "__main__":
    main()
