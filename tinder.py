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
        time.sleep(3600)

    def swiper(self, total: int, like: int, dislike: int) -> None:
        """will swipe left and right in proportion and until the 'total' number is reached"""


class TinderBotException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
