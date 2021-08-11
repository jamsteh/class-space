from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
from bcolors import bcolors

def compassLogin(safariDriver):
    with open(file = "login.json", mode = 'r') as rawLogin:
        login = json.loads(str(rawLogin.read()))

    username = login['username']
    password = login['password']
    print("retrieved username and password from store")

    safariDriver.get("https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/term/termSelection?mode=authsearch")
    print("arrived at howdy login")

    time.sleep(1)
    usernameField = safariDriver.find_element_by_id("username")
    passwordField = safariDriver.find_element_by_id("password")
    print("found username and password fields")

    usernameField.send_keys(username)
    passwordField.send_keys(password)
    time.sleep(4)
    passwordField.submit()
    print("submitted username and password fields")

    # submitButton = safariDriver.find_element_by_name()

def compassMFA(safariDriver):
    phoneRowLabel = safariDriver.find_element_by_css_selector("div.row-label.phone-label")
    callButton = phoneRowLabel.find_element_by_css_selector("button.auth-button.positive")

    callButton.click()
    print("clicked duo call button")

def compassTermSelect(safariDriver):
    # term-go - submit button ID
    # termForm = safariDriver.find_element_by_xpath("//fieldset@[role='form']")
    # s2id_autogen1_search
    # click on element first to let s2id_autogen1_search become fillable
    termFieldLink = safariDriver.find_element_by_css_selector("a.select2-choice")
    termFieldLink.click()
    termField = safariDriver.find_element_by_id("s2id_autogen1_search")
    termField.send_keys("Fall 2021 - College Station")
    time.sleep(2)
    termField.send_keys(Keys.ENTER)
    time.sleep(2)
    submitButton = safariDriver.find_element_by_id("term-go")
    submitButton.click()
    print("selected term")

def compassClassSelect(safariDriver):
    # submit button id: search-go
    # subject input id: s2id_autogen1
    print("searching aero courses...")
    subjectField = safariDriver.find_element_by_id("s2id_autogen1")
    subjectField.click()
    subjectField.send_keys("AERO - Aerospace Engineering")
    time.sleep(3)
    subjectField.send_keys(Keys.ENTER)
    time.sleep(3)
    

    rangeField = safariDriver.find_element_by_id("txt_course_number_range")
    rangeFieldTo = safariDriver.find_element_by_id("txt_course_number_range_to")

    rangeField.send_keys("400")
    rangeFieldTo.send_keys("500")

    submitButton = safariDriver.find_element_by_id("search-go")
    time.sleep(3)
    submitButton.click()

def compassTableScrape(safariDriver):
    time.sleep(3)
    print("found aero courses")
    numRows = len(safariDriver.find_elements_by_xpath("//*[@id='table1']/tbody/tr"))
    safariDriver.implicitly_wait(0)
    print("----------------------------")
    for rowIndex in range(1, numRows):
        try:
            subject = safariDriver.find_element_by_xpath(f"//*[@id='table1']/tbody/tr[{rowIndex}]/td[3]").text
            courseNumber = safariDriver.find_element_by_xpath(f"//*[@id='table1']/tbody/tr[{rowIndex}]/td[4]").text
            instructor = safariDriver.find_element_by_xpath(f"//*[@id='table1']/tbody/tr[{rowIndex}]/td[7]").find_element_by_css_selector("a.email").text
            try:
                occupiedSeats = safariDriver.find_element_by_xpath(f"//*[@id='table1']/tbody/tr[{rowIndex}]/td[11]/span[1]/span[2]").text
                maxSeats = safariDriver.find_element_by_xpath(f"//*[@id='table1']/tbody/tr[{rowIndex}]/td[11]/span[2]/span[2]").text
            except Exception:
                occupiedSeats = safariDriver.find_element_by_xpath(f"//*[@id='table1']/tbody/tr[{rowIndex}]/td[11]/span[2]/span[2]").text
                maxSeats = safariDriver.find_element_by_xpath(f"//*[@id='table1']/tbody/tr[{rowIndex}]/td[11]/span[3]/span[2]").text
                
            outputClassSpace(subject, courseNumber, instructor, occupiedSeats, maxSeats)
        except Exception:
            pass

def outputClassSpace(subject, courseNumber, instructor, occupiedSeats, maxSeats):
    if (occupiedSeats < maxSeats):
        print(f"{bcolors.OKGREEN}{subject : <4} {courseNumber : <3} | {instructor : <30} | {occupiedSeats : >3}/{maxSeats : <3}")
        return
    print(f"{bcolors.FAIL}{subject : <4} {courseNumber : <3} | {instructor : <30} | {occupiedSeats : >3}/{maxSeats : <3}")

    

def main():
    safariDriver = webdriver.Safari()
    safariDriver.set_window_position(0,0)
    safariDriver.set_window_size(1500,800)
    safariDriver.implicitly_wait(10)
    compassLogin(safariDriver)
    time.sleep(5)
    mainWindow = safariDriver.current_window_handle
    safariDriver.switch_to.frame("duo_iframe")
    compassMFA(safariDriver)
    safariDriver.switch_to.window(mainWindow)
    time.sleep(10)
    compassTermSelect(safariDriver)
    time.sleep(10)
    compassClassSelect(safariDriver)
    time.sleep(10)
    compassTableScrape(safariDriver)

if __name__ == "__main__":
    main()
