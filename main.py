from tinder import TinderBot
import os

if __name__ == '__main__':
    print("Welcome to the Tinder Swiper")
    total = int(input("Enter the number of total swipes that you would like: "))
    like = int(input("Enter the number of likes you would like to do before disliking: "))
    dislike = int(input("Enter the number of dislikes you would do before going to like again: "))
    bot = TinderBot()
    # login using facebook details
    bot.login(username=os.environ["PHONENUMBER"], password=os.environ["PASSWORD"])
    bot.swiper(total, like, dislike)

