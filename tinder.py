from selenium import webdriver


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

    def login(self, username: str, password: str) -> None:
        """will log in the user with using their facebook credentials"""

    def swiper(self, total: int, like: int, dislike: int) -> None:
        """will swipe left and right in proportion and until the 'total' number is reached"""

