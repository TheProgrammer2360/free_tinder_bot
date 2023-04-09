from tinder import TinderBot, OutOfLikesException
import time
import os

if __name__ == '__main__':
    print("Welcome to the Tinder Swiper")
    total = int(input("Enter the number of total swipes that you would like: "))
    like = int(input("Enter the number of likes you would like to do before disliking: "))
    dislike = int(input("Enter the number of dislikes you would do before going to like again: "))
    bot = TinderBot()
    time.sleep(5)
    # login using facebook details
    bot.login(username=os.environ["PHONENUMBER"], password=os.environ["PASSWORD"])
    # make the bot show the number of likes and dislikes completed at the end of the app
    try:
        bot.swiper(total, like, dislike)
    except OutOfLikesException:
        print(bot)

