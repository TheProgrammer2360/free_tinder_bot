from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import time


class TinderBot:
    def __init__(self):
        self.URL = "https://tinder.com/"
        self.driver = webdriver.Chrome(executable_path="/chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get(self.URL)

    def __discard_notification(self) -> None:
        """discards the notifications that pop up after login: helper method"""

    def __login_with_facebook(self) -> None:
        """will click the login with facebook: helper method"""

    def __accept_cookies(self) -> None:
        """clicks the accept cookies when the notification shows up after logging in: helper method"""
        xpath = "/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/button"
        try:
            # wait 10 seconds for the accept button to be present
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            # when 10 seconds have passed but still the accept button is not present
            raise TinderBotException("could not find the accept button")
        else:
            # when the button is present, find it and click it
            accept_button = self.driver.find_element(By.XPATH, xpath)
            accept_button.click()

    def login(self, username: str, password: str) -> None:
        """will log in the user with using their facebook credentials"""
        self.__accept_cookies()
        xpath = "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a"
        try:
            # wait maximum of 10 seconds for the log in link to be present
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            # When the element is not present after the 10 seconds have passed, stop the program
            raise TinderBotException("The login button is not found")
        else:
            # when the button is now present on screen, get hold of it and click it
            login_button = self.driver.find_element(By.XPATH, xpath)
            login_button.click()

        # xpath for the login with facebook button
        xpath = "/html/body/div[2]/main/div/div/div[1]/div/div/div[3]/span/div[2]/button"
        # wait for 5 seconds for the Google button to disappear and return
        time.sleep(5)
        # get the login with facebook button and click it
        login_button = self.driver.find_element(By.XPATH, xpath)
        login_button.click()
        time.sleep(3600)

    def swiper(self, total: int, like: int, dislike: int) -> None:
        """will swipe left and right in proportion and until the 'total' number is reached"""


class TinderBotException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
