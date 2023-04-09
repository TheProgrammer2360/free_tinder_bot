from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time


class TinderBot:
    def __init__(self):
        self.__total_swipes = 0
        self.__number_of_likes = 0
        self.__number_of_dislikes = 0
        self.URL = "https://tinder.com/"
        self.__driver = webdriver.Chrome(executable_path="/chromedriver.exe")
        self.__driver.maximize_window()
        self.__driver.get(self.URL)

    def __like(self) -> None:
        """Likes the profile that is currently showing"""
        # xpath of the button changes between the 2
        xpath1 = "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[4]/button"
        xpath2 = "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[4]/div/div[4]/button"
        # try xpath two first
        try:
            # use two because it seems that usually it is the one that shows up
            like_button = self.__driver.find_element(By.XPATH, xpath2)
        except NoSuchElementException:
            # when the button is not present
            # try xpath1
            like_button = self.__driver.find_element(By.XPATH, xpath1)

        # click the one like button that was found
        like_button.click()
        self.__number_of_likes += 1

    def __discard_notification(self) -> None:
        """discards the notifications that pop up after login: helper method"""
        xpath = "/html/body/div[2]/main/div/div/div/div[3]/button[1]"
        try:
            # wait for a maximum of 20 seconds for the first notification to show up
            WebDriverWait(self.__driver, 20).until(
                ec.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            # when the 20 seconds have passed but still the notification is not there, stop the app
            raise InternetErrorException("First notification is not detected")
        else:
            # When the notification is now present
            notification_response = self.__driver.find_element(By.XPATH, xpath)
            notification_response.click()
            # wait one second for the next notification to appear
            time.sleep(1)
            # update the xpath with the response of the next notification
            xpath = "/html/body/div[2]/main/div/div/div/div[3]/button[2]"
            notification_response = self.__driver.find_element(By.XPATH, xpath)
            notification_response.click()

    def __login_with_facebook(self, username: str, password: str) -> None:
        """will click the login with facebook on the second windows: helper method"""
        # switch to the second handle
        self.__driver.switch_to.window(self.__driver.window_handles[1])
        # login using the username and password specified
        username_area = self.__driver.find_element(By.ID, "email")
        username_area.send_keys(username)
        password_area = self.__driver.find_element(By.ID, "pass")
        password_area.send_keys(password)
        # wait 2 seconds and then click the login button
        time.sleep(2)
        login_button = self.__driver.find_element(By.ID, "loginbutton")
        login_button.click()
        # switch back to the first handle
        self.__driver.switch_to.window(self.__driver.window_handles[0])

    def __accept_cookies(self) -> None:
        """clicks the accept cookies when the notification shows up after logging in: helper method"""
        xpath = "/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/button"
        try:
            # wait 10 seconds for the accept button to be present
            WebDriverWait(self.__driver, 10).until(
                ec.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            # when 10 seconds have passed but still the accept button is not present
            raise TinderBotException("could not find the accept button")
        else:
            # when the button is present, find it and click it
            accept_button = self.__driver.find_element(By.XPATH, xpath)
            accept_button.click()

    def login(self, username: str, password: str) -> None:
        """will log in the user with using their facebook credentials"""
        self.__accept_cookies()
        xpath = "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a"
        try:
            # wait maximum of 10 seconds for the log in link to be present
            WebDriverWait(self.__driver, 10).until(
                ec.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            # When the element is not present after the 10 seconds have passed, stop the program
            raise TinderBotException("The login button is not found")
        else:
            # when the button is now present on screen, get hold of it and click it
            login_button = self.__driver.find_element(By.XPATH, xpath)
            login_button.click()

        # xpath for the login with facebook button
        xpath = "/html/body/div[2]/main/div/div/div[1]/div/div/div[3]/span/div[2]/button"
        # wait for 5 seconds for the Google button to disappear and return
        time.sleep(5)
        # get the login with facebook button and click it
        login_button = self.__driver.find_element(By.XPATH, xpath)
        login_button.click()
        # login on the second window
        self.__login_with_facebook(username=username, password=password)
        self.__discard_notification()

    def __dislike(self) -> None:
        """Likes the current profile that is currently showing"""
        # before any swiping has been done the xpath for the dislike button is xpath_one but changes after a swipe
        # has been made to xpath_two
        xpath_one = "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[2]/button"
        xpath_two = "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[4]/div/div[2]/button"
        if self.__number_of_likes == 0 and self.__number_of_dislikes == 0:
            # this run only when the has never been a swipe
            dislike_button = self.__driver.find_element(By.XPATH, xpath_one)
        else:
            # this will run if this is not the first swipe
            dislike_button = self.__driver.find_element(By.XPATH, xpath_two)

        # click the button and update the number of dislike
        dislike_button.click()
        self.__number_of_dislikes += 1

    def __str__(self):
        return f"Likes: {self.__number_of_likes}\nDislikes: {self.__number_of_dislikes}\nTotal: {self.__total_swipes}"

    def __is_it_out_of_likes(self) -> bool:
        """Checks if disturbance is caused by out of likes notification"""
        xpath = "/html/body/div[2]/main/div/div[1]/div[2]/div[1]/span[1]/div/div/span/div/h3"
        try:
            # try getting hold of the heading
            heading = self.__driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            # if the heading is not found
            return False
        else:
            # if it is found make sure it is the correct heading
            return heading.text == "You're Out of Likes!"

    def __is_it_add_tinder_to_home_screen(self) -> bool:
        """Checks to see if the notification is for add tinder to home screen"""
        xpath = "/html/body/div[2]/main/div/div[1]/div[2]/h1"
        try:
            # try to get the heading
            heading = self.__driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            # when the xpath finds is pointing at something not in the screen
            return False
        else:
            # make sure it is the right notification
            return heading.text == "Add Tinder to your Home Screen"

    def swiper(self, total: int, like: int, dislike: int) -> None:
        """will swipe left and right in proportion and until the 'total' number is reached"""
        # wait for a maximum of 14 seconds for the like button to be present
        xpath = "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[4]/button"
        try:
            WebDriverWait(self.__driver, 30).until(
                ec.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            # end the up
            raise InternetErrorException("Like button is still not showing")
        else:
            # wait two seconds to make it human like
            time.sleep(2)

        # run the loop as long as the total number of swipes has not been reached
        while self.__total_swipes != total:
            for i in range(0, like):
                # like the present profile
                self.__like()
                # increment the total number of likes
                self.__total_swipes += 1
                # if the total likes is reached stop the liking
                if self.__total_swipes == total:
                    break
                time.sleep(2)
                # check to see if there is an notification
                if self.__is_there_a_notification:
                    # if there is a notification dismiss it
                    self.__dismiss_notification_while_swiping()
                    # wait 2 seconds for the notification to disappear
                    time.sleep(2)
            if self.__total_swipes != total:
                for j in range(0, dislike):
                    # dislike
                    self.__dislike()
                    # increment the total number of swipes
                    self.__total_swipes += 1
                    # check if the total number is reached and if is it stop swiping
                    if self.__total_swipes == total:
                        break
                    # check if there is a notification and dismiss it when it occurs
                    time.sleep(1)

                    if self.__is_there_a_notification:
                        # if there is a notification dismiss it
                        self.__dismiss_notification_while_swiping()
                        # wait 2 seconds for the notification to disappear
                        time.sleep(2)
            time.sleep(5)
        print(self.__str__())



    def __dismiss_notification_while_swiping(self) -> None:
        """dismisses the notification that is currently open"""
        if self.__is_it_out_of_likes():
            # stop the program
            raise OutOfLikesException("Out of likes")
        elif self.__is_it_add_tinder_to_home_screen():
            # close the notification
            close_button_xpath = "/html/body/div[2]/main/div/div[2]/button[2]"
            close_button = self.__driver.find_element(By.XPATH, close_button_xpath)
            close_button.click()
        # wait 1 second for it to fully close the notification
        time.sleep(1)

    def __is_there_a_notification(self) -> bool:
        """checks to see if we do have a notification"""
        return self.__is_it_out_of_likes() or self.__is_it_add_tinder_to_home_screen()


class TinderBotException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InternetErrorException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class OutOfLikesException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
