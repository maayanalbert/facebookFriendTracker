
# database models

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from django.db.models.signals import post_save
from django.dispatch import receiver

import csv
import getpass
import os
import time

from datetime import datetime
from selenium import webdriver

# Django comes with built in user models. However, the information you can store
# in them is limited. To add more information, I created a profile model that
# updates with the user model and contains additional relevant properties.

# Update profile models with user models.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_day = models.IntegerField(default=0)
    facebook_email = models.CharField(max_length=200)
    interval_time = models.IntegerField(default=300)
    total_time = models.IntegerField(default=302400)
    tracking = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    def testFunction(self):
        return "hi"

    # A scraper that count the number of friends one has online. 
    # From https://github.com/bhamodi/facebook-online-friend-tracker
    def runScraper(self, facebook_password):
        # Compute total number of iterations and initialize iteration counter.
        iteration = 0

        # Initialize Chrome WebDriver.
        print('\nInitializing Chrome WebDriver...')
        driver = webdriver.Chrome()

        # Change default timeout and window size.
        driver.implicitly_wait(120)
        driver.set_window_size(700, 500)

        # Go to www.facebook.com and log in using the provided credentials.
        print('Logging into Facebook...')
        driver.get('https://www.facebook.com/')
        emailBox = driver.find_element_by_id('email')
        emailBox.send_keys(self.facebook_email)
        passwordBox = driver.find_element_by_id('pass')
        passwordBox.send_keys(facebook_password)
        driver.find_element_by_id('loginbutton').click()
        while iteration < number_of_iterations:
            # Wait for Facebook to update the number of online friends.
            print('\nWaiting for Facebook to update friends list... (This takes approximately 3 minutes.)')
            time.sleep(180)

            # Scrape the number of online friends.
            onlineFriendsCount = driver.find_element_by_xpath('//*[@id="fbDockChatBuddylistNub"]/a/span[2]/span').text.strip('()')
            if onlineFriendsCount:
                onlineFriendsCount = int(onlineFriendsCount)
            else:
                onlineFriendsCount = 0
                print('Done! Detected ' + str(onlineFriendsCount) + 
                    ' online friends.')

            # Get current time.
            today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Add a log
            self.log_set.create(log_time = today, 
                friends_online = onlineFriendsCount)
            print('Added: ' + today + ' -> ' + str(onlineFriendsCount) + 
                ' as a log.')

            # Wait for next interval and increment iteration counter.
            time.sleep(self.interval_time - 180)
            iteration += 1

        # Close Chrome WebDriver.
        driver.quit()

# The log model that stores how many friends have been online when.
class Log(models.Model):
    # Maps log to the correct profile. 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)

    log_time = models.DateTimeField('time logged')
    friends_online = models.IntegerField(default=0)

