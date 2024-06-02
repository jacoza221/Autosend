import io, os, time
import sys
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from winreg import *
import find_github_email
import smtplib
from email.message import EmailMessage

class Main:
    def __init__(self,):
        file_name = f'.\\account.json'
        with open(file_name) as file:
            info = json.load(file)

        self.mail = info['mail']
        self.password = info['password']
        self.content = info['content']
        self.getUserData = []
        self.allEmails = []

        # open the browser
        # options = webdriver.ChromeOptions()
        # options.add_argument("user-data-dir=C:\\Users\\3\\AppData\\Local\\Google\\Chrome\\User Data")
        # options.add_argument("profile-directory=Profile 5")
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.Chrome(options=options)
        # self.driver.maximize_window()
        # self.driver.quit()

        self.getUserInfo()

    def loadCompleted(self, locator, timeout):
        """ check website load complete """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            return True
        except TimeoutException:
            return False

    def clickElement(self, xpath_element):
        """ find element on website then click """
        try:
            if self.loadCompleted(xpath_element, 30):
                element = self.driver.find_element(By.XPATH, xpath_element)
                element.click()

        except NoSuchElementException:
            print("can not find element:", xpath_element)
        except Exception:
            print("can not click try perform ")
            time.sleep(10)
            ex_element = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, xpath_element)))
            # ex_element = self.driver.find_element(By.XPATH, xpath_element)
            ActionChains(self.driver).click(ex_element).perform()

    def click_select_date(self, id_btn):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, id_btn)))
            down_arrow_btn = self.driver.find_element(By.ID, id_btn)
            down_arrow_btn.click()
            print("click:" + id_btn)
        except Exception:
            print("can't find %s, try run javaScript" % id_btn)


    def getUserInfo(self):
        """ get users profile of github """
        self.driver.get("https://committers.top/switzerland")
        try:
            if self.loadCompleted("/html/body/div/section/table[1]", 30):
                table_element = self.driver.find_element(By.CLASS_NAME, 'users-list')
                tbody = table_element.find_element(By.TAG_NAME, 'tbody')
                rows = tbody.find_elements(By.TAG_NAME, 'tr')
                table_data = []

                for row in rows:
                    a_cells = row.find_elements(By.TAG_NAME, 'a')
                    # user_url = [cell.get_attribute("href") for cell in a_cells]
                    user_url = [cell.text for cell in a_cells]
                    if user_url:  # Check if the list is not empty
                        first_url = user_url[0]  # Get the first URL from the list
                        table_data.append(first_url)  # Append the first URL to the table_data list
                    # with open('extract_data.txt', mode='a', encoding='utf-8') as log_file:
                    #     log_file.write(' '.join(row_data) + '\n')
                self.getUserData = table_data
                self.driver.quit()
                self.getEmail()
        except TimeoutException:
            print("not find user table so exit program")
            sys.exit()
        except:
            print("has been login Ipaybank - can't find element")

    def getEmail(self):
        for githubUsername in self.getUserData:
            try:
                response = find_github_email.find(str(githubUsername))
            except:
                print(f"Email not find reason is find_github_email module error : username is{githubUsername}")
            if response['found'] == False:
                print(response)
            else:
                for eachEmail in response['email']:
                    self.allEmails.append(eachEmail)

    def sendEmail(self):
        for eachEmail in self.allEmails:
            pass

if __name__ == "__main__":
    Main()
    # result = find_github_email.find("fabian")
    # print(result)

