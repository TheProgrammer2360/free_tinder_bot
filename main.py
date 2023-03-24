from tinder import TinderBot
import os

if __name__ == '__main__':
    bot = TinderBot()
    # login using facebook details
    bot.login(username=os.environ["PHONENUMBER"], password=os.environ["PASSWORD"])

